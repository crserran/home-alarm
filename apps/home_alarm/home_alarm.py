import hassapi as hass

class HomeAlarm(hass.Hass):

  def initialize(self) -> None: 
    self.log("Welcome to Home Alarm security system.")
    self.sensors = self.args["sensors"]
    self.safe_mode = self.args["safe_mode"]
    self.media_player = self.args["media_player"]
    self.sound = self.args["sound"]
    self.notifiers = self.get_notifiers(self.args["notifiers"])
    self.activation_delay = self.args.get("activation_delay", 15)
    self.loop_delay = self.args.get("loop_delay", 3)
    self.stop_delay = self.args.get("stop_delay", 120)
    self.title = self.args.get("alert_title", "ALERT!")
    self.alert_msg = self.args.get("alert_msg", "Alarm has been fired!")
    self.alarm_is_running = False
    self.alarm_is_about_to_run = False # Alarm is triggered. Avoid multiple calls to countdown function
    self.sensor_fired_name = ""

    self.listen_state(self.disarm_alarm, self.safe_mode, new="off")
    for sensor in self.sensors:
      self.listen_state(self.door_opened_cb, sensor, new="on")

  def door_opened_cb(self, sensor, attribute, old, new, kwargs):  
    self.sensor_fired_name = self.friendly_name(sensor)
    safe_mode_state = self.get_state(self.safe_mode)
    self.log("A door or window has been opened")
    self.log(f"`alarm_is_about_to_run`: {self.alarm_is_about_to_run}")
    self.log(f"`alarm_is_running`: {self.alarm_is_running}")
    self.log(f"`safe_mode` state: {safe_mode_state}")
    if (safe_mode_state == "on" 
        and not self.alarm_is_about_to_run
        and not self.alarm_is_running):
      self.alarm_is_about_to_run = True
      self.run_in(self.countdown, self.activation_delay)

  def countdown(self, kwargs):
    safe_mode_state = self.get_state(self.safe_mode)
    if safe_mode_state == "on":
      self.call_service(
        "media_player/volume_set", 
        entity_id=self.media_player,
        volume_level=1
      )
      self.log("The alarm has been triggered")
      self.alarm_is_running = True
      self.fire_alarm()
      # Notify users
      for notifier in self.notifiers:
        self.call_service(
          notifier, 
          title=self.title + " [" + self.sensor_fired_name + "]",
          message="[" + self.sensor_fired_name + "]. " + self.alert_msg
        )
      self.run_in(self.stop_alarm, self.stop_delay) 
    self.alarm_is_about_to_run = False

  def fire_alarm(self, kwargs=None):
    if self.alarm_is_running:
      self.call_service(
        "media_player/play_media",
        entity_id=self.media_player,
        media_content_id=self.sound,
        media_content_type="sound"
      )
      self.run_in(self.fire_alarm, self.loop_delay)
    else:
      self.log("The alarm has been stopped")

  def stop_alarm(self, kwargs=None):
    self.alarm_is_running = False

  def disarm_alarm(self, safe_mode, attribute, old, new, kwargs=None):
    self.log("Alarm has been disarmed")
    if self.alarm_is_running:
      self.alarm_is_running = False

  def get_notifiers(self, notifiers):
    return [n.replace('.', '/') for n in notifiers]