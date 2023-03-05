import discord
import re
import time

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

last_action = {}
time_interval = 10

@client.event
async def on_message(message):
    if message.channel.type == discord.ChannelType.text:
        server = client.get_guild("SERVER-ID")   # Insert Discord server ID
        member = server.get_member(message.author.id)
    
        if message.author.bot:
            return

        mentions = re.findall(r'<@!?\d+>', message.content)
        if mentions:

            user_id = str(message.author.id)
            current_time = time.time()

            if user_id in last_action:
                last_action[user_id]['time'].append(current_time)
                last_action[user_id]['messages'].append(message)
            else:
                last_action[user_id] = {'time': [current_time], 'messages': [message]}


            num_actions = len(last_action[user_id]['time'])
            if num_actions >= 2 and current_time - last_action[user_id]['time'][0] < time_interval:
                await message.channel.send(f"{message.author.mention}, please do not spam mentions.")
                await last_action[user_id]['messages'][0].delete()
                await message.delete()
                await member.add_roles(discord.utils.get(server.roles, id="ROLE-ID")) # Insert Role ID (Muted Role)

            while last_action[user_id]['time'] and current_time - last_action[user_id]['time'][0] >= time_interval:
                last_action[user_id]['time'].pop(0)
                last_action[user_id]['messages'].pop(0)

client.run("TOKEN") # Insert Bot token