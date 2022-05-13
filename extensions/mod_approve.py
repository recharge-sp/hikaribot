import os

import hikari
import lightbulb

import config

plugin = lightbulb.Plugin("ArcHikari.ModApprove")
plugin.add_checks(lightbulb.guild_only, lightbulb.has_roles(*config.MOD_ROLEIDS))

@plugin.command()
@lightbulb.option("member", "欲審核之使用者", type=hikari.Member, required=True)
@lightbulb.command("approve", "審核使用者")
@lightbulb.implements(lightbulb.SlashCommand)
async def approve(ctx: lightbulb.Context) -> None:
    member = ctx.options.member
    if config.MEMBER_ROLEID not in member.role_ids:
        await member.add_role(config.MEMBER_ROLEID)
        if config.UNVERIFIED_ROLEID in member.role_ids:
            await member.remove_role(config.UNVERIFIED_ROLEID)
        await ctx.respond("已新增使用者。", flags=hikari.messages.MessageFlag.EPHEMERAL)
        channel = ctx.get_guild().get_channel(config.VERIFICATION_ANNOUNCE_CHANNELID)
        if channel:
            await channel.send(f"{member.mention} 審核已通過。", user_mentions=True)
    else:
        await ctx.respond("使用者已審核過。", flags=hikari.messages.MessageFlag.EPHEMERAL)
        
@plugin.command()
@lightbulb.option("member", "欲移除權限之使用者", type=hikari.Member, required=True)
@lightbulb.command("removeuser", "移除使用者權限")
@lightbulb.implements(lightbulb.SlashCommand)
async def removeuser(ctx: lightbulb.Context) -> None:
    member = ctx.options.member
    if config.MEMBER_ROLEID in member.role_ids:
        await member.remove_role(config.MEMBER_ROLEID)
        if not config.UNVERIFIED_ROLEID in member.role_ids:
            await member.add_role(config.UNVERIFIED_ROLEID)
        await ctx.respond("已移除使用者。", flags=hikari.messages.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond("使用者已移除。", flags=hikari.messages.MessageFlag.EPHEMERAL)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
