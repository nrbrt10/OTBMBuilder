import headers as h

class BufferManager:
    @classmethod
    def load_buffer(self, otbm: str):
        with open(otbm, 'rb') as file:
            return file.read()
        
    @classmethod
    def read_Int4LE(self, buffer: bytes) -> int:
        from struct import unpack
        return unpack('<i',buffer)[0]
    
    @classmethod
    def read_Int2LE(self, buffer: bytes) -> int:
        from struct import unpack
        if len(buffer) == 2:
            return unpack('<h', buffer)[0]
        else:
            raise('Buffer length not 2.')
        
    @classmethod
    def read_Long4LE(self, buffer: bytes) -> int:
        from struct import unpack
        if len(buffer) == 4:
            return unpack('<l', buffer)[0]
        else:
            raise('Buffer length not 4.')
        
    @classmethod
    def read_Int1LE(self, buffer: bytes) -> int:
        from struct import unpack
        if len(buffer) == 1:
            return unpack('<b', buffer)[0]
        else:
            raise('Buffer length not 1.')
    
    @classmethod
    def read_SignedInt1LE(self, buffer: bytes) -> int:
        from struct import unpack
        if len(buffer) == 1:
            return unpack('<B', buffer)[0]
        else:
            raise('Buffer length not 1.')

    @classmethod
    def encode_otbm(self, otbm: dict) -> bytes:
        from struct import pack
        
        buffer = b'\xfe' + pack('<b', otbm['type'])
        tbuffer = b''
        children = b''

        match otbm['type']:
            case 0:
                tbuffer = pack('<i', otbm['version']) + pack('<h', otbm['width']) + pack('<h', otbm['height']) + pack('<i', otbm['items_maj_version']) + pack('<i', otbm['items_min_version'])
            case 2:
                tbuffer = otbm['description']
            case 4:
                tbuffer = pack('<h', otbm['x']) + pack('<h', otbm['y']) + pack('<b', otbm['z'])
            case 5:
                tbuffer = pack('<B', otbm['x']) + pack('<B', otbm['y']) + h.OTBM_ATTR_ITEM + pack('<h', otbm['tileid'])
            case 12:
                pass
            case 15:
                pass

        tbuffer = self.insert_escape_byte(tbuffer)

        try:
            for node in otbm['children']:
                children = self.encode_otbm(node)
                tbuffer = tbuffer + children
                
        except:
            pass           
        
        buffer = buffer + tbuffer + b'\xff'
        return buffer

    @classmethod
    def insert_escape_byte(self, buffer: bytes) -> bytes:
        i = 0
        while len(buffer) > i:
            curr = buffer[i].to_bytes()
            if curr == h.NODE_INIT or curr == h.NODE_END or curr == h.NODE_ESC:
                buffer = buffer[:i] + h.NODE_ESC + buffer[i:]
                i += 1

            i += 1

        return buffer

class node:
    def __init__(self, iINIT: None, parent = None) -> None:
        self.children = []
        self.parent = parent
        self.iINIT = iINIT
        self.iEND = None

    def remove_escape_byte(self, buffer: bytes) -> bytes:
        i = 0
        while True:
            curr = buffer[i].to_bytes()
            prev = buffer[i-1].to_bytes()
            
            if (curr == h.NODE_INIT or curr == h.NODE_END) and prev != h.NODE_ESC:
                return buffer
            elif (curr == h.NODE_INIT or curr == h.NODE_END or curr == h.NODE_ESC) and prev == h.NODE_ESC:
                buffer = buffer[:i-1] + buffer[i:]
            
            i += 1
           
    def match_node(self, buffer: bytes) -> None:
        import struct

        bm = BufferManager
        # Removes ESC bytes from the node content
        buffer = self.remove_escape_byte(buffer=buffer[1:])

        match buffer[0].to_bytes():
            case h.OTBM_MAP_HEADER:
                self.type = 0
                self.version = bm.read_Int4LE(buffer[1:5])
                self.width = bm.read_Int2LE(buffer[5:7])
                self.height = bm.read_Int2LE(buffer[7:9])
                self.items_maj_version = bm.read_Int4LE(buffer[9:13])
                self.items_min_version = bm.read_Int4LE(buffer[13:17])
            
            case h.OTBM_MAP_DATA:
                self.type = 2
                i = self.walk_desc(buffer=buffer)
                self.description = buffer[1:i] # Just copying the description as is because I don't care about this.

            case h.OTBM_TILE_AREA:
                self.type = 4
                self.x = bm.read_Int2LE(buffer[1:3])
                self.y = bm.read_Int2LE(buffer[3:5])
                self.z = bm.read_Int1LE(buffer[5:6])

            case h.OTBM_TILE:
                self.type = 5
                self.x = bm.read_SignedInt1LE(buffer[1:2])
                self.y = bm.read_SignedInt1LE(buffer[2:3])
                if buffer[3].to_bytes() == h.OTBM_ATTR_ITEM:
                    self.tileid = bm.read_Int2LE(buffer[4:6])

            case h.OTBM_TOWNS:
                self.type = 12

            case h.OTBM_WAYPOINTS:
                self.type = 15

        return
    
    def walk_desc(self, buffer: bytes) -> int:
        i = 1
        while True:
            next = buffer[i+1].to_bytes()
            
            if next == h.NODE_INIT:
                return i+1

            i += 1

    def _to_dict(self) -> dict:
        remove_attr = ['iINIT', 'iEND', 'children', 'parent']
        
        dict_node = self.__dict__

        dict_node = {key: value for key, value in dict_node.items() if key not in remove_attr}

        if self.children:
            dict_node['children'] = []

            for child in self.children:
                dict_node['children'].append(child._to_dict())
        
        return dict_node
        
def parse_buffer(buffer: bytes) -> node:
    print('Reading OTBM buffer...')
    i = 0
    active_node = None

    while i < len(buffer):
        curr = buffer[i].to_bytes()
        prev = buffer[i-1].to_bytes()

        if curr == h.NODE_INIT and prev != h.NODE_ESC:
            if active_node is None:
                #initializes node if there is none
                active_node = node(iINIT=i)
                active_node.match_node(buffer=buffer[i:])

            else:
                #if data exists, a NODE INIT indicates a children node
                child = node(iINIT=i, parent=active_node)
                child.match_node(buffer=buffer[i:])
                active_node.children.append(child) #adds child node to children list
                active_node = child #child node becomes the active node

        elif curr == h.NODE_END and prev != h.NODE_ESC:
            active_node.iEND = i
            if active_node.parent is not None:
                active_node = active_node.parent #node closed, moving up to parent

        i += 1

    return active_node

buffer = BufferManager.load_buffer(otbm='D:/Documents/Tibia/RME/maps/void.otbm')
data = parse_buffer(buffer=buffer)
a = data._to_dict()
b = BufferManager.encode_otbm(a)