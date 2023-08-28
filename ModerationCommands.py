from discord.ext.commands import Cog, Bot, Context, command
import discord
import asyncio
import os



class Moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    def check_chat_for_bad_words(self, message: discord.Message):
        parent_file = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(parent_file, "Bad Words", "badwords.txt")
        with open(path, "r") as f:
            bad_words = f.readline()
        
        for word in message.content:
            if word in bad_words:
                return True
        
        return False
    
    @Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author == self.bot.user:
            return
        
        if self.check_chat_for_bad_words(message):
            user = str(message.author.name)

            #if user is not in the database then add the user
            if not self.bot.db.has_entry(user):
                self.bot.db.new_entry(user)

            self.bot.db[user]["bad_word_counter"] += 1

            #if users bad word counter reachers 3 then reset the counter and mute the member
            if self.bot.db[user]["bad_word_counter"] == 3:
                self.bot.db[user]["bad_word_counter"] = 0
                role = discord.utils.get(message.guild.roles, name=self.bot.mute_role_name)
                await message.author.add_roles(role)

            #update the database
            self.bot.db.update_database()

            await message.delete()

    @command(aliases=["m", "Mute"])
    async def mute(self, ctx:Context, member: discord.Member, time, *reason):
        #mutes a user for a certain amount of time unless time is specified as the letter "i" then the user
        #will be muted indefinitly
        guild = ctx.guild
        roles = guild.roles
        role = discord.utils.get(roles, name=self.bot.mute_role_name)
        perms = discord.Permissions()
        perms.update(send_messages=False, send_tts_messages=False, send_voice_messages=False, send_messages_in_threads=False, speak=False, stream=False, use_soundboard=False, view_channel=True)
            
        if not role:
            await guild.create_role(name=self.bot.mute_role_name, permissions=perms,  color=discord.colour.Color.from_rgb(255, 0, 0), position=22)
        if role.permissions != perms:
            await role.edit(permissions=perms)
        if role.position != self.mute_role_position:
            await role.edit(position=self.mute_role_position)

        if role and not discord.utils.get(member.roles, name=self.bot.mute_role_name):
            await member.add_roles(role)
        
        if time != "i":
            await asyncio.sleep(int(time))
            await member.remove_roles(role)
            
        
        

    @command(aliases=["um", "unm", "umute", "Unmute", "unMute"])
    async def unmute(self, ctx:Context, member: discord.Member, *reason):
        #will force unmute a user
        guild = ctx.guild
        roles = guild.roles
        role = discord.utils.get(roles, name=self.bot.mute_role_name)

        await member.remove_roles(role)

    @command()
    async def ban(self, ctx:Context, member: discord.Member, *reason):
        await member.ban()
    
    @command(aliases=["newnick", "cn", "nn", "NewNick"])
    #change a members nick name
    async def change_nick(self, ctx:Context, member:discord.Member, *new_nick):
        if new_nick:
            await member.edit(nick=" ".join(new_nick))



        