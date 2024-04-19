import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from utils import Authentication

class Check(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="check", description="Allows you to check your subscription length.")
    @commands.guild_only()
    async def check_cmd(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)

        if not Authentication.checkSubscription(interaction.user.id):
            roles = interaction.guild.get_member(interaction.user.id).roles
            for role in roles:
                if role.id in [1082053868545921055, 1082054748485726228, 1082055104678613014, 1082055935347937422, 1082056189480812564, 1092094332036714616, 1082069003897421824]:
                    roles.remove(role)

            await interaction.user.edit(roles=roles)
            return await interaction.followup.send(f"Your subscription has expired. Please purchase another one.")
        
        return await interaction.followup.send(f"Your subscription expires at {Authentication.getSubscription(interaction.user.id)}.")
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded.")
        
def setup(client):
    client.add_cog(Check(client))