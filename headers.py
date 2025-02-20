OTBM_MAP_HEADER= b"\x00"
OTBM_MAP_DATA= b"\x02"
OTBM_TILE_AREA= b"\x04"
OTBM_TILE= b"\x05"
OTBM_ITEM= b"\x06"
OTBM_TOWNS= b"\x0C"
OTBM_TOWN= b"\x0D"
OTBM_HOUSETILE= b"\x0E"
OTBM_WAYPOINTS= b"\x0F"
OTBM_WAYPOINT= b"\x10"

OTBM_ATTR_DESCRIPTION= b"\x01"
OTBM_ATTR_EXT_FILE= b"\x02"
OTBM_ATTR_TILE_FLAGS= b"\x03"
OTBM_ATTR_ACTION_ID= b"\x04"
OTBM_ATTR_UNIQUE_ID= b"\x05"
OTBM_ATTR_TEXT= b"\x06"
OTBM_ATTR_DESC= b"\x07"
OTBM_ATTR_TELE_DEST= b"\x08"
OTBM_ATTR_ITEM= b"\x09"
OTBM_ATTR_DEPOT_ID= b"\x0A"
OTBM_ATTR_EXT_SPAWN_FILE= b"\x0B"
OTBM_ATTR_EXT_HOUSE_FILE= b"\x0D"
OTBM_ATTR_HOUSEDOORID= b"\x0E"
OTBM_ATTR_COUNT= b"\x0F"
OTBM_ATTR_RUNE_CHARGES= b"\x16"

TILESTATE_NONE= b"\x0000"
TILESTATE_PROTECTIONZONE= b"\x0001"
TILESTATE_DEPRECATED= b"\x0002"
TILESTATE_NOPVP= b"\x0004"
TILESTATE_NOLOGOUT= b"\x0008"
TILESTATE_PVPZONE= b"\x0010"
TILESTATE_REFRESH= b"\x0020"

NODE_INIT = b"\xfe"
NODE_END = b"\xff"
NODE_ESC = b"\xfd"