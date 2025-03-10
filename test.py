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

pyotbm.ioOTBM.create_otbm(buffer=b_test_map,filename='newTest.otbm')

import numpy as np
from PIL import Image

path = 'A2.png'

image = Image.open(path).convert('RGBA')

pixels = image.load()

pixel_dict = {()}

image_array = np.array(image)

import matplotlib.pyplot as plt
plt.imshow(image_array)
plt.show()

sample = pyotbm.ioOTBM.load_buffer('maps/sample_biomes.otbm')

test = pyotbm.parse_buffer(sample)

test.children[0].children