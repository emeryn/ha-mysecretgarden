from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    entities = [
        GlobalPlantCountSensor(coordinator),
        GlobalThirstyCountSensor(coordinator),
        # --- LIGNES AJOUTÉES POUR LES GODETS ---
        GodetCountSensor(coordinator),
        GodetVarietesSensor(coordinator)
    ]
    
    for bac in coordinator.data.get("bacs", []):
        entities.append(BacPlantCountSensor(coordinator, bac["id"], bac["nom"]))
        
    async_add_entities(entities)

class GlobalPlantCountSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Total des plants"
        self._attr_unique_id = "msg_global_plant_count"
        self._attr_icon = "mdi:sprout"
        self._attr_native_unit_of_measurement = "plants"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, "global_garden")}, "name": "Mon Potager (Global)", "manufacturer": "My Secret Garden"}

    @property
    def native_value(self):
        return sum(bac.get("plant_count", 0) for bac in self.coordinator.data.get("bacs", []))


class GlobalThirstyCountSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Éléments à arroser"
        self._attr_unique_id = "msg_global_thirsty_count"
        self._attr_icon = "mdi:watering-can"
        self._attr_native_unit_of_measurement = "éléments"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, "global_garden")}, "name": "Mon Potager (Global)", "manufacturer": "My Secret Garden"}

    @property
    def native_value(self):
        bacs_soif = sum(1 for b in self.coordinator.data.get("bacs", []) if b.get("needs_water"))
        pots_soif = sum(1 for p in self.coordinator.data.get("pots", []) if p.get("needs_water"))
        return bacs_soif + pots_soif


class GodetCountSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Nombre total de godets"
        self._attr_unique_id = "msg_godets_total"
        self._attr_icon = "mdi:seed"
        self._attr_native_unit_of_measurement = "godets"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, "godets_garden")}, "name": "Mes Godets", "manufacturer": "My Secret Garden", "model": "Pouponnière"}

    @property
    def native_value(self):
        return self.coordinator.data.get("godets", {}).get("total", 0)

    @property
    def extra_state_attributes(self):
        """Affiche le détail des godets dans les infos supplémentaires"""
        return {"Détails": self.coordinator.data.get("godets", {}).get("details", "")}


class GodetVarietesSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Variétés en semis"
        self._attr_unique_id = "msg_godets_varietes"
        self._attr_icon = "mdi:leaf"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, "godets_garden")}, "name": "Mes Godets", "manufacturer": "My Secret Garden", "model": "Pouponnière"}

    @property
    def native_value(self):
        return self.coordinator.data.get("godets", {}).get("varietes", 0)


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
        return {"identifiers": {(DOMAIN, f"bac_{self.bac_id}")}, "name": self.bac_nom, "manufacturer": "My Secret Garden", "model": "Bac de culture"}

    @property
    def native_value(self):
        for bac in self.coordinator.data.get("bacs", []):
            if bac["id"] == self.bac_id:
                return bac["plant_count"]
        return 0