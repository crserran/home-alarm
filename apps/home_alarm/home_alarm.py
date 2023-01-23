import appdaemon.plugins.hass.hassapi as hass
from typing import List
from ha_core.state import State
from ha_core.alert import Alert, AlertList
from ha_alert import get_alerts
from ha_utils.ha_const import Generic
import ha_version


class HomeAlarm(hass.Hass):
    async def initialize(self) -> None:
        self.log(
            f"🚨 Home Alarm security system {ha_version.__version__}",
            ascii_encode=False,
        )

        # Home Alarm config parameters
        self.sensors = self.args["sensors"]
        self.safe_mode = self.args["safe_mode"]
        self.safe_mode_delay = self.args.get("safe_mode_delay", Generic.SAFE_MODE_DELAY)
        self.activation_delay = self.args.get(
            "activation_delay", Generic.ACTIVATION_DELAY
        )
        self.stop_delay = self.args.get("stop_delay", Generic.STOP_DELAY)

        # Home Alarm attributes
        self.state = State()
        alert_configs = self.args["alerts"]
        alert_list = self.parse_alerts(alert_configs)
        self.alerts = AlertList(alert_list)
        # Safe Mode initialization
        self.safe_mode_active = await self.get_state(self.safe_mode) == Generic.ON
        # Sensor that fires alarm
        self.sensor_fired = None
        # Handler functions
        self.handle_countdown_fired = None
        self.handle_stop_alarm = None
        self.handle_activate_safe_mode = None

        self.listen_state(self.safe_mode_cb, self.safe_mode)
        for sensor in self.sensors:
            self.listen_state(
                self.door_opened_cb, sensor, new=Generic.ON, old=Generic.OFF
            )

    async def safe_mode_cb(self, sensor, attribute, old, new, kwargs):
        if new == Generic.ON:
            self.handle_activate_safe_mode = await self.run_in(
                self.activate_safe_mode, self.safe_mode_delay
            )
        elif new == Generic.OFF:
            await self.run_in(self.disarm_alarm, 0)

    async def door_opened_cb(self, sensor, attribute, old, new, kwargs):
        self.sensor_fired = sensor
        sensor_fired_name = await self.friendly_name(self.sensor_fired)
        self.log(f"{sensor_fired_name} activated")
        self.log(f"`safe_mode_active` state: {self.safe_mode_active}")
        await self.reset_stop_alarm()
        if (
            self.safe_mode_active
            and not self.state.ready_to_fire
            and not self.state.fired
        ):
            self.state.set_ready_to_fire()
            self.handle_countdown_fired = await self.run_in(
                self.countdown, self.activation_delay
            )

    async def countdown(self, kwargs):
        if self.safe_mode_active:
            self.log("The alarm has been triggered")
            self.state.set_fired()
            # Alarm fired action
            self.alerts.alarm_fired(self.sensor_fired)
            # Alarm stop action after stop_delay
            self.handle_stop_alarm = await self.run_in(self.stop_alarm, self.stop_delay)

    async def cancel_timer(self, handle):
        if handle is not None and await self.timer_running(handle):
            await super().cancel_timer(handle)

    async def stop_alarm(self, kwargs=None):
        self.state.set_stopped()
        self.alerts.alarm_stopped()
        await self.cancel_timer(self.handle_stop_alarm)

    async def disarm_alarm(self, kwargs=None):
        if self.state.fired:
            self.log("Alarm has been disarmed")
            await self.stop_alarm()
        else:
            self.log("Safe mode deactivated")
            self.state.set_stopped()

        self.safe_mode_active = False

        await self.cancel_timer(self.handle_countdown_fired)
        await self.cancel_timer(self.handle_activate_safe_mode)

    async def reset_stop_alarm(self):
        if self.state.fired:
            self.log("Reset stop alarm timer")
            await self.cancel_timer(self.handle_stop_alarm)
            self.handle_stop_alarm = await self.run_in(self.stop_alarm, self.stop_delay)

    async def activate_safe_mode(self, kwargs):
        self.log("Safe mode activated")
        self.safe_mode_active = True

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
