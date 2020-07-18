from ha_core.alert import Alert
from ha_core.state import State
from ha_utils.ha_const import Generic, XiaomiGateway


class XiaomiGatewayAlert(Alert):
    alert_id = "xiaomi_gateway"

    def parse_kwargs(self, kwargs) -> None:
        self.gateways = kwargs["gw_mac"]
        self.ringtone = kwargs["ringtone_id"]
        self.volume = kwargs.get("ringtone_vol", XiaomiGateway.VOLUME)

    async def alarm_fired(self, sensor_fired) -> None:
        for gateway in self.gateways:
            await self.play_sound({"gateway": gateway})

    async def play_sound(self, kwargs=None):
        gateway = kwargs["gateway"]
        if self.state.fired:
            await self.hass.call_service(
                XiaomiGateway.PLAY,
                gw_mac=gateway,
                ringtone_id=self.ringtone,
                ringtone_vol=self.volume,
            )
            await self.hass.run_in(
                self.play_sound, XiaomiGateway.LOOP_DELAY, gateway=gateway
            )
        else:
            self.hass.log(f"Alarm from {gateway} has been stopped")

    async def alarm_stopped(self) -> None:
        self.hass.log("Stopping xiaomi gateways...")
        for gateway in self.gateways:
            await self.hass.call_service(XiaomiGateway.STOP, gw_mac=gateway)
