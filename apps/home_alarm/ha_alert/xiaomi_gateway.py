from ha_core.alert import Alert
from ha_core.state import State
from ha_utils.ha_const import Generic, XiaomiGateway

class XiaomiGatewayAlert(Alert):
  alert_id = "xiaomi_gateway"

  def parse_kwargs(self, kwargs) -> None:
    self.gateways = kwargs["gw_mac"]
    self.ringtone = kwargs["ringtone_id"]
    self.volume = kwargs.get("ringtone_vol", XiaomiGateway.XIAOMI_VOLUME)
    self.loop_delay = XiaomiGateway.XIAOMI_LOOP_DELAY

  async def alarm_fired(self, sensor_fired) -> None:
    for gateway in self.gateways:
      await self.play_sound({"gateway": gateway})

  async def play_sound(self, kwargs=None):
    gateway = kwargs["gateway"]
    if self.state.fired:
      await self.hass.call_service(
        XiaomiGateway.XIAOMI_PLAY,
        gw_mac=gateway,
        ringtone_id=self.ringtone,
        ringtone_vol=self.volume
      )
      if self.loop_delay:
        await self.hass.run_in(self.play_sound, self.loop_delay, gateway = gateway)
    else:
      self.hass.log(f"Alarm has been stopped")

  async def alarm_stopped(self) -> None:
    self.hass.log("Stopping xiaomi gateways...")
    for gateway in self.gateways:
      await self.hass.call_service(
        XiaomiGateway.XIAOMI_STOP,
        gw_mac=gateway
      )
