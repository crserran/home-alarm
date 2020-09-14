# Light Alert

## Attributes

|  Name  |  Type  | Required | Default |                   Description                   |
| :----: | :----: | :------: | :-----: | :---------------------------------------------: |
|   id   | string |   yes    |         | Light Alert identifier, value should be `light` |
| lights | array  |   yes    |   []    |                 List of lights.                 |

## Example

```yaml
alerts:
  - id: light
    lights:
      - light.livingroom
      - light.bedroom
```
