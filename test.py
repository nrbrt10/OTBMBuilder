from packages import pyotbm
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from packages.map_elements import BiomeFactory

path = 'Notia 2025-03-13-00-39.png'
image = Image.open(path).convert('RGB')
image_array = np.array(image)
plt.imshow(image_array)
plt.show()



biomes = BiomeFactory.from_config('cfg/config.json')
biomes_color = {tuple(value.base_color) : value for key, value in biomes.items()}
matches = {}

for ij in np.ndindex(image_array.shape[:2]):
    pixel = tuple(image_array[ij])
    if pixel in biomes_color:
        matches[ij] = biomes_color[pixel].get_tile()

def TileAreaFactory(matches: dict, data: pyotbm.MapData, img_shape: tuple):
    curr_x = 0
    curr_y = 0
    curr_z = 7

    limit_x = 255 if 255 <= img_shape[0] else img_shape[0]
    limit_y = 255 if 255 <= img_shape[1] else img_shape[1]

    active_TileArea = None

    def slide_TileArea(active_TileArea, curr_x, curr_y, curr_z, limit_x, limit_y, x, y):
        
        if not active_TileArea:
            print(f'init, {curr_x},{limit_x}:{curr_y},{limit_y}')
        elif limit_x > x and y > limit_y:
            curr_x = 0
            limit_x = 255
            
            limit_y = limit_y + 255 if limit_y + 255 <= img_shape[1] else img_shape[1]
            curr_y = curr_y + 256
            print(f'slide tilearea down, {curr_x},{limit_x},{x}:{curr_y},{limit_y},{y}')
        elif x > limit_x:
            limit_x = limit_x + 255 if limit_x + 255 <= img_shape[0] else img_shape[0]
            curr_x = curr_x + 256
            print(f'slide tilearea right, {curr_x},{limit_x},{x}:{curr_y},{limit_y},{y}')
        elif y > limit_y:
            limit_y = limit_y + 255 if limit_y + 255 <= img_shape[1] else img_shape[1]
            curr_y = curr_y + 256
            print('other')

        return pyotbm.TileArea(parent=data, x=curr_x, y=curr_y, z=curr_z), curr_x, curr_y, curr_z, limit_x, limit_y

    for xy, tile in matches.items():
        
        x = xy[1]
        y = xy[0]

        active_TileArea, curr_x, curr_y, curr_z, limit_x, limit_y = slide_TileArea(active_TileArea, curr_x, curr_y, curr_z, limit_x, limit_y, x, y)

        rel_x = x - curr_x
        rel_y = y - curr_y
        if rel_x > 255 or rel_y > 255 or rel_x < 0 or rel_y < 0:
            print(limit_x, limit_y, curr_x,  rel_x, rel_y, xy[::-1])
        pyotbm.Tile(active_TileArea, x=rel_x, y=rel_y, tileid=tile)

    return data

test_map = pyotbm.MapHeader(width=image.width, height=image.height)
data = pyotbm.MapData(test_map)
test = TileAreaFactory(matches=matches, data=data, img_shape=(image.width-1, image.height-1))

b_tm = test_map.to_buffer()

test.children[0].children

pyotbm.ioOTBM.serialize_otbm(b_tm, 'notia.otbm')

t = (1,2)
t[::-1][0]

matches[(220, 470)]

def test():
    i = 2

    if not i==1:
        pass
    elif i == 1:
        print('lol')

    return 1

t = test()

image.width
image.height


import json

with open('file.txt', 'w') as file:
    file.write(str(matches))