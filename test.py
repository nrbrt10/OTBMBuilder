import numpy as np
from packages import pyotbm

thidyia = pyotbm.MapFactory.from_img()
b_thidyia = thidyia.to_buffer()
pyotbm.ioOTBM.serialize_otbm(b_thidyia, 'Thidyia.otbm')

from numpy import array, where, unravel_index
from sklearn.neighbors import KNeighborsClassifier

from packages.image_handler import ImageHandler as ih
from packages.map_elements import BiomeFactory as bf
from packages.config_handler import ConfigFactory as cf

bio_array = array(ih.load_image('Thidyia-biomes.png'))
hm_array = array(ih.load_image('Thidyia-heightmap.png'))

biome_config = bf.from_config()
biome_config = {tuple(value.base_color): value for value in biome_config.values()}

heightmap_config = cf.read_config()
heightmap_config = {tuple(value['color']): value['floor'] for value in heightmap_config.values()}

biome_exclusions = cf.read_config(config_items='biome_exclusions')['biome_exclusions']

h, w, _ = bio_array.shape
bio_pixels = bio_array.reshape(-1, 3)
hm_pixels = hm_array.reshape(-1, 3)
excluded_biomes = {tuple(value.base_color) for value in biome_config.values() if value.name in biome_exclusions}

type(excluded_biomes)

bio_known_mask = array([tuple(pixel) in biome_config for pixel in bio_pixels])
bio_known_indices = where(bio_known_mask)[0]

hm_known_mask = array([tuple(pixel) in heightmap_config for pixel in hm_pixels])
hm_known_pixels = hm_pixels[hm_known_mask]
hm_unknown_pixels = hm_pixels[~hm_known_mask]

bio_known_pixels = bio_pixels[bio_known_mask]
bio_unknown_pixels = bio_pixels[~bio_known_mask]

bX = array(list(biome_config.keys()))
by = array([config.base_color for config in biome_config.values()])
biome_classifier = KNeighborsClassifier(n_neighbors=1)
biome_classifier.fit(bX, by)


hX = array(list(heightmap_config.keys()))
hy = array(list(heightmap_config.keys()))
hm_classifier = KNeighborsClassifier(n_neighbors=1)
hm_classifier.fit(hX, hy)

predicted_height = array(hm_classifier.predict(hm_unknown_pixels))


bio_unknown_indices = where(~bio_known_mask)[0]


predicted_color = array(biome_classifier.predict(bio_unknown_pixels))

elegible_known_mask = array([tuple(pixel) not in excluded_biomes for pixel in bio_known_pixels])
elegible_predicted_mask = array([tuple(pixel) not in excluded_biomes for pixel in predicted_color])

elegible_known_indices = where(elegible_known_mask)[0]
elegible_predicted_indices = where(~elegible_predicted_mask)[0]

elegible_known_pixels = bio_known_pixels[elegible_known_mask]
elegible_predicted_pixels = predicted_color[elegible_predicted_mask]

rebuilt_heightmap = np.zeros_like(hm_pixels)
rebuilt_heightmap[hm_known_mask] = hm_known_pixels
rebuilt_heightmap[~hm_known_mask] = predicted_height



hm_pixels_known_bio = rebuilt_heightmap[elegible_known_indices]
hm_pixels_predicted_bio = rebuilt_heightmap[elegible_predicted_indices]

def filter_exclusions(pixels: np.ndarray, exclusions: set=None):
    if exclusions:
        return np.array([tuple(pixel) not in exclusions for pixel in pixels])
    else:
        return pixels


def match_tiles(matches_dict, colors, heightmap, b_indices, biome_config, hm_config, h, w):
    
    for idx, biome_pixel, height_pixel in zip(b_indices, colors, heightmap):
        biome = biome_config[tuple(biome_pixel)]
        floor = hm_config[tuple(height_pixel)]
        matches_dict[(tuple(unravel_index(idx, (h,w))),floor)] = biome.get_tile()

    return matches_dict

matches = {}
test = match_tiles(matches, elegible_known_pixels, hm_pixels_known_bio, elegible_known_indices, biome_config, heightmap_config, h, w)

test





hX = array(list(heightmap_config.keys()))
hy = array([tuple(value['color']) for value in heightmap_config.values()])
hm_classifier = KNeighborsClassifier(n_neighbors=1)


hm_known_pixels = hm_pixels[hm_known_mask]
hm_unknown_pixels = hm_pixels[~hm_known_mask]



known_indices = where(bio_known_mask)[0]

config = cf.read_config()

config.heightmap_config

e =

bf.from_config().items()
