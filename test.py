from packages import pyotbm

test_map = pyotbm.map_header(width=2048, height=2048)
map_data = pyotbm.map_data(parent=test_map)
test_map.children.append(map_data)

tile_area = pyotbm.tile_area(x=500, y=500, z=7, parent=map_data)
map_data.children.append(tile_area)

tileid = 101
index = 0

for i in range(10):
    for j in range(10):
        
        tile_area.children.append(pyotbm.tile(parent=tile_area, x=i, y=j, tileid=103))

b_test_map = test_map.to_buffer()

import numpy as np
from PIL import Image

path = 'D:/Downloads/Erar 2025-02-05-00-38.png'

image = Image.open(path).convert('RGBA')

image_array = np.array(image)

import matplotlib.pyplot as plt
plt.imshow(image_array)
plt.show()

plt.imshow(image_array[:3245, 10080:])
plt.show()

int(6489/2)+1

int(6489/4)+1

stepx = int(image_array.shape[0]/6)
stepy = int(image_array.shape[1]/8)

botx = 0
topx = stepx

boty = 0
topy = stepy

while topy <= image_array.shape[1]:
    
    botx = 0
    topx = stepx

    while topx <= image_array.shape[0]:

        botx += stepx
        topx += stepx    
        
    boty += stepy
    topy += stepy


unique_bytes = []

for x in range(0, image_array.shape[0], stepx):
    for y in range(0, image_array.shape[1], stepy):
        #print(f'{x}:{x+stepx}, {y}:{y+stepy}')
        #plt.imshow(image_array[x:x+stepx, y:y+stepy])
        #plt.show()

        unique_bytes.append(np.unique(image_array[x:x+stepx, y:y+stepy].reshape(-1, image_array[2]),axis=0))


np.unique(image_array.reshape(-1, image_array.shape[2]), axis=0)



unique_values = np.unique(image_array[:3245, 10080:].reshape(-1, image_array[2]),axis=0)

unique_values = np.unique(image_array.reshape(-1, image_array.shape[2]), axis=0)

import json

json_path = 'D:/Downloads/Erar Minimal 2025-02-05-00-39.json'

with open(json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

data.keys()

data['pack'].keys()

biomes = {}

for i in range(len(data['biomesData']['name'])):

    name = data['biomesData']['name'][i]
    color = data['biomesData']['color'][i]
    biomes[name] = color


def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip("#")
    rgba = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgba

b_biomes = {}

for biome, color in biomes.items():
    b_biomes[biome] = hex_to_rgba(color)

b_biomes


image_array