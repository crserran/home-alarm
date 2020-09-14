# Media Player Alert

## Attributes

|     Name      |  Type  | Required | Default |                                                                                                      Description                                                                                                      |
| :-----------: | :----: | :------: | :-----: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|      id       | string |   yes    |         |                                                                             Media Player Alert identifier, value should be `media_player`                                                                             |
| media_players | array  |   yes    |   []    |                                                                                  Media player devices to reproduce the alarm sound.                                                                                   |
|     sound     | string |   yes    |         | If Alexa get the name of sound from [here](https://developer.amazon.com/es-ES/docs/alexa/custom-skills/ask-soundlibrary.html#available-sounds), otherwise other media players specify the full path of the mp3 track. |
|  loop_delay   |  int   |    no    |  None   |                                                          Time to reproduce again `sound` attribute. If `sound` duration is 4secs, `loop_delay` has to be 4.                                                           |
|    volume     | float  |    no    |    1    |                                                                                   Volume to reproduce the alarm sound. From 0 to 1.                                                                                   |
