from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SSL

from .const import (
    CONF_INPUT_LABEL_FORMAT,
    CONF_INPUT_LABELS,
    CONF_INPUT_LABEL_1,
    CONF_INPUT_LABEL_2,
    CONF_INPUT_LABEL_3,
    CONF_INPUT_LABEL_4,
    CONF_OUTPUT_LABEL_FORMAT,
    CONF_OUTPUT_LABELS,
    CONF_OUTPUT_LABEL_1,
    CONF_OUTPUT_LABEL_2,
    CONF_OUTPUT_LABEL_3,
    CONF_OUTPUT_LABEL_4,
    CONF_PATH,
    DEFAULT_INPUT_LABELS,
    DEFAULT_OUTPUT_LABELS,
    DEFAULT_PATH,
    DEFAULT_PORT,
    DEFAULT_SSL,
    DOMAIN,
)


class HDMIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        return HDMIOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                    vol.Optional(CONF_SSL, default=DEFAULT_SSL): bool,
                    vol.Optional(CONF_PATH, default=DEFAULT_PATH): str,
                    vol.Optional(CONF_INPUT_LABEL_1, default=DEFAULT_INPUT_LABELS[0]): str,
                    vol.Optional(CONF_INPUT_LABEL_2, default=DEFAULT_INPUT_LABELS[1]): str,
                    vol.Optional(CONF_INPUT_LABEL_3, default=DEFAULT_INPUT_LABELS[2]): str,
                    vol.Optional(CONF_INPUT_LABEL_4, default=DEFAULT_INPUT_LABELS[3]): str,
                    vol.Optional(CONF_OUTPUT_LABEL_1, default=DEFAULT_OUTPUT_LABELS[0]): str,
                    vol.Optional(CONF_OUTPUT_LABEL_2, default=DEFAULT_OUTPUT_LABELS[1]): str,
                    vol.Optional(CONF_OUTPUT_LABEL_3, default=DEFAULT_OUTPUT_LABELS[2]): str,
                    vol.Optional(CONF_OUTPUT_LABEL_4, default=DEFAULT_OUTPUT_LABELS[3]): str,
                }
            ),
            errors=errors,
        )


class HDMIOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = {**self._config_entry.data, **self._config_entry.options}

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_INPUT_LABEL_1, default=current.get(CONF_INPUT_LABEL_1, DEFAULT_INPUT_LABELS[0])): str,
                    vol.Optional(CONF_INPUT_LABEL_2, default=current.get(CONF_INPUT_LABEL_2, DEFAULT_INPUT_LABELS[1])): str,
                    vol.Optional(CONF_INPUT_LABEL_3, default=current.get(CONF_INPUT_LABEL_3, DEFAULT_INPUT_LABELS[2])): str,
                    vol.Optional(CONF_INPUT_LABEL_4, default=current.get(CONF_INPUT_LABEL_4, DEFAULT_INPUT_LABELS[3])): str,
                    vol.Optional(CONF_OUTPUT_LABEL_1, default=current.get(CONF_OUTPUT_LABEL_1, DEFAULT_OUTPUT_LABELS[0])): str,
                    vol.Optional(CONF_OUTPUT_LABEL_2, default=current.get(CONF_OUTPUT_LABEL_2, DEFAULT_OUTPUT_LABELS[1])): str,
                    vol.Optional(CONF_OUTPUT_LABEL_3, default=current.get(CONF_OUTPUT_LABEL_3, DEFAULT_OUTPUT_LABELS[2])): str,
                    vol.Optional(CONF_OUTPUT_LABEL_4, default=current.get(CONF_OUTPUT_LABEL_4, DEFAULT_OUTPUT_LABELS[3])): str,
                }
            ),
        )
