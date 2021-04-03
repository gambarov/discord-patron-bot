import json
import discord, aiohttp, logging
from discord.ext import commands
from utils.helper import get_discord_color, get_error_embed

logger = logging.getLogger('discord')

class LeakCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "leak", help = "leak")
    @commands.check_any(commands.is_owner())
    async def execute(self, ctx, phone: str):
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://htmlweb.ru/geo/api.php?json&telcod=" + phone) as response:
                    if response.status != 200:
                        logger.exception(await response.read())
                        return await ctx.send(embed = get_error_embed(desc = "Не удалось получить данные"))
                    data = json.loads(await response.read())
                    embed = discord.Embed(title = "🔎 Результаты поиска", colour = get_discord_color('info'))
                    
                    if 'country' in data:
                        country = data['country']
                        embed.add_field(name = "Страна", value = "{}, {}".format(country['name'], country['location']), inline = False)

                    if 'region' in data:
                        country = data['region']
                        embed.add_field(name = "Регион", value = "{}, {}".format(country['name'], country['okrug']), inline = False)

                    if '0' in data:
                        general = data['0']
                        embed.add_field(name = "Оператор", value = general['oper'], inline = False)
                        embed.add_field(name = "Город", value = general['name'], inline = False)

                    await ctx.send(embed = embed)

    @execute.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed = get_error_embed(desc = "Не указан номер"))
        if isinstance(error, commands.CheckFailure):
            return await ctx.send(embed = discord.Embed(title = "⛔ Доступ ограничен", description = "Команда доступна только для владельца", colour = get_discord_color('error')))
        logger.exception(error)
        await ctx.send(embed = get_error_embed(desc = "Не удалось получить данные"))

def setup(bot):
    bot.add_cog(LeakCommand(bot))