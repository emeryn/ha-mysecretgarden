import aiohttp
from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    api_url = data["api_url"]
    
    entities = []
    
    # Bouton Global (Nouveau)
    entities.append(GlobalWaterButton(coordinator, api_url))
    
    # Boutons individuels
    entities.extend([WaterButton(coordinator, api_url, "bac", b["id"], b["nom"]) for b in coordinator.data.get("bacs", [])])
    entities.extend([WaterButton(coordinator, api_url, "pot", p["id"], p["nom"]) for p in coordinator.data.get("pots", [])])
    
    async_add_entities(entities)


class GlobalWaterButton(ButtonEntity):
    """Bouton rattaché à l'appareil Global pour tout arroser."""
    def __init__(self, coordinator, api_url):
        self.coordinator = coordinator
        self.api_url = api_url
        self._attr_name = "Tout arroser"
        self._attr_unique_id = "msg_btn_water_global"
        self._attr_icon = "mdi:watering-can"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, "global_garden")}, "name": "Mon Potager (Global)", "manufacturer": "My Secret Garden"}

    async def async_press(self):
        async with aiohttp.ClientSession() as session:
            await session.post(f"{self.api_url}/api/ha/arrosage/valider_tout")
            await self.coordinator.async_request_refresh()


class WaterButton(ButtonEntity):
    def __init__(self, coordinator, api_url, item_type, item_id, item_nom):
        self.coordinator = coordinator
        self.api_url = api_url
        self.item_type = item_type
        self.item_id = item_id
        self.item_nom = item_nom
        self._attr_name = f"Valider arrosage {item_nom}"
        self._attr_unique_id = f"msg_btn_water_{item_type}_{item_id}"
        self._attr_icon = "mdi:water-pump"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, f"{self.item_type}_{self.item_id}")}, "name": self.item_nom}

    async def async_press(self):
        async with aiohttp.ClientSession() as session:
            await session.post(f"{self.api_url}/api/ha/arrosage/valider/{self.item_type}/{self.item_id}")
            await self.coordinator.async_request_refresh()