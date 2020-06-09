class Generic:
  ON = "on"
  OFF = "off"
  ACTIVATION_DELAY = 15
  STOP_DELAY = 180

class MediaPlayer:
  MEDIA_PLAYER_PLAY = "media_player/play_media"
  MEDIA_PLAYER_STOP = "media_player/media_stop"
  MEDIA_PLAYER_SET_VOL = "media_player/volume_set"
  MEDIA_PLAYER_CTYPE = "sound"
  MEDIA_PLAYER_VOLUME = 1
  MEDIA_PLAYER_VOLUME_LEVEL = "volume_level"

class Notifier:
  NOTIFICATION_TITLE = "ALERT! [{sensor}]"
  NOTIFICATION_MSG = "[{sensor}] Alarm has been fired!"