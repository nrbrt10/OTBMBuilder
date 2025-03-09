from packages import colors as c

class ConfigItem:
    def to_dict(self):          
        return {
                key : [data.to_dict() for data in value] if isinstance(value, list) else value for key, value in self.__dict__.items()
        }

class TerrainPalette(ConfigItem):
    def __init__(self, name: str, type: str, data: dict):
        super().__init__()
        self.name = name
        self.type = type
        self.data = data

class Biome(ConfigItem):
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

class ConfigManager:
    @staticmethod
    def serialize_config(filename: str, biomes: list[Biome]):
        import json
        config = {'biomes': []}

        for biome in biomes:
            print(biome.to_dict())
            config['biomes'].append(biome.to_dict())

        try:
            with open(filename, 'w+', encoding='utf-8') as export:
                json.dump(config, export, ensure_ascii=False, indent=3)
        except Exception as e:
            print(e)

        return config
    
    @staticmethod
    def read_config(path):
        import json

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
    def create_biome(name: str, color: tuple[int], palettes: dict[TerrainPalette]):
        biome = Biome(name, color)
        for palette_name, palette_data in palettes.items():
                biome.add_palette(TerrainPalette(palette_name, palette_data['type'], palette_data['data']))
        return biome

def test_config():

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
        }
    }

    biomes = [BiomeFactory.create_biome(name, data['color'], data['palettes']) for name, data in biome_definitions.items()]

    config = ConfigManager.serialize_config('config.json', biomes)

    return config