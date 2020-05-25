# Configuration

## Basic
This is a quick example about how to configure the application with Alexa as media player and 2 window/door sensors.

```yaml
home_alarm:
  module: home_alarm
  class: HomeAlarm
  sensors:
    - binary_sensor.livingroom_window_contact
    - binary_sensor.entrance_door_contact
  safe_mode: input_boolean.safe_mode
  sound: amzn_sfx_scifi_alarm_04
  media_player: media_player.alexa
  notifiers:
    - notify.mobile_app_iphone
    - notify.notifier
```

## Advanced
Example of an advanced configuration. I recommend to take a look `Attributes` section.

```yaml
home_alarm:
  module: home_alarm
  class: HomeAlarm
  sensors:
    - binary_sensor.livingroom_window_contact
    - binary_sensor.entrance_door_contact
  safe_mode: input_boolean.safe_mode
  activation_delay: 10
  media_player: media_player.alexa
  sound: amzn_sfx_scifi_alarm_04
  loop_delay: 4
  stop_delay: 240
  notifiers:
    - notify.mobile_app_iphone
    - notify.notifier
  alert_title: "ALARM ALERT!"
  alert_msg: "Alarm has been fired"
```

💡 ** IMPORTANT NOTE **

`sound` and `loop_delay` are linked variables. If the track specified at `sound` is too short, you will want to repeat it continuously specifying the attribute `loop_delay` as the same as the `sound` track duration.

## Attributes
 Name | Type | Required | Default | Description
:----:|:----:|:--------:|:-------:|:-----------:
sensors | array | yes | [] | Windows and doors binary sensors.
safe_mode | string | yes |  | Safe mode input boolean. If `true` protected mode enabled, otherwise `false` protected mode disabled.
media_player | string | yes |  | Media player device to reproduce the alarm sound.
sound | string | yes |  | If Alexa name of sound from [here](https://developer.amazon.com/es-ES/docs/alexa/custom-skills/ask-soundlibrary.html#available-sounds), otherwise other media players specify the full path of the mp3 track.
loop_delay | int | no | None | Time to reproduce again `sound` attribute. If `sound` duration is 4secs, `loop_delay` has to be 4.
stop_delay | int | no | 180 | Time to stop alarm after been fired.
activation_delay | int | no | 15 | Time that user has to be identified in the system. If user is not identified, alarm will be fired.
notifiers | array | yes | [] | List of notifiers to inform the incident detected.
alert_title | string | no | "ALERT!" | Customize the title of the notification
alert_msg | string | no | "Alarm has been fired!" | Customize the message of the notification


