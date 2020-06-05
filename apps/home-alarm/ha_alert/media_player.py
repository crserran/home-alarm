from ha_core.alert import Alert
from ha_core.state import State
from ha_utils.const import Generic, MediaPlayer

class MediaPlayerAlert(Alert):
  alert_id = "media_player"

  def parse_kwargs(self, kwargs) -> None:
    self.media_players = kwargs["media_players"]
    self.sound = kwargs["sound"]
    self.volume = kwargs.get("volume", MediaPlayer.MEDIA_PLAYER_VOLUME)
    self.loop_delay = kwargs.get("loop_delay", None)

  async def alarm_fired(self, sensor_fired) -> None:
    for media_player in self.media_players:
      await self.hass.call_service(
        MediaPlayer.MEDIA_PLAYER_SET_VOL, 
        entity_id=media_player,
        volume_level=self.volume
      )
      kwargs = { "media_player": media_player }
      await self.play_sound(kwargs)

  async def play_sound(self, kwargs):
    media_player = kwargs["media_player"]
    if self.state.fired:
      await self.hass.call_service(
        MediaPlayer.MEDIA_PLAYER_PLAY,
        entity_id=media_player,
        media_content_id=self.sound,
        media_content_type=MediaPlayer.MEDIA_PLAYER_CTYPE
      )
      if self.loop_delay:
        await self.hass.run_in(self.play_sound, self.loop_delay, media_player = media_player)
    else:
      self.hass.log(f"Alarm from {media_player} has been stopped")

  async def alarm_stopped(self) -> None:
    self.hass.log("Stopping media services...")
    for media_player in self.media_players:
      await self.hass.call_service(
        MediaPlayer.MEDIA_PLAYER_STOP,
        entity_id=media_player
      )