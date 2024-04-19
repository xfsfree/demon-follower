import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from utils import Authentication
from nextcord import Interaction, NotFound, Forbidden, HTTPException


class Upload(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="upload", description="Allows you to upload new tokens.")
    @commands.guild_only()
    async def upload_cmd(self, interaction: Interaction, tokens: nextcord.Attachment):
        # Check if the user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        try:
            await interaction.response.defer(ephemeral=True)
        except (NotFound, Forbidden, HTTPException):
            return  # Ignore the error silently if the interaction is not found or if deferring the response fails

        if not tokens.filename.endswith('.txt'):
            return await interaction.followup.send("Invalid file type. Please upload a .txt file.")

        if tokens == None or tokens == "":
            return await interaction.followup.send("Please upload a .txt file.")

        if await tokens.save("data/tokens.txt"):
            return await interaction.followup.send("Tokens uploaded.")
        else:
            return await interaction.followup.send("An error occurred while uploading the tokens.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded.")


def setup(client):
    client.add_cog(Upload(client))
