import appdaemon.plugins.hass.hassapi as hass
from typing import List
from ha_core.state import State
from ha_core.alert import Alert, AlertList
from ha_alert import get_alerts
from ha_alert.log_alert import LogAlert
from ha_utils.const import Generic

class HomeAlarm(hass.Hass):

  async def initialize(self) -> None: 
    self.log("Welcome to Home Alarm security system.")

    # Home Alarm config parameters
    self.sensors = self.args["sensors"]
    self.safe_mode = self.args["safe_mode"]
    self.activation_delay = self.args.get("activation_delay", Generic.ACTIVATION_DELAY)
    self.stop_delay = self.args.get("stop_delay", Generic.STOP_DELAY)

    # Home Alarm attributes
    self.state = State()
    alert_configs = self.args["alerts"]
    alert_list = self.parse_alerts(alert_configs)
    self.alerts = AlertList(alert_list)
    self.sensor_fired = None

    self.listen_state(self.disarm_alarm, self.safe_mode, new=Generic.OFF)
    for sensor in self.sensors:
      self.listen_state(self.door_opened_cb, sensor, new=Generic.ON)

  async def door_opened_cb(self, sensor, attribute, old, new, kwargs):  
    self.sensor_fired = sensor
    safe_mode_state = await self.get_state(self.safe_mode)
    self.log("A door or window has been opened")
    self.log(f"`safe_mode` state: {safe_mode_state}")
    if (safe_mode_state == Generic.ON
        and not self.state.ready_to_fire
        and not self.state.fired):
      self.state.ready_to_fire = True
      self.run_in(self.countdown, self.activation_delay)

  async def countdown(self, kwargs):
    safe_mode_state = await self.get_state(self.safe_mode)
    if safe_mode_state == Generic.ON:
      self.log("The alarm has been triggered")
      self.state.fired = True
      # Alarm fired action
      self.alerts.alarm_fired(self.sensor_fired)
      # Alarm stop action after stop_delay
      self.run_in(self.stop_alarm, self.stop_delay) 
    self.state.ready_to_fire = False

  async def stop_alarm(self, kwargs=None):
    self.alerts.alarm_stopped()
    self.state.fired = False
    self.state.stopped = True

  async def disarm_alarm(self, safe_mode, attribute, old, new, kwargs=None):
    if self.state.fired:
      self.log("Alarm has been disarmed")
      self.stop_alarm()

  def parse_alerts(self, alert_configs: List[dict]) -> List[Alert]:
    """
    Required:
      - id
    """
    alerts = []
    alerts_dict = get_alerts()
    for alert_config in alert_configs:
      alert_cls = alerts_dict.get(alert_config["id"])
      alerts.append(alert_cls(self.state, self, alert_config))
    return alerts