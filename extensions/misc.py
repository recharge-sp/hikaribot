import os

import hikari
import lightbulb

import config

plugin = lightbulb.Plugin("ArcHikari.Misc")
plugin.add_checks(lightbulb.guild_only)

@plugin.command()
@lightbulb.option("score", "成績", type=int, required=True)
@lightbulb.option("chart_constant", "譜面定數", type=float, required=True)
@lightbulb.command("calcpotential", "計算潛力值")
@lightbulb.implements(lightbulb.SlashCommand)
async def calcpotential(ctx: lightbulb.Context) -> None:
    chart_constant = ctx.options.chart_constant
    score = ctx.options.score
    potential = 0
    if score >= 10000000:
        potential = chart_constant + 2.0
    elif score >= 9800000:
        potential = chart_constant + 1.0 + (score - 9800000)/200000
    elif score < 9800000:
        potential = chart_constant + (score - 9500000)/300000
        if potential < 0: potential = 0
    await ctx.respond(f"結果：{potential:.2f}", flags=hikari.messages.MessageFlag.EPHEMERAL)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
