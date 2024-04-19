import nextcord, os, json
from nextcord.ext import commands
from nextcord.ext import tasks
from utils import Xbox

client = commands.Bot(command_prefix='^^^^^^^^^^', intents=nextcord.Intents.all())
extensions = []
ready = False
with open('data/config.json', 'r') as f: config = json.load(f)


@tasks.loop(minutes=1)
async def update_status():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.streaming, name=f"{len(Xbox.getTokens())} tokens"))
    
@client.event
async def on_ready():
    global ready
    if not ready:
        print('Bot is ready.')
        update_status.start()
        ready = True

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        extensions.append(file[:-3])

if __name__ == '__main__':
    for extension in extensions:
        client.load_extension(f'cogs.{extension}')

    client.run(config['dev_token'])