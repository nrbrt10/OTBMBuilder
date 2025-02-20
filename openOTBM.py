from OTBMparser import headers as h
import struct


def read_otbm(otbm):
    with open(file=otbm, mode='rb') as file:
        buffer = file.read()

    return buffer

void_buffer = read_otbm('void.otbm')
test_buffer = read_otbm('otbm2json_test.otbm')


node_start = void_buffer.find(b'\xfe')

node_start

struct.unpack('<hh', void_buffer[6:10])
struct.unpack('<h', void_buffer[10:12])
struct.unpack('<h', void_buffer[12:14])
struct.unpack('<hh', void_buffer[14:18])
struct.unpack('<hh', void_buffer[18:22])



def read_buffer(buffer):
    
    nodes = {
        'NODE_INIT': [],
        'NODE_END': [],
        'NODE_ESC': []
    }
    
    for i, byte in enumerate(buffer):
        match byte.to_bytes():
            case b'\xfe':
                nodes['NODE_INIT'].append(i)

            case b'\xff':
                nodes['NODE_END'].append(i)

            case b'\xfd':
                nodes['NODE_ESC'].append(i)

    return nodes

#nodes = read_buffer(test_buffer)

class node:
    def __init__(self, buffer: bytes):
        self.children = []
        match buffer[0].to_bytes():
            case h.OTBM_MAP_HEADER:
                self.type = 0
                self.version = struct.unpack('<i', buffer[2:6])[0]
                self.width = struct.unpack('<h', buffer[6:8])[0]
                self.height = struct.unpack('<h', buffer[8:10])[0]
                self.items_maj_version = struct.unpack('<l', buffer[10:14])[0]
                self.items_min_version = struct.unpack('<l', buffer[14:18])[0]

            case h.OTBM_MAP_DATA:
                self.type = 2
            
            case h.OTBM_TILE_AREA:
                self.type = 4

            case h.OTBM_TILE:
                self.type = 5
    
    def check_esc(self, buffer: bytes):
        pass



def read_node(buffer):
    i = 0
    while i <= len(buffer):
        try:
            if buffer[i+1] == h.NODE_ESC:
                pass

        except:
            #end of buffer
            pass
        
        
        
        if buffer[i] == h.NODE_INIT and buffer[i+1] != h.NODE_ESC:
            if data:
                child, i = read_node(buffer[i:])
                data.add_children(child)
            else:
                data = node()

        elif buffer[i] == h.NODE_END and buffer[i+1] != h.NODE_ESC:
            return data, i
        
        elif buffer[i] == h.NODE_ESC and buffer[i+1] == h.NODE_ESC:
            pass

def read_node2(buffer: bytes):
                
    data = None
    i = 0

    while i <= len(buffer):
        if buffer[i+1] != h.NODE_ESC:
            match buffer[i]:
                case h.NODE_INIT:
                    if data:
                        child_node = node(buffer[i+1:])

                case h.NODE_END:

        
    
            



def decode_buffer(buffer: bytes):

    byte_dict = {
        'INIT': [],
        'END': []
    }

    def check_esc():
        try:
            if buffer[i+1].to_bytes() == h.NODE_ESC:
                return True
            else:
                return False
        except:
            return False

    for i, byte in enumerate(buffer):
        match byte.to_bytes():
            case h.NODE_INIT:
                if check_esc():
                    continue
                else:
                    byte_dict['INIT'].append(i)
            case h.NODE_END:
                if check_esc():
                    continue
                else:
                    byte_dict['END'].append(i)

    return byte_dict


b = decode_buffer(void_buffer)

b

class blind_node:
    def __init__(self, init):
        self.init = init
        self.children = []

    def set_end(self, end):
        self.end = end

    def add_child(self, child):
        self.children.append(child)
    
    def set_parent(self, parent):
        self.parent = parent

#def match_nodes(buffer_dict: dict):
#
#    iINIT, iEND = 0, 0 #indexes for INIT and END lists
#    #def drill_down():
#        while iINIT+1 < len(buffer_dict['INIT']):
#            if buffer_dict['INIT'][iINIT]+1 < buffer_dict['END'][iEND]:
#                if data:
#                    child = blind_node(init=buffer_dict['INIT'][iINIT])
#                    child.set_parent(parent=data)
#                    data.add_child(child=child)
#                    data = child
#                    iINIT += 1   
#                else:
#                    data = blind_node(init=buffer_dict['INIT'][iINIT])
#                    iINIT +=1
#            else:
#                data.set_end(buffer_dict['END'][iEND])
#                iEND += 1
#                if data.parent:
#                    data = data.parent
                    
#def match_nodes(buffer_dict: dict):
#
#    data = None
#    iINIT, iEND = 0, 0 #indexes for INIT and END lists
#    while iINIT+1 < len(buffer_dict['INIT']):
#        
#        if not data:
#            data = blind_node(init=buffer_dict['INIT'][iINIT])
#            if buffer_dict['INIT'][iINIT+1] < buffer_dict['END'][iEND]:
#                iINIT += 1
#        
#        else:
#            if buffer_dict['INIT'][iINIT+1] < buffer_dict['END'][iEND]:
#                child = blind_node(init=buffer_dict['INIT'][iINIT])
#                child.set_parent(parent=data)
#                data.add_child(child=child)
#                data = child
#                iINIT += 1
#
#            elif buffer_dict['INIT'][iINIT] < buffer_dict['END'][iEND] and buffer_dict['INIT'][iINIT+1] > buffer_dict['END'][iEND]:
#                child = blind_node(init=buffer_dict['INIT'][iINIT])
#                child.set_parent(parent=data)
#                child.set_end(end=buffer_dict['END'][iEND])
#                data.add_child(child=child)
#                iINIT += 1
#                iEND += 1
#                print(buffer_dict['INIT'][iINIT],buffer_dict['END'][iEND])
#
#            else:
#                data.set_end(buffer_dict['END'][iEND])
#                if data.parent:
#                    data = data.parent
#                else:
#                    return data
#                iINIT += 1
#                iEND += 1

            
struct.unpack('<bb',void_buffer[402:404])

void_buffer.find(b'\xfe\x04')
void_buffer[131:].find(b'\x04')

struct.unpack('<h', void_buffer[149:151])

struct.unpack('<b', void_buffer[138])

1

void_buffer[149:151]

b

void_buffer[400:]
void_buffer[421]

data = {}
node_start = void_buffer.find(b'\xfe')
next_node = void_buffer[node_start:].find(b'\xfe')
node_end = void_buffer[node_start:].find(b'\xff')

struct.unpack('<i', void_buffer[6:10])[0]
struct.unpack('<h', void_buffer[10:12])[0]
struct.unpack('<h', void_buffer[12:14])[0]
struct.unpack('<l', void_buffer[14:18])[0]
struct.unpack('<36s', void_buffer[27:64])
        
void_buffer
test_buffer

h.NODE_INIT

test_buffer[25:].find(b'\x01')

void_buffer[96]

struct.unpack('<36s',void_buffer[27:63])