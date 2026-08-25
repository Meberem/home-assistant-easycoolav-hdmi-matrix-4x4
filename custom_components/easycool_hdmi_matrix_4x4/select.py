from __future__ import annotations

import logging

try:
    from homeassistant.components.select import SelectEntity
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.exceptions import HomeAssistantError
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
except ImportError:  # pragma: no cover - exercised in test environments without HA
    SelectEntity = object  # type: ignore[assignment]
    ConfigEntry = object  # type: ignore[assignment]
    HomeAssistant = object  # type: ignore[assignment]
    HomeAssistantError = RuntimeError  # type: ignore[assignment]
    AddEntitiesCallback = object  # type: ignore[assignment]

from .bridge import read_state, send_route
from .const import (
    CONF_HOST,
    CONF_INPUT_LABEL_FORMAT,
    CONF_INPUT_LABELS,
    CONF_OUTPUT_LABEL_FORMAT,
    CONF_OUTPUT_LABELS,
    CONF_PATH,
    CONF_PORT,
    CONF_SSL,
    DEFAULT_INPUT_LABELS,
    DEFAULT_OUTPUT_LABELS,
    DOMAIN,
    INPUT_COUNT,
    OUTPUT_COUNT,
    get_labels,
    merge_entry_data,
)

_LOGGER = logging.getLogger(__name__)


class HDMIOutputSelect(SelectEntity):
    """Expose one routing selector per output."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:video-input-hdmi"

    def __init__(self, entry: ConfigEntry, output_num: int) -> None:
        self._entry = entry
        self._output_num = output_num
        self._attr_unique_id = f"{entry.entry_id}-output-{output_num}"
        label_data = merge_entry_data(entry.data, entry.options)
        self._input_labels = get_labels(
            label_data,
            CONF_INPUT_LABELS,
            CONF_INPUT_LABEL_FORMAT,
            DEFAULT_INPUT_LABELS,
        )
        self._output_labels = get_labels(
            label_data,
            CONF_OUTPUT_LABELS,
            CONF_OUTPUT_LABEL_FORMAT,
            DEFAULT_OUTPUT_LABELS,
        )
        self._attr_options = self._input_labels
        self._option_map = {label: index + 1 for index, label in enumerate(self._input_labels)}
        self._attr_current_option = None
        self._current_input = None
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_HOST],
            "manufacturer": "HDMI Matrix",
            "model": "4x4 HDMI Matrix",
            "configuration_url": f"http://{entry.data[CONF_HOST]}:{entry.data.get(CONF_PORT, 80)}{entry.data.get(CONF_PATH, "/")}",
        }

    @property
    def name(self) -> str:
        return self._output_labels[self._output_num - 1]

    @property
    def device_info(self) -> dict[str, object]:
        return self._attr_device_info

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def current_option(self) -> str | None:
        if self._current_input is not None:
            return self._input_labels[self._current_input - 1]
        return self._attr_current_option

    async def async_select_option(self, option: str) -> None:
        input_num = self._option_map.get(option)
        if input_num is None:
            raise HomeAssistantError(f"Unknown input label: {option}")
        try:
            states = await self.hass.async_add_executor_job(
                send_route,
                self._entry.data[CONF_HOST],
                self._entry.data[CONF_PORT],
                self._entry.data.get(CONF_SSL, False),
                self._entry.data.get(CONF_PATH, "/"),
                self._output_num,
                input_num,
            )
        except Exception as exc:  # pragma: no cover - defensive logging path
            _LOGGER.exception("Unable to send route command for output %s", self._output_num)
            raise HomeAssistantError(str(exc)) from exc

        self._current_input = states.get(self._output_num)
        self._attr_current_option = option
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        await self.async_update()

    async def async_update(self) -> None:
        try:
            states = await self.hass.async_add_executor_job(
                read_state,
                self._entry.data[CONF_HOST],
                self._entry.data[CONF_PORT],
                self._entry.data.get(CONF_SSL, False),
                self._entry.data.get(CONF_PATH, "/"),
            )
            self._current_input = states.get(self._output_num)
            if self._current_input is not None:
                self._attr_current_option = self._input_labels[self._current_input - 1]
        except Exception:  # pragma: no cover - matrix state may be unavailable at startup
            _LOGGER.debug("Unable to read HDMI matrix state for output %s", self._output_num)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create four selectors for the HDMI matrix outputs."""
    entities = [HDMIOutputSelect(entry, output_num) for output_num in range(1, OUTPUT_COUNT + 1)]
    async_add_entities(entities)
