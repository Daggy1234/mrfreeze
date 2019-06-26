import discord

def setup(bot):
    bot.add_cog(DeparturesCog(bot))

class DeparturesCog(discord.ext.commands.Cog, name='Departures'):
    """How the bot acts when members leave the chat."""
    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.Cog.listener()
    async def on_member_remove(self, member):
        mod_channel = discord.utils.get(member.guild.channels, name='mod-discussion')

        embed = discord.Embed(color=0x00dee9)
        embed.set_thumbnail(url=member.avatar_url_as(static_format="png"))
        embed.add_field(
            name=f"{member.name}#{member.discriminator} has left the server! :sob:",
            value=(
                f"{member.mention} is a smudgerous trech " +
                f"who's turned their back on {member.guild.name}.\n" +
                f"We now have only {len(member.guild.members)} members."
            )
        )

        await mod_channel.send(embed=embed)