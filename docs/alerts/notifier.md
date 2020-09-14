# Notifier Alert

## Attributes

|   Name    |  Type  | Required |              Default               |                      Description                      |
| :-------: | :----: | :------: | :--------------------------------: | :---------------------------------------------------: |
|    id     | string |   yes    |                                    | Notifier Alert identifier, value should be `notifier` |
| notifiers | array  |   yes    |                 []                 |         List of notifiers to send the alert.          |
|   title   | string |    no    |        "ALERT! [{sensor}]"         |        Customize the title of the notification        |
|  message  | string |    no    | "[{sensor}] Alarm has been fired!" |      Customize the message of the notification.       |

!!! tip
For `title` and `message` you can write `{sensor}` inside the string in order to know what sensor has been fired.
