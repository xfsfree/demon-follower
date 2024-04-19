import nextcord
import datetime
from nextcord.ext import commands
from nextcord import Forbidden, HTTPException, Interaction, NotFound
from utils import Authentication


class Authenticate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="authenticate", description="Allows you to authenticate a user")
    @commands.guild_only()
    async def authenticate_cmd(self, interaction: Interaction,
                               user: nextcord.Member = nextcord.SlashOption(name="user",
                                                                            description="The user you'd like to authenticate.",
                                                                            required=True),
                               days: int = nextcord.SlashOption(name="days",
                                                                description="The amount of days you'd like to give the user access to the bot for.",
                                                                required=True, min_value=1, default=30)):

        # Check if the user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        try:
            await interaction.response.defer(ephemeral=True)
        except (NotFound, Forbidden, HTTPException):
            return  # Ignore the error silently if the interaction is not found or if deferring the response fails

        authenticate = Authentication.addSubscription(user.id, days)
        if authenticate[0]:
            expiry = datetime.datetime.now() + datetime.timedelta(days=days)
            return await interaction.followup.send(
                f"Successfully authenticated <@!{user.id}> until {expiry.strftime('%m/%d/%y %H:%M:%S%p')}")
        elif authenticate[1] == 'User already has an active subscription.':
            return await interaction.followup.send(f"<@!{user.id}> already has an active subscription.")
        else:
            return await interaction.followup.send(f"Failed to authenticate <@!{user.id}>.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded.")


def setup(client):
    client.add_cog(Authenticate(client))
