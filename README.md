# HOME ALARM

![GitHub release (latest by date)](https://img.shields.io/github/v/release/crserran/home-alarm?style=for-the-badge)
[![downloads-latest](https://img.shields.io/github/downloads/crserran/home-alarm/latest/total?style=for-the-badge)](http://github.com/crserran/home-alarm/releases/latest)
![GitHub Release Date](https://img.shields.io/github/release-date/crserran/home-alarm?style=for-the-badge)
[![azure-pipelines-build](https://img.shields.io/azure-devops/build/criserrano93/Home%20Alarm/1/master.svg?style=for-the-badge)](https://dev.azure.com/criserrano93/Home%20Alarm/_build/latest?definitionId=1&branchName=master)

[![community-topic](https://img.shields.io/badge/community-topic-blue?style=for-the-badge)](https://community.home-assistant.io/t/home-alarm-build-your-own-security-system-at-home/203784)

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![buy-me-a-beer](https://img.shields.io/badge/sponsor-Buy%20me%20a%20beer-orange?style=for-the-badge)](https://www.buymeacoffee.com/crserran)

_Home Alarm_ allows you to use any media player such as Alexa or Google Home to make them act as an alarm system at home. It also supports the notification system to alert you if you are not at home.

# Documentation

This security system keep listening the window and door sensors that are installed in your smart home system and the safe mode input.

If the safe mode is active and some of windows or doors are opened, the user has a few seconds to indentify himself into the system. ([see link](https://crserran.github.io/home-alarm/identification/))

If the user cannot identify himself into the system, the alarm will be fired on the media player and the user will be notified that an unathorized user has been entered to his house.

You can check the full documentation [here](https://crserran.github.io/home-alarm/)

# Example

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

# Requirements

For run successfully this application you have to take into account the following:

- At least one window/door sensor configured
- Safe Mode as an input_boolean configured in HA
- Have a media player configured in HA
- At least one notifier
