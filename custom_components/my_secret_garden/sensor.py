from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    entities = []
    
    for bac in coordinator.data.get("bacs", []):
        entities.append(BacPlantCountSensor(coordinator, bac["id"], bac["nom"]))
        
    async_add_entities(entities)

class BacPlantCountSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, bac_id, bac_nom):
        super().__init__(coordinator)
        self.bac_id = bac_id
        self.bac_nom = bac_nom
        self._attr_name = f"Plants dans {bac_nom}"
        self._attr_unique_id = f"msg_bac_{bac_id}_count"
        self._attr_icon = "mdi:sprout"
        self._attr_native_unit_of_measurement = "plants"

    @property
    def device_info(self):
        """Regroupe cette entité sous l'appareil 'Bac XYZ' dans HA."""
        return {
            "identifiers": {(DOMAIN, f"bac_{self.bac_id}")},
            "name": self.bac_nom,
            "manufacturer": "My Secret Garden",
            "model": "Bac de culture"
        }

    @property
    def native_value(self):
        for bac in self.coordinator.data.get("bacs", []):
            if bac["id"] == self.bac_id:
                return bac["plant_count"]
        return 0
