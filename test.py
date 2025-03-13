from packages import pyotbm
from packages import colors

import numpy as np
from PIL import Image

path = 'A1.png'

image = Image.open(path).convert('RGB')

pixels = image.load()

image_array = np.array(image)

from packages.map_elements import BiomeFactory

biomes = BiomeFactory.from_config('cfg/config.json')

biomes_color = {tuple(value.base_color) : value for key, value in biomes.items()}

matches = {}

for ij in np.ndindex(image_array.shape[:2]):
    pixel = tuple(image_array[ij])
    if pixel in biomes_color:
        matches[ij] = biomes_color[pixel].get_tile()

test_map = pyotbm.MapHeader(width=image.width, height=image.height)
data = pyotbm.MapData(test_map)

def TileAreaFactory(matches: dict, data: pyotbm.MapData):
    curr_x = 0
    curr_y = 0
    curr_z = 7

    limit_x = 255 if 255 <= image.width-1 else image.width-1
    limit_y = 255 if 255 <= image.height-1 else image.height-1

    active_TileArea = None

    for xy, tile in matches.items():
        
                    
        if limit_x >= xy[1] and limit_y < xy[0]:
            curr_y = curr_y + 255 if curr_y + 255 <= image.height-1 else curr_y + 0
            limit_y = limit_y + 255 if limit_y + 255 <= image.height-1 else image.height-1

            active_TileArea = pyotbm.TileArea(parent=data, x=curr_x, y=curr_y, z=curr_z)

        elif limit_y >= xy[0] and limit_x < xy[1]:
            curr_x = curr_x + 255 if curr_x + 255 <= image.width-1 else image.width-1
            limit_x = limit_x + 255 if limit_x + 255 <= image.width-1 else image.width-1

            active_TileArea = pyotbm.TileArea(parent=data, x=curr_x, y=curr_y, z=curr_z)

        elif limit_x < xy[1] and limit_y < xy[0]:

            curr_y = curr_y + 255 if curr_y + 255 <= image.height-1 else curr_y + 0
            limit_y = limit_y + 255 if limit_y + 255 <= image.height-1 else image.height-1

            curr_x = curr_x + 255 if curr_x + 255 <= image.width-1 else image.width-1
            limit_x = limit_x + 255 if limit_x + 255 <= image.width-1 else image.width-1

            active_TileArea = pyotbm.TileArea(parent=data, x=curr_x, y=curr_y, z=curr_z)

        rel_x = xy[1]-curr_x
        rel_y = xy[0]-curr_y
        pyotbm.Tile(active_TileArea, x=rel_x, y=rel_y, tileid=tile)

    return data

test = TileAreaFactory(matches=matches, data=data)
b_tm = test_map.to_buffer()

pyotbm.ioOTBM.serialize_otbm(b_tm, 'notia.otbm')