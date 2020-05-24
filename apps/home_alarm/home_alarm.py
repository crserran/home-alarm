import hassapi as hass


class HomeAlarm(hass.Hass):
  MEDIA_PLAYER_PLAY = "media_player/play_media"
  MEDIA_PLAYER_STOP = "media_player/media_stop"
  MEDIA_PLAYER_SET_VOL = "media_player/volume_set"
  MEDIA_PLAYER_CTYPE = "sound"
  MEDIA_PLAYER_VOLUME = 0.1
  ACTIVATION_DELAY = 15
  STOP_DELAY = 180
  NOTIFICATION_TITLE = "ALERT!"
  NOTIFICATION_MSG = "Alarm has been fired!"
  ON = "on"
  OFF = "off"

  def initialize(self) -> None: 
    self.log("Welcome to Home Alarm security system.")
    self.sensors = self.args["sensors"]
    self.safe_mode = self.args["safe_mode"]
    self.media_player = self.args["media_player"]
    self.sound = self.args["sound"]
    self.notifiers = self.get_notifiers(self.args["notifiers"])
    self.activation_delay = self.args.get("activation_delay", self.ACTIVATION_DELAY)
    self.loop_delay = self.args.get("loop_delay", None)
    self.stop_delay = self.args.get("stop_delay", self.STOP_DELAY)
    self.title = self.args.get("alert_title", self.NOTIFICATION_TITLE)
    self.alert_msg = self.args.get("alert_msg", self.NOTIFICATION_MSG)
    self.alarm_is_running = False
    self.alarm_is_about_to_run = False # Alarm is triggered. Avoid multiple calls to countdown function
    self.sensor_fired_name = ""

    self.listen_state(self.disarm_alarm, self.safe_mode, new=self.OFF)
    for sensor in self.sensors:
      self.listen_state(self.door_opened_cb, sensor, new=self.ON)

  def door_opened_cb(self, sensor, attribute, old, new, kwargs):  
    self.sensor_fired_name = self.friendly_name(sensor)
    safe_mode_state = self.get_state(self.safe_mode)
    self.log("A door or window has been opened")
    self.log(f"`alarm_is_about_to_run`: {self.alarm_is_about_to_run}")
    self.log(f"`alarm_is_running`: {self.alarm_is_running}")
    self.log(f"`safe_mode` state: {safe_mode_state}")
    if (safe_mode_state == self.ON
        and not self.alarm_is_about_to_run
        and not self.alarm_is_running):
      self.alarm_is_about_to_run = True
      self.run_in(self.countdown, self.activation_delay)

  def countdown(self, kwargs):
    safe_mode_state = self.get_state(self.safe_mode)
    if safe_mode_state == self.ON:
      self.call_service(
        self.MEDIA_PLAYER_SET_VOL, 
        entity_id=self.media_player,
        volume_level=self.MEDIA_PLAYER_VOLUME
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
        self.MEDIA_PLAYER_PLAY,
        entity_id=self.media_player,
        media_content_id=self.sound,
        media_content_type=self.MEDIA_PLAYER_CTYPE
      )
      if self.loop_delay:
        self.run_in(self.fire_alarm, self.loop_delay)
    else:
      self.log("The alarm has been stopped")

  def stop_alarm(self, kwargs=None):
    self.stop_media_service()

  def disarm_alarm(self, safe_mode, attribute, old, new, kwargs=None):
    if self.alarm_is_running:
      self.log("Alarm has been disarmed")
      self.stop_media_service()

  def stop_media_service(self):
    self.log("Stopping media service...")
    self.call_service(
      self.MEDIA_PLAYER_STOP,
      entity_id=self.media_player
    )
    self.alarm_is_running = False

  def get_notifiers(self, notifiers):
    return [n.replace('.', '/') for n in notifiers]