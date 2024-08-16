import discord
import os
from shutil import copyfileobj
import requests
import json

def get_mtg_cards(text):
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

if __name__=='__main__':
    get_mtg_cards("[[Jace, Vryn's Prodigy]]")
    get_mtg_cards("[[Jace, the Mind Sculptor]]")