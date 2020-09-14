Google Home and others media players have the ability to play mp3 tracks from internet or locally. That's because you have to adapt the `apps.yaml` configuration to make that working properly.

I recommend to follow the next steps in order to have app well configured.

Find a track with `mp3` extension from the internet or use one localy. Copy & paste the url to the `sound` attribute.

Figure out at the track duration and fit the `loop_delay` attribute with the track duration. You can skip this step if your track is greater than `stop_delay`.
