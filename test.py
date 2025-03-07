from packages import pyotbm

test_map = pyotbm.Map_header(width=2048, height=2048)
map_data = pyotbm.Map_data(parent=test_map)
tile_area = pyotbm.Tile_area(x=500, y=500, z=7, parent=map_data)

for i in range(10):
    for j in range(10):
        pyotbm.Tile(parent=tile_area, x=i, y=j, tileid=101)

test_map.to_buffer()
b_test_map = test_map.to_buffer()

pyotbm.ioOTBM.create_otbm(buffer=b_test_map,filename='newTest.otbm')

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

stepx
stepy

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


map_sections = []

for x in range(0, image_array.shape[0], stepx):
    for y in range(0, image_array.shape[1], stepy):
        #print(f'{x}:{x+stepx}, {y}:{y+stepy}')
        #plt.imshow(image_array[x:x+stepx, y:y+stepy])
        #plt.show()

        map_sections.append(image_array[x:x+stepx, y:y+stepy])




np.unique(image_array.reshape(-1, image_array.shape[2]), axis=0)

sub_array = image_array[botx:botx+stepx, boty:boty+stepy]

unique_bytes = np.unique(sub_array.reshape(-1, sub_array.shape[2]), axis=0)

plt.imshow(sub_array)
plt.show()

unique_bytes

len(sub_array.reshape(-1, sub_array.shape[2]))

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
    rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    return rgb

b_biomes = {}

for biome, color in biomes.items():
    b_biomes[biome] = hex_to_rgba(color)

b_biomes

for byte in unique_bytes[:,:3]:
    if list(byte) in b_biomes.values():
        print(byte)


unique_bytes[:,:3]

b_biomes