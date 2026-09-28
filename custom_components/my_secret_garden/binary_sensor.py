from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    entities = [BacWaterSensor(coordinator, b["id"], b["nom"]) for b in coordinator.data.get("bacs", [])]
    entities.extend([PotWaterSensor(coordinator, p["id"], p["nom"]) for p in coordinator.data.get("pots", [])])
    async_add_entities(entities)

class BacWaterSensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator, bac_id, bac_nom):
        super().__init__(coordinator)
        self.bac_id = bac_id
        self.bac_nom = bac_nom
        self._attr_name = f"Besoin d'eau {bac_nom}"
        self._attr_unique_id = f"msg_bac_{bac_id}_water"
        self._attr_icon = "mdi:water-alert"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"bac_{self.bac_id}")}, 
            "name": self.bac_nom, 
            "manufacturer": "My Secret Garden"
        }

    @property
    def is_on(self):
        for bac in self.coordinator.data.get("bacs", []):
            if bac["id"] == self.bac_id: return bac["needs_water"]
        return False

class PotWaterSensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator, pot_id, pot_nom):
        super().__init__(coordinator)
        self.pot_id = pot_id
        self.pot_nom = pot_nom
        self._attr_name = f"Besoin d'eau {pot_nom}"
        self._attr_unique_id = f"msg_pot_{pot_id}_water"
        self._attr_icon = "mdi:flower"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pot_{self.pot_id}")}, 
            "name": self.pot_nom, 
            "manufacturer": "My Secret Garden", 
            "model": "Pot"
        }

    @property
    def is_on(self):
        for pot in self.coordinator.data.get("pots", []):
            if pot["id"] == self.pot_id: return pot["needs_water"]
        return False
