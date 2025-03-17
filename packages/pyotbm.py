from packages import headers as h

class ioOTBM:
    @staticmethod
    def load_buffer(otbm: str):
        with open(otbm, 'rb') as file:
            return file.read()
        
    @staticmethod
    def read_Int4LE(buffer: bytes) -> int:
        from struct import unpack
        return unpack('<i',buffer)[0]
    
    @staticmethod
    def read_Int2LE(buffer: bytes) -> int:
        from struct import unpack
        if len(buffer) == 2:
            return unpack('<h', buffer)[0]
        else:
            raise('Buffer length not 2.')
        
    @staticmethod
    def read_Long4LE(buffer: bytes) -> int:
        from struct import unpack
        if len(buffer) == 4:
            return unpack('<l', buffer)[0]
        else:
            raise('Buffer length not 4.')
        
    @staticmethod
    def read_Int1LE(buffer: bytes) -> int:
        from struct import unpack
        if len(buffer) == 1:
            return unpack('<b', buffer)[0]
        else:
            raise('Buffer length not 1.')
    
    @staticmethod
    def read_SignedInt1LE(buffer: bytes) -> int:
        from struct import unpack
        if len(buffer) == 1:
            return unpack('<B', buffer)[0]
        else:
            raise('Buffer length not 1.')

    @staticmethod
    def insert_escape_byte(buffer: bytes) -> bytes:
        i = 0
        while len(buffer) > i:
            curr = buffer[i].to_bytes()
            if curr == h.NODE_INIT or curr == h.NODE_END or curr == h.NODE_ESC:
                buffer = buffer[:i] + h.NODE_ESC + buffer[i:]
                i += 1

            i += 1

        return buffer

    @staticmethod
    def remove_escape_byte(buffer: bytes) -> bytes:
        i = 0
        while True:
            curr = buffer[i].to_bytes()
            prev = buffer[i-1].to_bytes()
            
            if (curr == h.NODE_INIT or curr == h.NODE_END) and prev != h.NODE_ESC:
                return buffer
            elif (curr == h.NODE_INIT or curr == h.NODE_END or curr == h.NODE_ESC) and prev == h.NODE_ESC:
                buffer = buffer[:i-1] + buffer[i:]
            
            i += 1

    @staticmethod
    def serialize_otbm(buffer:bytes, filename: str) -> None:
        with open(filename, 'wb') as file:
            try:
                file.write(buffer)
            except Exception as e:
                print(e)

class Node:
    def __init__(self, parent: object=None):
        self.parent = parent
        self.children = []

        if parent:
            parent.children.append(self)
    
    def to_dict(self, children=False) -> dict:
        remove_attr = ['children', 'parent']

        dict_node = {key: value for key, value in self.__dict__.items() if key not in remove_attr}

        if children and self.children:
                dict_node['children'] = [child.to_dict(children=True) for child in self.children]
        
        return dict_node
    
    def children_to_buffer(self) -> bytes:
        return b''.join(child.to_buffer() for child in self.children)
    
    def __repr__(self) -> str:
        return f'\n{self.__class__.__name__}:\n\t{'\n\t'.join([f'{k}: {v}' for k, v in self.to_dict().items()])}\n'

class MapHeader(Node):
    def __init__(self, buffer: bytes=None, **kwargs) -> None:
        super().__init__()
        self.type = 0

        if buffer:
            self.from_buffer(buffer=buffer)
        elif kwargs.get('width') and kwargs.get('height'):
            self.version = 2
            self.width = kwargs.get('width')
            self.height = kwargs.get('height')
            self.items_maj_version = 3
            self.items_min_version = 57
        else:
            raise('MapHeader init failed.')

    def from_buffer(self, buffer: bytes) -> None:
        io = ioOTBM    

        self.version = io.read_Int4LE(buffer[1:5])
        self.width = io.read_Int2LE(buffer[5:7])
        self.height = io.read_Int2LE(buffer[7:9])
        self.items_maj_version = io.read_Int4LE(buffer[9:13])
        self.items_min_version = io.read_Int4LE(buffer[13:17])

        return
    
    def to_buffer(self) -> bytes:
        from struct import pack
        io = ioOTBM

        magic_bytes = bytes(4)
        buffer = magic_bytes + h.NODE_INIT
        
        b_type = pack('<b', self.type)
        b_version = pack('<i', self.version)
        b_width = pack('<h', self.width)
        b_height = pack('<h', self.height)
        b_imjv = pack('<i', self.items_maj_version)
        b_imnv = pack('<i', self.items_min_version)

        temp_buffer = b_type + b_version + b_width + b_height + b_imjv + b_imnv

        temp_buffer = io.insert_escape_byte(buffer=temp_buffer)

        if self.children:
            temp_buffer += self.children_to_buffer()

        buffer += temp_buffer + h.NODE_END

        return buffer

class MapData(Node):
    def __init__(self, parent: MapHeader, buffer: bytes=None, **kwargs) -> None:
        super().__init__(parent=parent)
        self.type = 2
        self.description = []

        if buffer:
            self.from_buffer(buffer=buffer)
        else:
            self.description.append("Saved with Remere's Map Editor 3.7.0")

    def from_buffer(self, buffer: bytes) -> None:
        i = 0
        
        while True:
            curr = buffer[i].to_bytes()

            match curr:
                case h.OTBM_ATTR_DESCRIPTION:
                    length = buffer[i+1]
                    i += 3
                    self.description.append(buffer[i:i+length].decode('ascii'))
                case h.OTBM_ATTR_EXT_HOUSE_FILE:
                    length = buffer[i+1]
                    i += 3
                    self.house_file = buffer[i:i+length].decode('ascii')
                case h.OTBM_ATTR_EXT_SPAWN_FILE:
                    length = buffer[i+1]
                    i += 3
                    self.spawn_file = buffer[i:i+length].decode('ascii')
                case h.NODE_INIT:
                    return buffer[i-1:]
                case h.NODE_END:
                    return buffer[i-1:]
            
            i += 1

    def to_buffer(self) -> bytes:
        from struct import pack
        io = ioOTBM

        b_type = pack('<b', self.type)
        buffer = h.NODE_INIT + b_type

        for desc in self.description:
            length = len(desc).to_bytes()
            
            temp_buffer = h.OTBM_ATTR_DESCRIPTION + length + bytes(1) + str.encode(desc)

        if hasattr(self, 'house_file'):
            length = len(self.house_file).to_bytes()

        if hasattr(self, 'spawn_file'):
            length = len(self.spawn_file).to_bytes()
        
        temp_buffer = io.insert_escape_byte(buffer=temp_buffer)

        if self.children:
            temp_buffer += self.children_to_buffer()

        buffer += temp_buffer + h.NODE_END

        return buffer

class TileArea(Node):
    def __init__(self, parent: MapData, buffer: bytes=None, **kwargs) -> None:
        super().__init__(parent=parent)
        self.type = 4

        if buffer:
            self.from_buffer(buffer=buffer)
        else:
            self.x = kwargs.get('x')
            self.y = kwargs.get('y')
            self.z = kwargs.get('z')

    def from_buffer(self, buffer: bytes) -> None:
        io = ioOTBM

        self.x = io.read_Int2LE(buffer[1:3])
        self.y = io.read_Int2LE(buffer[3:5])
        self.z = io.read_Int1LE(buffer[5:6])

        return
    
    def to_buffer(self) -> bytes:
        from struct import pack
        io = ioOTBM

        buffer = h.NODE_INIT
        
        b_type = pack('<b', self.type)
        b_x = pack('<h', self.x)
        b_y = pack('<h', self.y)
        b_z = pack('<b', self.z)

        temp_buffer = b_type + b_x + b_y + b_z

        temp_buffer = io.insert_escape_byte(buffer=temp_buffer)

        if self.children:
            temp_buffer += self.children_to_buffer()

        buffer += temp_buffer + h.NODE_END

        return buffer
    
    def find_xy(self, x: int, y: int):
        relative_x = x - self.x
        relative_y = y - self.y

        return next((tile for tile in self.children if tile.x == relative_x and tile.y == relative_y), None)
       
class Tile(Node):
    def __init__(self, parent: TileArea, buffer: bytes=None, **kwargs) -> None:
        super().__init__(parent=parent)
        self.type = 5

        if buffer:
            self.from_buffer(buffer=buffer)
        else:
            self.x = int(kwargs.get('x'))
            self.y = int(kwargs.get('y'))
            self.tileid = int(kwargs.get('tileid'))
    
    def from_buffer(self, buffer: bytes) -> None:
        io = ioOTBM

        self.x = io.read_SignedInt1LE(buffer[1:2])
        self.y = io.read_SignedInt1LE(buffer[2:3])
        if buffer[3].to_bytes() == h.OTBM_ATTR_ITEM:
            self.tileid = io.read_Int2LE(buffer[4:6])

        return
    
    def to_buffer(self) -> bytes:
        from struct import pack
        io = ioOTBM

        buffer = h.NODE_INIT

        b_type = pack('<b', self.type)
        b_x = pack('<B', self.x)
        b_y = pack('<B', self.y)
        b_tileid = pack('<h', self.tileid)

        temp_buffer = b_type + b_x + b_y + h.OTBM_ATTR_ITEM + b_tileid

        temp_buffer = io.insert_escape_byte(buffer=temp_buffer)

        if self.children:
            temp_buffer += self.children_to_buffer()

        buffer += temp_buffer + h.NODE_END

        return buffer
    
class Item(Node):
    def __init__(self, parent: Tile, buffer: bytes=None, **kwargs) -> None:
        super().__init__(parent=parent)
        self.type = 6

        if buffer:
            self.from_buffer(buffer=buffer)
        else:
            self.item = kwargs.get('itemid')

    def from_buffer(self, buffer: bytes) -> None:
        io = ioOTBM

        self.itemid = io.read_Int2LE(buffer[1:3])

        return

    def to_buffer(self) -> bytes:
        from struct import pack
        io = ioOTBM

        buffer = h.NODE_INIT

        b_type = pack('<b', self.type)
        b_itemid = pack('<h', self.itemid)

        temp_buffer = b_type + b_itemid

        temp_buffer = io.insert_escape_byte(buffer=temp_buffer)

        if self.children:
            temp_buffer += self.children_to_buffer()

        buffer += temp_buffer + h.NODE_END

        return buffer

class Towns(Node):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.type = 12

    def to_buffer(self) -> bytes:
        from struct import pack
        b_type = pack('<b', self.type)

        buffer = h.NODE_INIT + b_type + h.NODE_END

        return buffer

class Waypoints(Node):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.type = 15

    def to_buffer(self) -> bytes:
        from struct import pack
        b_type = pack('<b', self.type)

        buffer = h.NODE_INIT + b_type + h.NODE_END

        return buffer

class NodeFactory:
    @staticmethod
    def from_buffer(buffer: bytes, parent: Node) -> Node:
        io = ioOTBM
        
        buffer = io.remove_escape_byte(buffer=buffer[1:]) # Starts one byte after h.NODE_INIT

        header = buffer[0].to_bytes()
        
        match header:
            case h.OTBM_MAP_HEADER:
                return MapHeader(buffer=buffer)
            
            case h.OTBM_MAP_DATA:
                return MapData(buffer=buffer, parent=parent)
            
            case h.OTBM_TILE_AREA:
                return TileArea(buffer=buffer, parent=parent)
            
            case h.OTBM_TILE:
                return Tile(buffer=buffer, parent=parent)
            
            case h.OTBM_ITEM:
                return Item(buffer=buffer, parent=parent)
            
            case h.OTBM_TOWNS:
                return Towns(parent=parent)
            
            case h.OTBM_WAYPOINTS:
                return Waypoints(parent=parent)
            
            case _:
                return Node(parent=parent)
            
class MapFactory:
    @staticmethod
    def empty_map(width, height) -> MapHeader:
        map = MapHeader(width=width, height=height)
        MapData(parent=map)
        return map
    
    @staticmethod
    def from_img() -> MapHeader:
        from packages.image_handler import ImageHandler as ih
        from packages.map_elements import BiomeFactory
        from packages.config_handler import ConfigFactory as cf

        print('Extracting biome data from config.')
        biomes = BiomeFactory.from_config()
        biomes_colors = {tuple(value.base_color) : value for key, value in biomes.items()}

        color_exclusions = cf.read_config(config_items='exclusions')

        print('Loading image data.')
        image = ih.load_image()
        print('Matching pixels to biome data.')
        matches = ih.match_pixels(image=image, color_config=biomes_colors, color_exclusions=color_exclusions)

        def compute_TileAreas(map_data: MapData, img_width: int, img_height: int):
            x_loc = 0
            y_loc = 0
            z_loc = 7

            x_limit = 255 if 255 <= img_width else img_width
            y_limit = 255 if 255 <= img_height else img_height

            tile_areas = {}

            while True:
                tile_areas[(x_limit, y_limit)] = TileArea(parent=map_data, x=x_loc, y=y_loc, z=z_loc)

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

        def allocate_Tiles(tile_areas: dict, matches: dict):
    
            for xy, tile in matches.items():

                x = xy[1]
                y = xy[0]

                for limits, value in tile_areas.items():
                    if x <= limits[0] and x >= value.x and y <= limits[1] and y >= value.y and tile:
                        relative_x = x - value.x
                        relative_y = y - value.y
                        Tile(parent=value, x=relative_x, y=relative_y, tileid=tile)

            return
    
        map = MapFactory.empty_map(width=image.width, height=image.height)
        print('Computing TileAreas...')
        tile_areas = compute_TileAreas(map_data=map.children[0], img_width=image.width-1, img_height=image.height-1)
        print('Allocating tiles to TileAreas...')
        allocate_Tiles(tile_areas=tile_areas, matches=matches)

        return map

def parse_buffer(buffer: bytes) -> MapHeader:
    print('Reading OTBM buffer...')
    i = 0
    active_node = None

    while i < len(buffer):
        curr = buffer[i].to_bytes()
        prev = buffer[i-1].to_bytes()

        if curr == h.NODE_INIT and prev != h.NODE_ESC:
            if active_node is None:
                # Initializes active node if there is none
                print(f'Root found at {i}.')
                active_node = NodeFactory.from_buffer(buffer=buffer[i:], parent=None)
                
            else:
                # If there is an active node, a NODE INIT indicates a children
                print(f'Child found at {i}')
                child = NodeFactory.from_buffer(buffer=buffer[i:], parent=active_node)
                active_node = child # Child becomes the active node

        elif curr == h.NODE_END and prev != h.NODE_ESC:
            if active_node.parent:
                active_node = active_node.parent # Activating parent node.
        i += 1
    
    return active_node