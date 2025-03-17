from packages import pyotbm

boia = pyotbm.MapFactory.from_img()
b_boia = boia.to_buffer()
pyotbm.ioOTBM.serialize_otbm(b_boia, 'kokeia.otbm')

from packages.config_handler import ConfigFactory as cf

cf.read_config(config_items='exclusions')