import numpy as np
from PIL import Image
#import matplotlib.pyplot as plt

try:
    from packages import pyotbm
    from packages.map_elements import BiomeFactory
except Exception as e:
    print(e)

path = 'Notia 2025-03-13-00-39.png'
image = Image.open(path).convert('RGB')
image_array = np.array(image)
#plt.imshow(image_array)
#plt.show()



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

def TileAreaBuilder():
    width = 500
    height = 300

    x_loc = 0
    y_loc = 0

    x_limit = 255
    y_limit = 255
    id = 0

    tile_areas = {}

    while x_limit <= width and y_limit <= height:
        tile_areas[f'tile_area_{id}'] = [(x_loc, x_limit), (y_loc, y_limit)]
        print(tile_areas)

        if x_limit == width and y_limit == height:
            return tile_areas
        elif x_limit < width:
            x_loc = x_loc + 256 if x_loc + 256 <= width else width
            x_limit = x_limit + 255 if x_loc + 255 <= width else width
        elif x_limit == width:
            x_loc = 0
            x_limit = 255

            y_loc = y_loc + 256 if y_loc + 256 <= height else height
            y_limit = y_limit + 256 if y_limit + 256 <= height else height

        id += 1

    return tile_areas

tiles = TileAreaBuilder()

