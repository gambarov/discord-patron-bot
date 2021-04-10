import discord, re, logging
from discord.ext import commands
from utils.helper import get_discord_color, get_error_embed

logger = logging.getLogger(__name__)

class InfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name = "инфа", help = "информация по тому или иному объекту")
    async def execute(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.me(ctx)

    @execute.command(name = "юзер", help = "информация о пользователе")
    async def me(self, ctx, name = ''):
        if name != '':
            if ctx.guild is None:
                return await ctx.send(embed = discord.Embed(description = "Пользователь должен быть на одном сервере с Вами", colour = get_discord_color('error')))
            name = re.sub('[<@!>]', '', name)
            try:
                user = ctx.guild.get_member(int(name))
            except:
                user = ctx.guild.get_member_named(name)
            if user is None:
                return await ctx.send(embed = get_error_embed(desc = "Пользователь '{}' не найден".format(name)))
        else:
            user = ctx.author

        embed = discord.Embed(title = "{}#{}".format(user.name, user.discriminator), colour = user.colour, description = "<@!{}>".format(user.id))
        embed.set_thumbnail(url = user.avatar_url)
        embed.add_field(
            name = "Created:",
            value = user.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        )
        embed.set_footer(text = "ID: {}".format(user.id))
        embed = self.add_member_info(user, embed)
        await ctx.send(embed = embed)

    @execute.command(name = "сервер", help = "информация о сервере")
    async def guild(self, ctx):
        guild = ctx.guild
        if ctx.guild is None:
            return await ctx.send(discord.Embed(description = "Вы должны находиться на сервере", colour = get_discord_color('error')))
        embed = discord.Embed(title = guild.name, description = guild.description, colour = get_discord_color('info'))
        embed.add_field(name = "Owner:", value = "<@!{}>".format(guild.owner.id))
        embed.add_field(name = "Members:", value = int(guild.member_count))
        embed.set_thumbnail(url = guild.icon_url)
        embed.set_footer(text = "ID: {}".format(guild.id))
        return await ctx.send(embed = embed)

    async def cog_command_error(self, ctx, error):
        logger.exception(error)
        await ctx.send(embed = get_error_embed(desc = "Не удалось получить информацию"))

    def add_member_info(self, member, embed):
        if not isinstance(member, discord.Member):
            return embed
        embed.add_field(
            name = "Joined:",
            value = member.joined_at.strftime("%m/%d/%Y, %H:%M:%S")
        )
        if len(member.roles) > 1:
            field_value = ""
            for role in member.roles:
                if role.name == "@everyone": 
                    continue
                field_value += (role.mention)
                if role is not member.roles[-1]:
                    field_value += ', '
            embed.add_field(name = "Roles ({}):".format(len(member.roles) - 1), value = field_value, inline = False)
        return embed

def setup(bot):
    bot.add_cog(InfoCommand(bot))