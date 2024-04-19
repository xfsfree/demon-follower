import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.embeds import Embed
from utils import Authentication


class UnAuthenticate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="unauthenticate", description="Allows you to unauthenticate a user")
    @commands.guild_only()
    async def unauthenticate_cmd(self, interaction: Interaction,
                                 user: nextcord.Member = nextcord.SlashOption(name="user",
                                                                              description="The user you'd like to remove.",
                                                                              required=True)):
        # Check if the user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        remove = Authentication.removeSubscription(user.id)
        if remove:
            return await interaction.followup.send(f"Successfully removed <@!{user.id}> from the database.")
        else:
            return await interaction.followup.send(f"Failed to remove <@!{user.id}> from the database.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded.")


def setup(client):
    client.add_cog(UnAuthenticate(client))
