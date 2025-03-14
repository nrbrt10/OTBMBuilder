#import matplotlib.pyplot as plt
from packages import pyotbm
from packages.map_elements import BiomeFactory
from packages.image_handler import ImageHandler as ih

#plt.imshow(image_array)
#plt.show()

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
            x_loc = x_loc + 255 if x_loc + 255 <= img_width else img_width
            x_limit = x_limit + 255 if x_loc + 255 <= img_width else img_width
        
        elif x_limit == img_width:
            x_loc = 0
            x_limit = 255

            y_loc = y_loc + 255 if y_loc + 255 <= img_height else img_height
            y_limit = y_limit + 255 if y_limit + 255 <= img_height else img_height

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

biomes = BiomeFactory.from_config()
biomes_color = {tuple(value.base_color) : value for key, value in biomes.items()}
image = ih.load_image('Loulives 2025-03-13-23-55.png')
matches = ih.match_pixels(image=image, color_config=biomes_color)

map = pyotbm.MapFactory.empty_map(width=image.width, height=image.height)
map_data = TileAreaFactory(map_data=map.children[0], img_width=image.width-1, img_height=image.height-1)

AllocateTiles(tile_areas=map_data, matches=matches)

map_buffer = map.to_buffer()

pyotbm.ioOTBM.serialize_otbm(map_buffer, 'notia.otbm')