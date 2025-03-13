class MapItem:
    def to_dict(self):          
        return {
                key : [data.to_dict() for data in value] if isinstance(value, list) else value for key, value in self.__dict__.items()
        }

class TerrainPalette(MapItem):
    def __init__(self, name: str, type: str, data: dict):
        super().__init__()
        self.name = name
        self.type = type
        self.data = data

class Biome(MapItem):
    def __init__(self, name: str, color: list[int]):
        self.name = name
        self.base_color = color
        self.terrain_palettes = []

    def add_palette(self, palette):

        if isinstance(palette, TerrainPalette):
            self.terrain_palettes.append(palette)
        else:
            raise TypeError(f'Error: {palette} is an invalid palette type.')

        return
    
    def get_tile(self):
        import random

        all_tiles = []
        all_weights = []

        for palette in self.terrain_palettes:
            tiles = list(palette.data.keys())
            weights = list(palette.data.values())

            all_tiles.extend(tiles)
            all_weights.extend(weights)

        return random.choices(all_tiles, weights=all_weights, k=1)[0]

class ConfigFactory:
    @staticmethod
    def serialize_config(config: dict):
        import json
        try:
            with open('cfg/config.json', 'w', encoding='utf-8') as export:
                json.dump(config, export, ensure_ascii=False, indent=3)
        except Exception as e:
            print(e)
    
    @staticmethod
    def read_config():
        import json

        path = 'cfg/config.json'

        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        
        except FileNotFoundError:
            print(f'Error: Config file not found at {path}.')
            return None

        except json.JSONDecodeError:
            print(f'Error: Invalid JSON format in {path}.')
            return None
    
class BiomeFactory:
    @staticmethod
    def init_biome(name: str, color: tuple[int], palettes: dict[str] | list[str]):
        biome = Biome(name, color)
        if isinstance(palettes, dict):
            for palette_name, palette_data in palettes.items():
                biome.add_palette(TerrainPalette(palette_name, palette_data['type'], palette_data['data']))
                
        elif isinstance(palettes, list):
            for palette in palettes:
                biome.add_palette(TerrainPalette(palette['name'], palette['type'], palette['data']))
        return biome
    
    @staticmethod
    def from_config(path: str):
        
        data = ConfigFactory.read_config()

        return {biome['name'] : BiomeFactory.init_biome(biome['name'], biome['base_color'], biome['terrain_palettes']) for biome in data['biomes']}
    
    @staticmethod
    def to_config(biomes: list[Biome]):
        biomes_config = {'biomes' : []}
        for biome in biomes:
            biomes_config['biomes'].append(biome.to_dict())

        ConfigFactory.serialize_config(biomes_config)

def sample_config():

    from packages import colors as c

    biome_definitions = {
        'COLD_DESERT' : {
            'color' : c.COLD_DESERT,
            'palettes' : {
                    'grass': {'type': 'tile', 'data': {25004: 200, 25005: 20, 25006: 20, 25007: 5, 25010: 5, 25008: 5, 25009: 5}},
                    'snow': {'type': 'tile', 'data': {670: 240, 6580: 10, 6581: 10, 6582: 10, 6583: 10, 6584: 10, 6585: 10, 6586: 10, 6587: 10, 6588: 10, 6589: 10, 6590: 10, 6591: 10, 6592: 10, 6593: 10}},
                    'sand': {'type': 'tile', 'data': {21605: 250, 21606: 10, 21607: 10, 21608: 10, 21609: 10, 21610: 5, 21611: 10, 21612: 10}}
            }
        },
        'GLACIER' : {
            'color' : c.GLACIER,
            'palettes' : {
                    'snow' : {'type': 'tile', 'data': {670: 240, 6580: 10, 6581: 10, 6582: 10, 6583: 10, 6584: 10, 6585: 10, 6586: 10, 6587: 10, 6588: 10, 6589: 10, 6590: 10, 6591: 10, 6592: 10, 6593: 10}}
            }
        },
        'TUNDRA': {
            'color' : c.TUNDRA,
            'palettes' : {
                    'snow' : {'type': 'tile', 'data': {670: 240, 6580: 10, 6581: 10, 6582: 10, 6583: 10, 6584: 10, 6585: 10, 6586: 10, 6587: 10, 6588: 10, 6589: 10, 6590: 10, 6591: 10, 6592: 10, 6593: 10}},
                    'muddy_floor' : {'type' : 'tile', 'data' : {11561: 10000}}
            }
        },
        'HOT_DESERT' : {
            'color' : c.HOT_DESERT,
            'palettes' : {
                    'sand' : {'type': 'tile', 'data' : {231: 1}},
                    'dry_earth' : {'type': 'tile', 'data': {836: 1}}
            }
        },
        'GRASSLAND' : {
            'color' : c.GRASSLAND,
            'palettes' : {
                    'grass' : {'type' : 'tile', 'data' : {9043: 2500, 9044: 10, 9045: 25, 9046: 25, 9047: 25, 9048: 25, 9049: 25, 9050: 25, 9051: 15, 9052: 25, 9053: 25, 9054: 25, 9055: 20, 9056: 20, 9057: 20, 9058: 20}},
                    'dirt' : {'type' : 'tile', 'data' : {103: 1}}
            }
        },
        'SAVANNA' : {
            'color' : c.SAVANNA,
            'palettes' : {
                    'dried_grass' : {'type' : 'tile', 'data' : {8326: 2500, 8327: 2500, 8328: 2500, 8329: 2500, 8330: 2500, 8331: 2500, 8332: 2500, 8333: 2500, 8334: 2500, 8347: 2500, 8348: 2500}},
                    'dry_earth' : {'type': 'tile', 'data': {836: 1}},
                    'mud_sand' : {'type' : 'tile', 'data': {11077: 10000}}
            }
        },
        'TROPICAL_SEASONAL_FOREST' : {
            'color' : c.TROPICAL_SEASONAL_FOREST,
            'palettes' : {
                    'jungle_grass' : {'type': 'tile', 'data' : {3263 : 1}},
                    'jungle_dirt' : {'type' : 'tile', 'data' : {3264: 11, 3265: 1}}
            }
        },
        'TROPICAL_RAINFOREST' : {
            'color' : c.TROPICAL_RAINFOREST,
            'palettes' : {
                    'jungle_grass' : {'type': 'tile', 'data' : {3263 : 1}},
                    'jungle_dirt' : {'type' : 'tile', 'data' : {3264: 11, 3265: 1}}
            }
        },
        'WETLAND' : {
            'color' : c.WETLAND,
            'palettes' : {
                    'lush_grass' : {'type': 'tile', 'data': {12698: 2500, 12699: 2500, 12700: 2500, 12702: 2500, 12704: 2500, 12705: 2500}},
                    'shallow_water' : {'type' : 'tile', 'data' : {15401: 2500, 15401: 2500}}
            }
        },
        'RIVER' : {
            'color' : c.RIVER,
            'palettes' : {
                    'water' : {'type': 'tile', 'data': {4608: 3, 4609: 1, 4610: 1, 4611: 1, 4612: 1, 4613: 1, 4614: 1, 4615: 1, 4616: 1, 4617: 1, 4618: 1, 4619: 1, 4664: 1, 4665: 1, 4666: 1}}
            }
        },
        'TEMPERATE_DECIDUOUS_FOREST' : {
            'color' : c.TEMPERATE_DECIDUOUS_FOREST,
            'palettes' : {
                    'grass' : {'type' : 'tile', 'data' : {9043: 2500, 9044: 10, 9045: 25, 9046: 25, 9047: 25, 9048: 25, 9049: 25, 9050: 25, 9051: 15, 9052: 25, 9053: 25, 9054: 25, 9055: 20, 9056: 20, 9057: 20, 9058: 20}},
                    'dirt' : {'type' : 'tile', 'data' : {103: 1}},
                    'forest_floor' : {'type' : 'tile', 'data' : {20776: 2000, 20777: 1000, 20778: 1200, 20779: 1200, 20780: 2500, 20781: 2000}}

            }
        },
        'TEMPERATE_RAINFOREST' : {
            'color' : c.TEMPERATE_RAINFOREST,
            'palettes' : {
                    'grass' : {'type' : 'tile', 'data' : {9043: 2500, 9044: 10, 9045: 25, 9046: 25, 9047: 25, 9048: 25, 9049: 25, 9050: 25, 9051: 15, 9052: 25, 9053: 25, 9054: 25, 9055: 20, 9056: 20, 9057: 20, 9058: 20}},
                    'dirt' : {'type' : 'tile', 'data' : {103: 1}},
                    'forest_floor' : {'type' : 'tile', 'data' : {20776: 2000, 20777: 1000, 20778: 1200, 20779: 1200, 20780: 2500, 20781: 2000}}
            }
        },
        'TAIGA' : {
            'color' : c.TAIGA,
            'palettes' : {
                    'grass' : {'type' : 'tile', 'data' : {9043: 2500, 9044: 10, 9045: 25, 9046: 25, 9047: 25, 9048: 25, 9049: 25, 9050: 25, 9051: 15, 9052: 25, 9053: 25, 9054: 25, 9055: 20, 9056: 20, 9057: 20, 9058: 20}},
                    'dirt' : {'type' : 'tile', 'data' : {103: 1}},
                    'forest_floor' : {'type' : 'tile', 'data' : {20776: 2000, 20777: 1000, 20778: 1200, 20779: 1200, 20780: 2500, 20781: 2000}}

            }
        }
    }

    biomes = [BiomeFactory.init_biome(name, data['color'], data['palettes']) for name, data in biome_definitions.items()]

    config = BiomeFactory.to_config(biomes)

    return config

sample_config()

def image_config():
    image_config = {
        'image_properties' : {
            'name' : 'A1.png'
            }
    }

    ConfigFactory.serialize_config(image_config)