import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from utils import Authentication, Xbox


class Party(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="party", description="Allows you to spam a user with party invites")
    @commands.guild_only()
    async def party_cmd(self, interaction: Interaction, xuid: str):
        # Check if the user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        for token in Xbox.getTokens():
            await Xbox.sendParty(token, xuid)


def setup(client):
    client.add_cog(Party(client))
