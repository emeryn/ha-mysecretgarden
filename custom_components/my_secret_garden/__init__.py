import logging
from datetime import timedelta
import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, CONF_API_URL

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor", "binary_sensor", "button"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initialise l'intégration depuis l'interface UI."""
    api_url = entry.data[CONF_API_URL]

    async def async_update_data():
        """Récupère l'état global depuis FastAPI."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{api_url}/api/ha/state") as response:
                    response.raise_for_status()
                    return await response.json()
            except Exception as err:
                raise UpdateFailed(f"Erreur API My Secret Garden: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="My Secret Garden Data",
        update_method=async_update_data,
        update_interval=timedelta(minutes=60),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api_url": api_url
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Supprime l'intégration proprement."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
