# Xiaomi Gateway Alert

## Attributes

|     Name     |  Type  | Required | Default |                                                  Description                                                  |
| :----------: | :----: | :------: | :-----: | :-----------------------------------------------------------------------------------------------------------: |
|      id      | string |   yes    |         |                       Xiaomi Gateway Alert identifier, value should be `xiaomi_gateway`                       |
|    gw_mac    | array  |   yes    |   []    |                                    List of Xiaomi Gateways mac addresses.                                     |
| ringtone_id  |  int   |   yes    |         | Check the available ringtones from [here](https://www.home-assistant.io/integrations/xiaomi_aqara/#services). |
| ringtone_vol |  int   |    no    |   100   |                                   Volume of xiaomi gateway. From 0 to 100.                                    |

## Example

```yaml
alerts:
  - id: xiaomi_gateway
    gw_mac:
      - xxxxxxxxxxxx
      - yyyyyyyyyyyy
    ringtone_id: 2
    ringtone_vol: 100
```
