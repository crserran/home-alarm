class Generic:
    ON = "on"
    OFF = "off"
    SAFE_MODE_DELAY = 60
    ACTIVATION_DELAY = 15
    STOP_DELAY = 180


class MediaPlayer:
    PLAY = "media_player/play_media"
    STOP = "media_player/media_stop"
    SET_VOL = "media_player/volume_set"
    CTYPE = "sound"
    VOLUME = 1
    DEFAULT_INIT_VOLUME = 0.5
    VOLUME_LEVEL = "volume_level"


class Notifier:
    TITLE = "ALERT! [{sensor}]"
    MSG = "[{sensor}] Alarm has been fired!"


class XiaomiGateway:
    PLAY = "xiaomi_aqara/play_ringtone"
    STOP = "xiaomi_aqara/stop_ringtone"
    VOLUME = 100
    LOOP_DELAY = 8


class Light:
    TOGGLE = "light/toggle"
    TURN_ON = "light/turn_on"
    TURN_OFF = "light/turn_off"
    COLOR = [255, 0, 0]
    BRIGHTNESS = 255


class Switch:
    TURN_ON = "switch/turn_on"
    TURN_OFF = "switch/turn_off"
