import discord
import modules.Palworld as Palworld
import modules.Scryfall as Scryfall

TOKEN = open('./.credentials.txt', 'r').read().strip()
CLIENT = discord.Client(intents=discord.Intents.all())
SPHINX_ID = '<@1202626093274767400>'


def get_documentation():
    with open('documentation.md', 'r') as fin:
        content = fin.read()
        content = content.replace('{{ sphinx_id }}', SPHINX_ID)
        return content


@CLIENT.event
async def on_ready():
    channel = CLIENT.get_channel(1202629932799492217)
    await channel.send('I have arisen!')

@CLIENT.event
async def on_message(message):
    if message.author == CLIENT.user:
        return
    
    elif "okay gamers" in message.content:
        await message.channel.send('@everyone')

    elif SPHINX_ID not in message.content and '[[' not in message.content: 
        return
    
    debug = True if str(message.channel) == 'bot-testing-zone' else False

    # Documentation
    if message.content.strip() == SPHINX_ID:
        await message.channel.send(get_documentation())
    
    # Palworld
    elif 'palworld' in str(message.channel) or (debug and 'palworld' in message.content):
        response = Palworld(message)
        
        if isinstance(response, str):
            await message.channel.send(response)
        
        elif isinstance(response, discord.File):
            await message.channel.send(file=response)

    # Magic: The Gathering
    elif '[[' in message.content and message.content.count('[[') == message.content.count(']]'):
        card_list = Scryfall.get_mtg_cards(message.content)
        next_message = []
        
        # The number of cards is more than 10, so we need to tell the requester that we are done processing
        finished_processing = True if len(card_list) > 10 else False 

        while card_list:
            next_message.append(card_list.pop())

            if len(next_message) == 10 or len(card_list) == 0:
                await message.channel.send(files=next_message)
                next_message = []
        
        # Declare the query done
        if finished_processing:
            await message.channel.send('Whew, that was a lot of cards...')


if __name__ == '__main__':
    CLIENT.run(TOKEN)