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


def match_pixels(image_array: np.ndarray, color_config: dict):
    matches = {}

    for ij in np.ndindex(image_array.shape[:2]):
        pixel = tuple(image_array[ij])
        if pixel in color_config:
            matches[ij] = color_config[pixel].get_tile()

    return matches

def TileAreaFactory(map_data: pyotbm.MapData, img_width: int, img_height: int):
    x_loc = 0
    y_loc = 0
    z_loc = 7

    x_limit = 255 if 255 <= img_width else img_width
    y_limit = 255 if 255 <= img_height else img_height

    tile_areas = {}

    while True:
        tile_areas[(x_limit, y_limit)] = pyotbm.TileArea(parent=map_data, x=x_loc, y=y_loc, z=z_loc)

        if x_limit == img_width and y_limit == img_height:
            return tile_areas
        
        elif x_limit < img_width:
            x_loc = x_loc + 256 if x_loc + 256 <= img_width else img_width
            x_limit = x_limit + 255 if x_loc + 255 <= img_width else img_width
        
        elif x_limit == img_width:
            x_loc = 0
            x_limit = 255

            y_loc = y_loc + 256 if y_loc + 256 <= img_height else img_height
            y_limit = y_limit + 256 if y_limit + 256 <= img_height else img_height

def AllocateTiles(tile_areas: dict, matches: dict):
    
    for xy, tile in matches.items():

        x = xy[1]
        y = xy[0]

        for limits, value in tile_areas.items():
            if x <= limits[0] and x >= value.x and y <= limits[1] and y >= value.y:
                relative_x = x - value.x
                relative_y = y - value.y
                pyotbm.Tile(parent=value, x=relative_x, y=relative_y, tileid=tile)

    return

matches = match_pixels(image_array=image_array, color_config=biomes_color)
map = pyotbm.MapFactory.empty_map(width=image.width, height=image.height)
map_data = TileAreaFactory(map_data=map.children[0], img_width=image.width-1, img_height=image.height-1)

map_buffer = map.to_buffer()


pyotbm.ioOTBM.serialize_otbm(map_buffer, 'notia.otbm')

t = (1,2)
t[::-1][0]

matches[(220, 470)]

def TileAreaBuilder(map_data: pyotbm.MapData):
    width = 500
    height = 300

    x_loc = 0
    y_loc = 0

    x_limit = 255
    y_limit = 255
    id = 0

    tile_areas = {}

    while x_limit <= width and y_limit <= height:
        tile_areas[f'tile_area_{id}'] = (x_loc, y_loc)
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

