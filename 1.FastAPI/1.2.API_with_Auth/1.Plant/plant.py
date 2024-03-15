import requests
import os
import dotenv
import argparse
from io import BytesIO
from PIL import Image

dotenv = dotenv.load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str)
args = parser.parse_args()
plant = args.input

def get_plant_name():
    url = "https://my-api.plantnet.org/v2/identify/all"

    payload = {
        "api-key": os.getenv('PlantNet_API_KEY')
    }

    headers = {}

    files = {
        'images': open('generated_pic.png', 'rb')
    }

    response = requests.post(url, params=payload, headers=headers, files=files)
    if response.status_code != 200:
        raise Exception('can not obtain the plant name\nError code ' + str(response.status_code))
    return response.json()['bestMatch']


url = "https://54285744-illusion-diffusion.gateway.alpha.fal.ai/"
payload = {
    "image_url": "https://storage.googleapis.com/falserverless/illusion-examples/india-flag.png",
    "prompt": plant
}
headers = {
    "Authorization": os.getenv('Fal_API_KEY'),
    "Content-Type": "application/json"
}

try:
  response = requests.post(url, headers=headers, json=payload)
  if response.status_code != 200:
    raise Exception('can not generate the image\nError code ' + str(response.status_code))
  img_url = response.json()['image']['url']
  res = requests.get(img_url)
  img = Image.open(BytesIO(res.content))
  img.save('generated_pic.png')
  plant_name = get_plant_name()
except Exception as e:
  print(e)
else:
  print(plant_name)
# response.status_code