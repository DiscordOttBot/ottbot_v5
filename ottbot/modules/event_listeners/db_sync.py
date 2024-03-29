# -*- coding: utf-8 -*-
"""Sync the database on shard ready and guild create events."""

import logging

import hikari
import tanjun

from ottbot.db import AsyncPGDatabase
from ottbot.utils.funcs import build_loaders

component, load_component, unload_component = build_loaders()

logger = logging.getLogger(__name__)


@component.with_listener(hikari.ShardReadyEvent)
async def lsnr_shard_ready_sync_db(
    event: hikari.ShardReadyEvent, db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase)
) -> None:
    """Shard ready event listener."""
    guilds = await event.app.rest.fetch_my_guilds()

    for guild in guilds:
        await db.execute("INSERT INTO guild_config (guild_id) VALUES ($1) ON CONFLICT DO NOTHING", guild.id)


@component.with_listener(hikari.GuildJoinEvent)
async def lsnr_new_guild_sync_db(
    event: hikari.GuildJoinEvent, db: AsyncPGDatabase = tanjun.inject(type=AsyncPGDatabase)
) -> None:
    """Add new guild to db when the bot joins."""
    await db.execute("INSERT INTO guild_config (guild_id) VALUES ($1) ON CONFLICT DO NOTHING", event.guild.id)
