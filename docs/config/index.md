# Configuration

## Basic
This is a quick example about how to configure the application with 2 Alexas as media players, 2 window/door sensors and 1 motion sensor.

```yaml
home_alarm:
  module: home_alarm
  class: HomeAlarm
  sensors:
    - binary_sensor.livingroom_window_contact
    - binary_sensor.entrance_door_contact
    - binary_sensor.entrance_motion_occupancy
  safe_mode: input_boolean.safe_mode
  alerts:
    - id: media_player
      sound: amzn_sfx_scifi_alarm_04
      loop_delay: 4
      media_players: 
        - media_player.alexa
        - media_player.alexa2
    - id: notifier
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
    - binary_sensor.entrance_motion_occupancy
  safe_mode: input_boolean.safe_mode
  safe_mode_delay: 90
  activation_delay: 10
  stop_delay: 240
  alerts:
    - id: media_player
      sound: amzn_sfx_scifi_alarm_04
      loop_delay: 4
      volume: 0.8
      media_players: 
        - media_player.alexa
        - media_player.alexa2
    - id: notifier
      notifiers:
        - notify.mobile_app_iphone
        - notify.notifier
      title: "ALARM ALERT! {sensor}"
      message: "Alarm has been fired from {sensor} sensor"
```

!!! info "IMPORTANT NOTE"
    `sound` and `loop_delay` are linked variables. If the track specified at `sound` is too short, you will want to repeat it continuously specifying the attribute `loop_delay` as the same as the `sound` track duration.

## Attributes
### Generic
 Name | Type | Required | Default | Description
:----:|:----:|:--------:|:-------:|:-----------:
sensors | array | yes | [] | Windows and doors binary sensors.
safe_mode | string | yes |  | Safe mode input boolean. If `true` protected mode enabled, otherwise `false` protected mode disabled.
safe_mode_delay | int | no | 60 | Time the user has to leave the house after safe_mode sensor is changed to `ON` state.
activation_delay | int | no | 15 | Time that user has to be identified in the system. If user is not identified, alarm will be fired.
stop_delay | int | no | 180 | Time to stop alarm after been fired.
alerts | array | yes | [] | List of alerts (view supported alerts on the alerts section)

### Alerts

 * [Media Player Alerts](../alerts/media_player.md)
 * [Notifier Alerts](../alerts/notifier.md)

