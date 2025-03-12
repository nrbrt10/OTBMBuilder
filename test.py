from packages import pyotbm
from packages import colors

test_map = pyotbm.MapHeader(width=2048, height=2048)
map_data = pyotbm.MapData(parent=test_map)
tile_area = pyotbm.Tile(x=500, y=500, z=7, parent=map_data)

for i in range(10):
    for j in range(10):
        pyotbm.Tile(parent=tile_area, x=i, y=j, tileid=101)

test_map.to_buffer()
b_test_map = test_map.to_buffer()

pyotbm.ioOTBM.serialize_otbm(buffer=b_test_map,filename='newTest.otbm')

import numpy as np
from PIL import Image

path = 'C:/Users/1022895/Documents/GitHub/OTBMBuilder/A1.png'

image = Image.open(path).convert('RGB')

pixels = image.load()

image_array = np.array(image)

import matplotlib.pyplot as plt
plt.imshow(image_array)
plt.show()

from packages.config_manager import BiomeFactory

biomes = BiomeFactory.from_config('C:/Users/1022895/Documents/GitHub/OTBMBuilder/biome_config.json')

biomes_lookup = {biome.base_color : biome for biome in biomes.items()}

reshaped_img = image_array.reshape(-1, 3)

print('Test')

from PIL import Image
import numpy as np
import pandas as pd

path = 'C:/Users/1022895/Documents/GitHub/OTBMBuilder/A1.png'

with Image.open(path) as im:
    image = im.convert('RGB')

image_array = np.array(image)

import json

config = 'C:/Users/1022895/Documents/GitHub/OTBMBuilder/biome_config.json'
with open(config, 'r', encoding='utf-8') as file:
    data = json.load(file)

biomes = data['biomes']

biomes

b = {}
for biome in biomes:
    np_base_color = tuple(np.array(biome['base_color']))
    b[np_base_color] = biome['name']
    
matches = {}

for ij in np.ndindex(image_array.shape[:2]):

    as_tuple = tuple(image_array[ij])
    if as_tuple in b:
        matches[ij] = b[as_tuple]


