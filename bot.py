import discord
import discord.ext.commands as commands
import json
from ModerationCommands import Moderation
from database import Database
import os


"""
    This is a simple discord moderation bot.
    Features include muting, banning, changing nicknames, and monitoring chat-channels.

"""
parent_file = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(parent_file, "settings.json")
with open(path, "r") as j:
    settings = json.load(j)

database = Database(parent_file)

class DiscordModerationBot(commands.Bot):
    def __init__(self, database, parent_file):
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.parent_file = parent_file
        self.db = database
        self.mute_role_position = settings["MUTE_ROLE_POSITION"]
        self.mute_role_name = settings["MUTE_ROLE_NAME"]
        
    async def on_ready(self):
        print("Moderation bot is ready!")
        await self.add_cog(Moderation(self))

    async def on_disconnect(self):
        print("Moderation bot has disconnected!")
        await self.remove_cog(Moderation(self))


bot = DiscordModerationBot(database, parent_file)

bot.run(settings["BOT_TOKEN"])
