import requests
from bs4 import BeautifulSoup
import os

def img_scraper(query, quantity):
    directory = query.replace(' ', '+')
    os.makedirs(directory, exist_ok=True)

    # format the query for the Google search URL
    query = query.replace(' ', '+')

    url = f"https://www.google.com/search?q={query}&tbm=isch"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')

    # download the images
    downloaded_images = 0
    for i, image in enumerate(images):
        image_url = image['src']
        image_file = os.path.join(directory, f"image{i+1}.jpg")

        try:
            # skipping invalid URLs
            if not image_url.startswith('http'):
                raise ValueError("Invalid URL")

            response = requests.get(image_url)
            response.raise_for_status()


            with open(image_file, 'wb') as file:
                file.write(response.content)

            downloaded_images += 1
            print(f"Downloaded: {image_file}")

            if downloaded_images == quantity:
                break
        except (requests.exceptions.HTTPError, ValueError) as e:
            print(f"Error downloading image: {image_url}")
            print(str(e))

    if downloaded_images == 0:
        print("No images found.")
