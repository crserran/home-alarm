# Switch Alert

## Attributes

|   Name   |  Type  | Required | Default |                    Description                    |
| :------: | :----: | :------: | :-----: | :-----------------------------------------------: |
|    id    | string |   yes    |         | Switch Alert identifier, value should be `switch` |
| switches | array  |   yes    |   []    |                 List of switches.                 |

## Example

```yaml
alerts:
  - id: switch
    lights:
      - switch.bedroom
      - switch.livingroom
```
