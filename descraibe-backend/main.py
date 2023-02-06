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

ART_PATH = Path(__file__).parent.parent / 'descraibe-frontend/public'
ART_ARCHIVE = Path(__file__).parent.parent / 'descraibe-frontend/archive/art.zip'
DATA_FILE = Path(__file__).parent.parent / 'descraibe-frontend/src/data.json'


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
        prompt = input('> ')
        if prompt.strip().lower() == 'exit':
            return
        data = generate_images(prompt)
        for obj in data:
            webbrowser.open(obj['url'])
        choice = get_selection(data)
        if choice:
            image_file = save_image(choice['url'])
            prompt_data.append({
                'prompt': prompt,
                'image': image_file.name
            })

        with open(DATA_FILE, 'w') as f:
            json.dump(prompt_data, f, indent=2)


if __name__ == "__main__":
    main()
