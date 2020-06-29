from ha_core.alert import Alert
from ha_core.state import State
from ha_utils.ha_const import Generic, Light

class LightAlert(Alert):
  alert_id = "light"

  def parse_kwargs(self, kwargs) -> None:
    self.lights = kwargs["lights"]

  async def alarm_fired(self, sensor_fired) -> None:
    for light in self.lights:
      await self.toggle_light({"light": light})

  async def toggle_light(self, kwargs):
    light = kwargs["light"]
    if self.state.fired:
      await self.hass.call_service(
        Light.LIGHT_TOGGLE,
        entity_id=light,
        color_name="red",
        brightness=255
      )
      await self.hass.run_in(self.toggle_light, 1, light = light)
    else:
      self.hass.log(f"Alarm from {light} has been stopped")

  async def alarm_stopped(self) -> None:
    self.hass.log("Stopping lights...")
    for light in self.lights:
      await self.hass.call_service(
        Light.LIGHT_TURN_OFF,
        entity_id=light
      )
