# -*- coding=utf-8 -*-
"""Music related slash commands."""
# import logging
# import typing

# import hikari
# import lavasnek_rs
# import tanjun

# from ottbot import config as config_
from ottbot.utils.funcs import build_loaders

music, load_component, unload_component = build_loaders()

# logger = logging.getLogger(__name__)


# class EventHandler:
#     """Handles events from the Lavalink server."""

#     async def track_start(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStart) -> None:
#         """Handles track start events."""
#         logger.info(f"Track started on guild: {event.guild_id}")

#     async def track_finish(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackFinish) -> None:
#         """Handles track finish events."""
#         logger.info(f"Track finished on guild: {event.guild_id}")

#     async def track_exception(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackException) -> None:
#         """Handles track exception events."""
#         logger.info(f"Track exception event happened on guild: {event.guild_id}")

#         # If a track was unable to be played, skip it
#         skip = await lavalink.skip(event.guild_id)
#         node = await lavalink.get_guild_node(event.guild_id)

#         if skip and node:
#             if not node.queue and not node.now_playing:
#                 await lavalink.stop(event.guild_id)


# # suggest a song name based on what the user has typed
# async def _song_autocomplete(
#     ctx: tanjun.abc.AutocompleteContext,
#     partial_word: str,
#     lavalink: lavasnek_rs.Lavalink = tanjun.inject(type=lavasnek_rs.Lavalink),
# ) -> None:
#     tracks = (await lavalink.auto_search_tracks(partial_word)).tracks
#     await ctx.set_choices({x.info.title: x.info.title for x in tracks})


# @music.with_listener(hikari.ShardReadyEvent)
# async def on_shard_ready(
#     event: hikari.ShardReadyEvent,
#     client_: tanjun.Client = tanjun.injected(type=tanjun.Client),
#     config: config_.FullConfig = tanjun.inject(type=config_.FullConfig),
# ) -> None:
#     """Event that triggers when the hikari gateway is ready."""
#     if config.lavalink_password is None:
#         return
#     builder = (
#         lavasnek_rs.LavalinkBuilder(event.my_user.id, config.tokens.bot)
#         .set_host(config.lavalink_host)
#         .set_password(config.lavalink_password)
#         .set_start_gateway(False)
#         # We set start gateway False because hikari can handle
#         # voice events for us.
#     )

#     # Here we add lavasnek_rs.Lavalink as a type dependency to the client
#     # We will use this later to have access to it in all our commands

#     client_.set_type_dependency(lavasnek_rs.Lavalink, await builder.build(EventHandler))


# @music.with_listener(hikari.VoiceStateUpdateEvent)
# async def on_voice_state_update(
#     event: hikari.VoiceStateUpdateEvent,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Passes voice state updates to lavalink."""
#     lavalink.raw_handle_event_voice_state_update(
#         event.state.guild_id,
#         event.state.user_id,
#         event.state.session_id,
#         event.state.channel_id,
#     )


# @music.with_listener(hikari.VoiceServerUpdateEvent)
# async def on_voice_server_update(
#     event: hikari.VoiceServerUpdateEvent,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Passes voice server updates to lavalink."""
#     if event.endpoint is not None:
#         await lavalink.raw_handle_event_voice_server_update(
#             event.guild_id,
#             event.endpoint,
#             event.token,
#         )


# @music.with_slash_command
# @tanjun.as_slash_command("join", "Connect the bot to a voice channel.")
# async def join_as_slash(
#     ctx: tanjun.abc.SlashContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Connect the bot to a voice channel."""
#     if channel := await _join_voice(ctx, lavalink):
#         await ctx.respond(f"Connected to <#{channel}>")


# @music.with_message_command
# @tanjun.as_message_command("join")
# async def join_as_message(
#     ctx: tanjun.abc.MessageContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Connect the bot to a voice channel."""
#     if channel := await _join_voice(ctx, lavalink):
#         await ctx.respond(f"Connected to <#{channel}>")


# async def _join_voice(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> typing.Optional[hikari.Snowflake]:
#     """Joins your voice channel."""
#     assert ctx.guild_id is not None

#     if ctx.client.cache and ctx.client.shards:
#         # Get the users voice state
#         if (voice_state := ctx.client.cache.get_voice_state(ctx.guild_id, ctx.author)) is None:
#             await ctx.respond("Please connect to a voice channel.")
#             return None

#         # Join the voice channel
#         await ctx.client.shards.update_voice_state(ctx.guild_id, voice_state.channel_id, self_deaf=True)
#         # Lavasnek waits for the data on the event
#         conn = await lavalink.wait_for_full_connection_info_insert(ctx.guild_id)
#         # Lavasnek tells lavalink to connect
#         await lavalink.create_session(conn)
#         return voice_state.channel_id

#     await ctx.respond("Unable to join voice. The cache is disabled or shards are down.")
#     return None


# @music.with_slash_command
# @tanjun.with_str_slash_option(
#     "song", "The title or youtube link of the song you want to play.", autocomplete=_song_autocomplete
# )
# @tanjun.as_slash_command("play", "Play a song, or add it to the queue.")
# async def play_as_slash(
#     ctx: tanjun.abc.SlashContext,
#     song: str,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Play a song, or add it to the queue."""
#     await _play_track(ctx, song, lavalink)


# @music.with_message_command
# @tanjun.with_greedy_argument("song")  # Set song to be greedy
# @tanjun.with_parser  # Add an argument parser to the command
# @tanjun.as_message_command("play")
# async def play_as_message(
#     ctx: tanjun.abc.MessageContext,
#     song: str,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Play a song, or add it to the queue."""
#     await _play_track(ctx, song, lavalink)


# async def _play_track(ctx: tanjun.abc.Context, song: str, lavalink: lavasnek_rs.Lavalink) -> None:
#     """Attempts to play the song from youtube."""
#     assert ctx.guild_id is not None

#     # Check if we are connected to voice
#     conn = lavalink.get_guild_gateway_connection_info(ctx.guild_id)

#     if not conn:
#         # Join the users voice channel if we are not already connected
#         if not await _join_voice(ctx, lavalink):
#             # Return out of the function if joining vc failed
#             return

#     if not (tracks := (await lavalink.auto_search_tracks(song)).tracks):
#         # We didn't find any tracks
#         await ctx.respond(f"No tracks found found song: <{song}>")
#         return

#     try:
#         # Play the first track in tracks
#         # Set the requester, and queue the song
#         await lavalink.play(ctx.guild_id, tracks[0]).requester(ctx.author.id).queue()
#     except lavasnek_rs.NoSessionPresent:
#         # Occurs if lavalink crashes
#         await ctx.respond("Unable to join voice. This may be an internal error.")
#         return

#     await ctx.respond(f"Added to queue: `{tracks[0].info.title}`")


# @music.with_slash_command
# @tanjun.as_slash_command("leave", "Leaves the voice channel and clears the queue.")
# async def leave_as_slash(
#     ctx: tanjun.abc.SlashContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Leaves the voice channel and clears the queue."""
#     await _leave_voice(ctx, lavalink)


# @music.with_message_command
# @tanjun.as_message_command("leave")
# async def leave_as_message(
#     ctx: tanjun.abc.MessageContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Leaves the voice channel and clears the queue."""
#     await _leave_voice(ctx, lavalink)


# async def _leave_voice(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> None:
#     """Stops playback of the current song."""
#     assert ctx.guild_id is not None

#     if lavalink.get_guild_gateway_connection_info(ctx.guild_id):
#         # If were connected, destroy the connection
#         await lavalink.destroy(ctx.guild_id)

#         if ctx.client.shards:
#             # Set voice channel to None
#             await ctx.client.shards.update_voice_state(ctx.guild_id, None)
#             await lavalink.wait_for_connection_info_remove(ctx.guild_id)

#         # We must manually remove the node and queue loop from lavasnek
#         await lavalink.remove_guild_node(ctx.guild_id)
#         await lavalink.remove_guild_from_loops(ctx.guild_id)

#         await ctx.respond("Disconnected from voice.")
#         return

#     await ctx.respond("I am not currently connected.")


# @music.with_slash_command
# @tanjun.as_slash_command("stop", "Stops the currently playing song, skip to play again.")
# async def stop_as_slash(
#     ctx: tanjun.abc.SlashContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Stops the currently playing song, skip to play again."""
#     await _stop_playback(ctx, lavalink)


# @music.with_message_command
# @tanjun.as_message_command("stop")
# async def stop_as_message(
#     ctx: tanjun.abc.MessageContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Stops the currently playing song, skip to play again."""
#     await _stop_playback(ctx, lavalink)


# async def _stop_playback(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> None:
#     """Stops the currently playing song."""
#     assert ctx.guild_id is not None

#     await lavalink.stop(ctx.guild_id)  # Stop the player
#     await ctx.respond("Stopped playback.")


# @music.with_slash_command
# @tanjun.as_slash_command("skip", "Skips the current song.")
# async def skip_as_slash(
#     ctx: tanjun.abc.SlashContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Skips the current song."""
#     await _skip_track(ctx, lavalink)


# @music.with_message_command
# @tanjun.as_message_command("skip")
# async def skip_as_message(
#     ctx: tanjun.abc.MessageContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Skips the current song."""
#     await _skip_track(ctx, lavalink)


# async def _skip_track(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> None:
#     """Skips the current song."""
#     assert ctx.guild_id is not None

#     if not (skip := await lavalink.skip(ctx.guild_id)):
#         await ctx.respond("No tracks left to skip.")
#         return

#     elif node := await lavalink.get_guild_node(ctx.guild_id):
#         # If we skipped and the queue is empty we need to
#         # stop the player
#         if not node.queue and not node.now_playing:
#             await lavalink.stop(ctx.guild_id)

#     await ctx.respond(f"Skipped: {skip.track.info.title}")


# @music.with_slash_command
# @tanjun.as_slash_command("pause", "Pauses the current song.")
# async def pause_as_slash(
#     ctx: tanjun.abc.SlashContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Pauses the current song."""
#     await _pause_playback(ctx, lavalink)


# @music.with_message_command
# @tanjun.as_message_command("pause")
# async def pause_as_message(
#     ctx: tanjun.abc.MessageContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Pauses the current song."""
#     await _pause_playback(ctx, lavalink)


# async def _pause_playback(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> None:
#     """Pauses the current song."""
#     assert ctx.guild_id is not None

#     await lavalink.pause(ctx.guild_id)
#     await ctx.respond("Paused playback.")


# @music.with_slash_command
# @tanjun.as_slash_command("resume", "Resumes the current song.")
# async def resume_as_slash(
#     ctx: tanjun.abc.SlashContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Resumes the current song."""
#     await _resume_playback(ctx, lavalink)


# @music.with_message_command
# @tanjun.as_message_command("resume")
# async def resume_as_message(
#     ctx: tanjun.abc.MessageContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Resumes the current song."""
#     await _resume_playback(ctx, lavalink)


# async def _resume_playback(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> None:
#     """Resumes playing the current song."""
#     assert ctx.guild_id is not None

#     await lavalink.resume(ctx.guild_id)
#     await ctx.respond("Resuming playback.")


# @music.with_slash_command
# @tanjun.as_slash_command("playing", "Displays info on the currently playing song.")
# async def playing_as_slash(
#     ctx: tanjun.abc.Context,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Displays info on the currently playing song."""
#     await _playing(ctx, lavalink)


# @music.with_message_command
# @tanjun.as_message_command("playing")
# async def playing_as_message(
#     ctx: tanjun.abc.MessageContext,
#     lavalink: lavasnek_rs.Lavalink = tanjun.injected(type=lavasnek_rs.Lavalink),
# ) -> None:
#     """Displays info on the currently playing song."""
#     await _playing(ctx, lavalink)


# async def _playing(ctx: tanjun.abc.Context, lavalink: lavasnek_rs.Lavalink) -> None:
#     """Displays info on the currently playing song."""
#     assert ctx.guild_id is not None

#     if not (node := await lavalink.get_guild_node(ctx.guild_id)):
#         # No node, means no music
#         await ctx.respond("Unable to connect to the node.")
#         return

#     if not node.now_playing:
#         # Nothing is playing
#         await ctx.respond("Nothing is playing now.")
#         return

#     if node.now_playing:
#         # Info on the current track
#         await ctx.respond(
#             f"Title: {node.now_playing.track.info.title}\n" f"Requested by: <@!{node.queue[0].requester}>"
#         )
