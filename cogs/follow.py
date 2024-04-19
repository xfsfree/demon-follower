import os
import asyncio
import json
import threading
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, NotFound, Forbidden, HTTPException
from nextcord.embeds import Embed
from utils import Xbox, Authentication


def is_admin(user):
    return user.guild_permissions.administrator


class Follow(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.follow_counts = {}
        self.tokens_last_modified = None
        self.tokens_length = None

    def reset_follow_counts(self):
        self.follow_counts = {}

    def tokens_file_modified(self):
        tokens_file = 'data/tokens.txt'
        if os.path.exists(tokens_file):
            modified_time = os.path.getmtime(tokens_file)
            length = os.path.getsize(tokens_file)
            if (self.tokens_last_modified is None or modified_time > self.tokens_last_modified) or (
                    self.tokens_length is None or length != self.tokens_length):
                self.tokens_last_modified = modified_time
                self.tokens_length = length
                return True
        return False

    @nextcord.slash_command(name="follow",
                            description="Allows you to send followers to the gamertag or xuid of your choice")
    @commands.guild_only()
    @commands.cooldown(1, 90, commands.BucketType.user)
    async def follow_cmd(self, interaction: Interaction,
                         search_term: str = nextcord.SlashOption(name="profile",
                                                                 description="The profile you'd like to send followers to.",
                                                                 required=True, min_length=2),
                         amount: int = nextcord.SlashOption(name="amount",
                                                            description="The amount of followers you'd like to send.",
                                                            required=True, min_value=1),
                         account_type: str = nextcord.SlashOption(choices={"gamertag": "gamertag", "xuid": "xuid"},
                                                                  name="account_type",
                                                                  description="The type of the requested input",
                                                                  required=True)):

        config = json.load(open('data/config.json', 'r'))
        try:
            await interaction.response.defer()
        except (NotFound, Forbidden, HTTPException):
            return

        ephemeral = not is_admin(interaction.user)

        if Authentication.checkSubscription(interaction.user.id):
            if not config.get('enabled'): return await interaction.followup.send("The bot is currently disabled.",
                                                                                 ephemeral=ephemeral)
            if not Xbox.getTokens() or len(Xbox.getTokens()) < 1: return await interaction.followup.send(
                "There are no tokens available.", ephemeral=ephemeral)
            if amount > len(Xbox.getTokens()): return await interaction.followup.send(
                f"The amount of followers you're requesting is more than how many tokens are available. We currently have {len(Xbox.getTokens())} tokens.",
                ephemeral=ephemeral)
            if search_term == None or search_term == "": return await interaction.followup.send(
                "You must provide a search term.", ephemeral=ephemeral)

            profile_data = Xbox.getProfile(search_term)
            try:
                if account_type == "gamertag":
                    xuid = profile_data["people"][0]["xuid"]
                elif account_type == "xuid":
                    xuid = search_term
            except:
                return await interaction.followup.send("I was unable to find that profile.", ephemeral=ephemeral)

            try:
                current_followers = profile_data["people"][0]["detail"]["followerCount"]
                picture = profile_data["people"][0]["displayPicRaw"]
            except:
                current_followers = 0
                picture = None
            with open('data/blacklist.txt', 'r') as file:
                blacklist = file.readlines()
                if f"{xuid}\n" in blacklist:
                    return await interaction.followup.send(
                        "Gamertag Blacklisted")
            embed = Embed(title="Follow Command", description=f"""
            > **Sent to:** {search_term}
            > **Amount to send**: {amount}
            > **XUID**: {xuid if account_type == "xuid" else profile_data["people"][0]["xuid"]}
            > **Current Followers**: {current_followers:,}
            """, color=0x00ff00)
            embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}",
                             icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
            if picture:
                embed.set_thumbnail(url=picture)

            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

            if self.tokens_file_modified():
                self.reset_follow_counts()

            sent_followers = self.follow_counts.get(search_term, 0)
            for token in Xbox.getTokens()[sent_followers:sent_followers + amount]:
                try:
                    await asyncio.sleep(.3)
                    thread = threading.Thread(target=asyncio.run,
                                              args=(Xbox.sendFollow(token, xuid, interaction.user.name),))
                    thread.daemon = True
                    thread.start()
                except:
                    pass

            self.follow_counts[search_term] = sent_followers + amount

            return await interaction.followup.send(
                f"I've finished sending {amount} followers to {search_term}. They should now have {current_followers + amount:,} followers.",
                ephemeral=ephemeral)
        else:
            return await interaction.followup.send(
                f"<@!{interaction.user.id}>, you do not have an active subscription. Please contact <@!1106772524378886154> or <@994622843893592267>.",
                ephemeral=ephemeral)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded.")


def setup(client):
    client.add_cog(Follow(client))
