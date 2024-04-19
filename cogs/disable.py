import json, nextcord
from nextcord.ext import commands
from nextcord import Interaction


class Disable(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="status", description="Changes the status of the bot.")
    @commands.guild_only()
    async def status_cmd(self, interaction: Interaction, status: bool):
        # Check if the user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        config = json.load(open('data/config.json', 'r'))
        await interaction.response.defer(ephemeral=True)

        config['enabled'] = status
        with open('data/config.json', 'w') as f:
            json.dump(config, f, indent=4)

        return await interaction.followup.send(f"Successfully {'enabled' if status else 'disabled'} the bot.",
                                               ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded.")


def setup(client):
    client.add_cog(Disable(client))
