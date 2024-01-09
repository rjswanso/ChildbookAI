import openai
import json
import asyncio

from dotenv import load_dotenv

load_dotenv()

openai.api_key = '${OPENAI_API_KEY}'

def create_Story(characters, story_prompt):
    story_section_chunks = []
    story_sections = []
    story_lst_two = []

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a children's book author who writes stories for kids between age 4 and 8 years old."},
        {"role": "user", "content": "Write a children's story about these characters: 'Russell and Nataly' and the following story prompt: 'They live in Michigan'. Create a 5 word maximum story title for the story. Separate the story into 3 sections focused on certain scenes in the story. Label the title, 'Title::' and label each section, 'Section #::', Only include a new line after the title and after each section"},
        {"role": "assistant", "content": """Title:: Michigan's Magical Adventure
         Section 1:: The Mysterious Map
         Nataly and Russell lived in Michigan, where frosty winters turned into vibrant springs. One day, they stumbled upon a dusty map hidden in their attic. It revealed a trail leading deep into the heart of the state's largest forest.
         
         Section 2:: Forest of Whispers
         Excitement bubbled as they set off, their journey taking them through towering trees that whispered secrets of the past. Along the path, they met wise old owls and playful chipmunks who shared tales of hidden treasures rumored to grant special wishes.
         
         Section 3:: The Glowing Lake
         Their adventure led them to a sparkling lake surrounded by wildflowers. In the center of the lake stood a mystical rock, glowing with an enchanting light. It seemed to beckon them closer, promising the fulfillment of their heart's deepest desires.
         
         Section 4:: A Wish Unspoken
         Nataly and Russell hesitated, realizing that the real treasure was the love they shared as siblings. With smiles, they made a silent wish in their hearts to always be together. As they touched the glowing rock, it radiated warmth and granted their unspoken desire.
         
         Section 5:: Homeward Bound
         With hearts full of gratitude, Nataly and Russell returned home to Michigan, cherishing their newfound bond. The attic map and glowing rock remained their secret, a reminder that the most magical adventures are often found right in their own backyard."""},
        {"role": "user", "content": "Write a children's story about these characters: " + characters + "and the following story prompt: " + story_prompt + ". Create a 5 word maximum story title for the story. Separate the story into 3-5 sections focused on certain scenes in the story. Only include a new line after the title and after each section"}],
        temperature = 0.5,
        max_tokens=300
        )
    
    response = response.choices[0].message.content.strip()
    story_plot = response
    story_chunks = response.splitlines()
    story_title = story_chunks.pop(0)[8:].strip()
    for i in range(len(story_chunks)):
        s_ind = story_chunks[i].index('::') + 2
        story_sections.append(story_chunks[i][s_ind:].strip())
        story_section_chunks.append(story_chunks[i+1].strip())
    
    return story_title, story_plot, story_sections, story_section_chunks

def getImagesFromAI(story,style):
    story_section = json.loads(story.story_section_chunks)[0]
    print(story_section)
    image_urls = []
    response = openai.Image.create(
        prompt="An image that represents a part of the story: {} with room to add text in the uper 30 percent of the image and with the style {}".format(story_section,style),
        n=1,
        size="512x512"
        )
    image_urls.append(response['data'][0]['url'])
    
    return image_urls


"""#After the title and after each section, place two percent symbols: '%%'"}],
        temperature = 0.5,
        max_tokens=100
    )
    print(response.choices[0].message.content.strip())
    response = response.choices[0].message.content.strip()
    story_chunks = response.split('%%')
    story_chunks = [s.strip() for s in story_chunks]
    story_title = story_chunks.pop(0)
    story_plot = ' '.join(story_chunks)
    story_chunks_str = json.dumps(story_chunks)
    print(story_chunks_str, story_plot)
    return story_title, story_plot, story_chunks"""