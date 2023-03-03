from ha_core.alert import Alert
from ha_core.state import State
from ha_utils.ha_const import Generic, MediaPlayer


class MediaPlayerAlert(Alert):
    alert_id = "media_player"

    def parse_kwargs(self, kwargs) -> None:
        self.media_players = kwargs["media_players"]
        self.sound = kwargs["sound"]
        self.volume = kwargs.get("volume", MediaPlayer.VOLUME)
        self.default_init_volume = kwargs.get(
            "default_init_volume", MediaPlayer.DEFAULT_INIT_VOLUME
        )
        self.loop_delay = kwargs.get("loop_delay", None)
        # Initial state of media players
        self.init_state = dict()

    async def alarm_fired(self, sensor_fired) -> None:
        self.init_state = await self.get_init_state()
        await self.hass.call_service(
            MediaPlayer.SET_VOL, entity_id=self.media_players, volume_level=self.volume
        )
        await self.play_sound()

    async def play_sound(self, kwargs=None):
        if self.state.fired:
            await self.hass.call_service(
                MediaPlayer.PLAY,
                entity_id=self.media_players,
                media_content_id=self.sound,
                media_content_type=MediaPlayer.CTYPE,
            )
            if self.loop_delay:
                await self.hass.run_in(self.play_sound, self.loop_delay)
        else:
            self.hass.log(f"Alarm has been stopped")

    async def alarm_stopped(self) -> None:
        self.hass.log("Stopping media services...")
        await self.hass.call_service(MediaPlayer.STOP, entity_id=self.media_players)
        await self.set_init_state()

    async def get_init_state(self) -> dict:
        state = dict()
        for media_player in self.media_players:
            volume = await self.hass.get_state(media_player, MediaPlayer.VOLUME_LEVEL)
            state[media_player] = (
                volume if volume is not None else self.default_init_volume
            )
        return state

    async def set_init_state(self):
        for media_player in self.media_players:
            await self.hass.call_service(
                MediaPlayer.SET_VOL,
                entity_id=media_player,
                volume_level=self.init_state[media_player],
            )
