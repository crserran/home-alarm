import appdaemon.plugins.hass.hassapi as hass
from ha_core.alert import Alert
from ha_core.state import State
from ha_utils.ha_const import Generic, Switch


class SwitchAlert(Alert):
    alert_id = "switch"

    def parse_kwargs(self, kwargs) -> None:
        self.switches = kwargs["switches"]

    async def alarm_fired(self, sensor_fired) -> None:
        for switch in self.switches:
            await self.hass.call_service(Switch.TURN_ON, entity_id=switch)

    async def alarm_stopped(self) -> None:
        self.hass.log("Stopping switches...")
        for switch in self.switches:
            await self.hass.call_service(Switch.TURN_OFF, entity_id=switch)
