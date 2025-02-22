from packages import pyotbm
from packages import headers


test_map = pyotbm.map(width=2048, height=2048)
map_data = pyotbm.map_data(parent=test_map)
test_map.children.append(map_data)

tile_area = pyotbm.tile_area(x=500, y=500, z=7, parent=map_data)
map_data.children.append(tile_area)

tileid = 101

for i in range(10):
    for j in range(10):
        tile_area.children.append(pyotbm.tile(parent=tile_area, x=i, y=j, tileid=101))


t = test_map._to_dict()

io = pyotbm.ioOTBM
io.create_otbm(io.encode_otbm(t), 'test_map.otbm')

