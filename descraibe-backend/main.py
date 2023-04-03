from __future__ import annotations

import json
import os
from hashlib import sha256
from pathlib import Path
from pprint import pprint

import openai
import webbrowser
import requests
import zipfile

import colorama
from colorama import Fore, Style
from resources.prompt import Prompt

ART_PATH = Path(__file__).parent.parent / 'descraibe-frontend/public'
ART_ARCHIVE = Path(__file__).parent.parent / 'descraibe-frontend/archive/art.zip'
DATA_FILE = Path(__file__).parent.parent / 'descraibe-frontend/src/data.json'


def generate_prompt() -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="write a short prompt for a weird but interesting AI generated image that contains less than 15 total characters not including any spaces.",
        max_tokens=15,
        temperature=1,
        n=1
    )
    print(f"Prompt Tokens    : {response['usage']['prompt_tokens']}")
    print(f"Completion Tokens: {response['usage']['completion_tokens']}")
    print(f"Total Tokens Used: {response['usage']['total_tokens']}\n")
    
    prompt_text = response['choices'][0]['text']
    
    return prompt_text

def generate_images(prompt: str) -> list:
    response = openai.Image.create(
        prompt=prompt,
        n=3,
        size="512x512"
    )
    return response['data']


def get_selection(data: list) -> dict | None:
    while True:
        for id, url in enumerate([i['url'] for i in data], start=1):
            print(f'{id}: {url}')
        selected_image = input('Select an image (blank to skip): ')
        if selected_image:
            try:
                choice = int(selected_image)
                selection = data[choice - 1]
                return selection
            except (ValueError, IndexError):
                print('Invalid Input!')
        else:
            return None


def save_image(url: str) -> Path:
    data = requests.get(url).content
    art_file = ART_PATH / f"art_{sha256(data).hexdigest()}.png"
    with open(art_file, 'wb') as f:
        f.write(data)
    return art_file

def get_prompt() -> None:
    while True:
        if input(f"\n\nEnter (a) to auto generate prompts using davinci-003 {Fore.RED}(may use up to 27 OpenAI tokens per prompt){Style.RESET_ALL}, or (m) to manually enter a prompt:").strip().lower() == 'a':
            prompt_text = generate_prompt() 
        else:
            prompt_text = input('manual prompt > ')
        
        prompt = Prompt(prompt_text)

        print(f"Prompt      : {Fore.GREEN}{prompt.text}{Style.RESET_ALL}")
        print(f"Letter Count: {Fore.GREEN}{prompt.letter_count}{Style.RESET_ALL}")
        print(f"Difficulty  : {Fore.GREEN}{prompt.difficulty:.2f}{Style.RESET_ALL} (1 = minimum | 1.75 = average | 3 = hard) ex: (ASTRO CLOUD = 1.30 | SAD CLOWN IN CHINATOWN = 1.73 | MAJESTIC FJORD VIEWS = 2.56 | WORD WIZZARDS = 3.17)\n")
        
        if input("Enter (y) to accept prompt, or (n) to reject prompt:").strip().lower() == 'y':
            return prompt

def main():
    """Generates a new images for data.json prompts, and saves the image files."""
    openai.api_key = os.environ['OpenAIKEY']
    running = True
    with open(DATA_FILE) as f:
        prompt_data = json.load(f)

    # Archive old art
    # for art_file in ART_PATH.iterdir():
    #     if art_file.name.startswith('art'):
    #         with zipfile.ZipFile(ART_ARCHIVE, 'a', compresslevel=6) as zip:
    #             zip.write(art_file, art_file.name)
    #         art_file.unlink()

    while running:
        prompt = get_prompt()

        data = generate_images(prompt.text)

        for obj in data:
            webbrowser.open(obj['url'])
        choice = get_selection(data)
        if choice:
            image_file = save_image(choice['url'])
            prompt_data.append({
                'prompt': prompt.text,
                'image': image_file.name
            })

        with open(DATA_FILE, 'w') as f:
            json.dump(prompt_data, f, indent=2)


if __name__ == "__main__":
    main()
