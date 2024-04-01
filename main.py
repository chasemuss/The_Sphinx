import discord
import json
import os
import requests
from shutil import copyfileobj
import time


TOKEN = open('.credentials.txt', 'r').read().strip()
client = discord.Client(intents=discord.Intents.all())
sphinx_id = '<@1202626093274767400>'


# region [Magic Bot]
def get_mtg_card(text):

    # Make sure the cache folder exists, if not, make it
    if not os.path.exists('./MTG_Cards'):
        os.mkdir('./MTG_Cards')

    # Set card image path
    def cache_image(card_name, card_set, image_uri):
        # Prep for finding / storing the image
        if not os.path.exists(f'./MTG_Cards/{card_set}'): 
            os.mkdir(f'./MTG_Cards/{card_set}')
        image_path = f'./MTG_Cards/{card_set}/{card_name}.jpg'
        image_path = image_path.replace('//', '-')
        image_path = image_path.replace(' ', '_')
        image_path = image_path.replace('"', '')
        image_path = image_path.replace("'", '')
        image_path = image_path.replace(',', '')

        # Get the image if it isn't cached
        if not os.path.exists(image_path):
            with open(image_path, 'wb') as photo: 
                copyfileobj(requests.get(image_uri, stream=True).raw, photo)
        
        return image_path

    # Used for when a card only has one relevent face
    def single_face(card):
        # Set Card Details
        card_name = card['name']
        card_set = card['set']
        card_image_uri = card['image_uris']['large']

        # Return the image
        return [discord.File(cache_image(card_name, card_set, card_image_uri))]

    # Used for when a card has 2 relevent sides
    def double_face(card):
        # Set return variable
        return_set = []
        
        # Set Card Details
        card_set = card['set']
        
        # Loop through the card faces
        for face in card['card_faces']:
            
            # Get the face details
            face_name = face['name']
            face_image_uri = face['image_uris']['large']

            # Add the image to the return set
            return_set.append(discord.File(cache_image(face_name, card_set, face_image_uri)))
        
        # Return images
        return return_set

    # Set Image list to be returned
    images_to_return = []
    
    # Count how many searches are to be done
    num_searches = text.count('[[')

    # Set search criteria
    search_criteria = []
    for x in range(num_searches):
        criterion = text[text.index('[[') + 2: text.index(']]')]
        search_criteria.append(criterion)

    # Get all the images defined by the queries
    for search in search_criteria:

        # Adjust search for url
        search = search.replace(':', '%3A')
        search = search.replace('"', '')
        search = search.replace(' ', '+')
        search = search.replace('//', '-')

        # Generate URL
        url = f'https://api.scryfall.com/cards/search?q=game%3Apaper+{search}'

        # Get Query Data
        search_response = json.loads(requests.get(url).text)

        # Get 
        for card in search_response['data']:
            try: images_to_return.extend(single_face(card))
            except KeyError: images_to_return.extend(double_face(card))

    # Yield the results
    return images_to_return

# endregion

# region [Palworld Bot]
def Palworld(message):
    def is_server_online(hostname='73.155.108.62'): return os.system('ping -c 4 ' + hostname) == 0
    if 'server' in str(message.content).lower(): return 'Server is online!' if is_server_online() else 'Server is offline...'
    if ' type' in str(message.content).lower(): return discord.File('Palworld_Type_Chart.png')
# endregion

@client.event
async def on_ready():
    channel = client.get_channel(1202629932799492217)
    await channel.send('I have arisen!')


@client.event
async def on_message(message):
    
    if message.author == client.user: return # Don't respond to self
    if sphinx_id not in message.content and '[[' not in message.content: return # Don't respond unless requested
    
    debug = True if str(message.channel) == 'bot-testing-zone' else False

    # Documentation
    if str(message.content).lower() == f'{sphinx_id}, help':
        content = ''
        with open('documentation.md', 'r') as fin:
            for line in fin:
                content += line.replace("{{ sphinx_id }}", sphinx_id)
        await message.channel.send(content)
        return

    # Palworld Commands
    if 'palworld' in str(message.channel) or debug:
        try:
            response = Palworld(message)
            if isinstance(response, str):
                await message.channel.send(response)
            elif isinstance(response, discord.File):
                await message.channel.send(file=response)
        except:
            await message.channel.send(
                f'Sorry, <@{message.author.id}>, but I do not know what you are asking for in regards to Palworld')

    if '[[' in message.content and message.content.count('[[') == message.content.count(']]'):
        card_list = get_mtg_card(message.content)
        next_message = []
        finished_procesing = True if len(card_list) > 10 else False
        while card_list:
            card = card_list.pop()
            next_message.append(card)

            if len(next_message) == 10 or len(card_list) == 0:
                await message.channel.send(files=next_message)
                next_message = []

            time.sleep(1)
        
        if finished_procesing:
            await message.channel.send("Whew, that was a lot of cards...")
        

    # Misc Commands
    if 'freddy fazbear' in str(message.content).lower(): await message.channel.send(file=discord.File('freddy.gif'))

    if 'cringe' in str(message.content).lower(): await message.channel.send(file=discord.File('cringe.gif'))


client.run(TOKEN)
