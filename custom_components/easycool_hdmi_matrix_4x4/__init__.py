from __future__ import annotations

try:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
except ImportError:  # pragma: no cover - exercised in test environments without HA
    ConfigEntry = object  # type: ignore[assignment]
    HomeAssistant = object  # type: ignore[assignment]

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the HDMI matrix integration from a Home Assistant config entry."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {"entry": entry}
    await hass.config_entries.async_forward_entry_setups(entry, ["select"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the HDMI matrix integration."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["select"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
