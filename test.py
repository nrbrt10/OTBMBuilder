from packages import pyotbm

test_map = pyotbm.map_header(width=2048, height=2048)
map_data = pyotbm.map_data(parent=test_map)
test_map.children.append(map_data)

tile_area = pyotbm.tile_area(x=500, y=500, z=7, parent=map_data)
map_data.children.append(tile_area)

tileid = 101
index = 0

for i in range(10):
    for j in range(10):
        
        tile_area.children.append(pyotbm.tile(parent=tile_area, x=i, y=j, tileid=103))

b_test_map = test_map.to_buffer()

pyotbm.ioOTBM.create_otbm(buffer=b_test_map, filename='test2.otbm')

buffer = pyotbm.ioOTBM.load_buffer(otbm='D:/Documents/Python/OTBMBuilder/test2.otbm')

test = pyotbm.parse_buffer(buffer)

test.to_dict(True)

buffer