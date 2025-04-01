import numpy as np

from packages.image_handler import ImageHandler as ih
from packages.map_elements import BiomeFactory as bf
from packages.config_handler import ConfigFactory as cf

bio_array = np.array(ih.load_image('Thidyia-biomes.png'))
hm_array = np.array(ih.load_image('Thidyia-heightmap.png'))

from matplotlib import pyplot as plt
plt.imshow(hm_array)
plt.show()

from packages import pyotbm
map = pyotbm.MapFactory.from_img('Thidyia.otbm')