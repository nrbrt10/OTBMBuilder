import numpy as np
from packages import pyotbm


from packages.image_handler import ImageHandler as ih
from packages.map_elements import BiomeFactory as bf
from packages.config_handler import ConfigFactory as cf

bio_array = np.array(ih.load_image('Thidyia-biomes.png'))
hm_array = np.array(ih.load_image('Thidyia-heightmap.png'))

from matplotlib import pyplot as plt
plt.imshow(bio_array)
plt.show()

mp = pyotbm.MapProcessor()
matches = mp.process_map_data()

mp.elegible_hm_known_pixels
mp.elegible_hm_predicted_pixels
mp.elegible_bio_predicted_indices
mp.elegible_bio_known_pixels
mp.elegible_bio_known_indices

matches

h, w, _= mp.biome_img.shape
h_areas = h // 255
w_areas = w // 255
tile_areas = np.zeros(shape=[h_areas, w_areas])

yt = mp.decoded_indices_X // 255 * 255
xt = mp.decoded_indices_Y // 255 * 255

i_vals = np.arange(w_areas)
j_vals = np.arange(h_areas)

i_grid, j_grid = np.meshgrid(i_vals, j_vals, indexing='xy')

tile_areas = np.minimum(i_grid * 255, w), np.minimum(j_grid * 255, h)

tile_areas = np.stack(tile_areas, axis=-1)

def mock_create_tile_areas(row):
    print(row)
    return

np.apply_along_axis(mock_create_tile_areas, axis=2, arr=tile_areas)

def new_compute_TileAreas():
    pass