import nextcord
from nextcord.ext import commands
from nextcord import Forbidden, HTTPException, Interaction, NotFound
from utils import Xbox

class Blacklist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="blacklist", description="Blacklist a tag from bot")
    @commands.guild_only()
    async def authenticate_cmd(self, interaction: Interaction,
                               xuid: int = nextcord.SlashOption(name="xuid",
                                                                description="Xuid to blacklist",
                                                                required=True, min_value=1, default=30)):

        # Check if the user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        try:
            await interaction.response.defer(ephemeral=True)
        except (NotFound, Forbidden, HTTPException):
            return  # Ignore the error silently if the interaction is not found or if deferring the response fails

        do_work = await Xbox.black(xuid)
        if do_work:
            return await interaction.followup.send(
                f"Successfully Blacklisted: {xuid}")
        else:
            return await interaction.followup.send(
                "Issue Reached")
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded.")


def setup(client):
    client.add_cog(Blacklist(client))
