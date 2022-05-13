import os

import hikari
import lightbulb

import config


bot = lightbulb.BotApp(token=config.BOT_TOKEN, default_enabled_guilds=config.BOT_GUILDS)
bot.load_extensions_from("extensions")

@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"執行`{event.context.command.name}`指令時發生錯誤，請回報給recharge-sp。", flags=hikari.messages.MessageFlag.EPHEMERAL)
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.MissingRequiredRole):
        await event.context.respond("你無此權限。", flags=hikari.messages.MessageFlag.EPHEMERAL)
    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("你不是我的主人。", flags=hikari.messages.MessageFlag.EPHEMERAL)
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"此指令正在冷卻，請在`{exception.retry_after:.2f}`秒後重試。", flags=hikari.messages.MessageFlag.EPHEMERAL)
    else:
        raise exception


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()
