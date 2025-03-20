from packages import config_handler as cfg

class MapItem:
    def to_dict(self) -> dict:          
        return {
                key : [data.to_dict() for data in value] if isinstance(value, list) else value for key, value in self.__dict__.items()
        }

class TerrainPalette(MapItem):
    def __init__(self, name: str, type: str, data: dict) -> None:
        super().__init__()
        self.name = name
        self.type = type
        self.data = data

class Biome(MapItem):
    def __init__(self, name: str, color: list[int]) -> None:
        self.name = name
        self.base_color = color
        self.terrain_palettes = []

    def add_palette(self, palette) -> None:

        if isinstance(palette, TerrainPalette):
            self.terrain_palettes.append(palette)
        else:
            raise TypeError(f'Error: {palette} is an invalid palette type.')

        return
    
    def get_tile(self) -> int:
        from random import choices

        all_tiles = []
        all_weights = []

        try:
            for palette in self.terrain_palettes:
                tiles = list(palette.data.keys())
                weights = list(palette.data.values())

                all_tiles.extend(tiles)
                all_weights.extend(weights)

            return choices(all_tiles, weights=all_weights, k=1)[0]
        except:
            return None
    
class BiomeFactory:
    @staticmethod
    def init_biome(name: str, color: tuple[int], palettes: dict[str] | list[str]) -> Biome:
        biome = Biome(name, color)
        if isinstance(palettes, dict):
            for palette_name, palette_data in palettes.items():
                biome.add_palette(TerrainPalette(palette_name, palette_data['type'], palette_data['data']))
                
        elif isinstance(palettes, list):
            for palette in palettes:
                biome.add_palette(TerrainPalette(palette['name'], palette['type'], palette['data']))
        return biome
    
    @staticmethod
    def from_config() -> dict:
        
        data = cfg.ConfigFactory.read_config()

        return {biome['name'] : BiomeFactory.init_biome(biome['name'], biome['base_color'], biome['terrain_palettes']) for biome in data.biomes}
    
    @staticmethod
    def to_config(biomes: list[Biome]) -> None:
        biomes_config = {'biomes' : []}
        for biome in biomes:
            biomes_config['biomes'].append(biome.to_dict())

        cfg.ConfigFactory.add_to_config(biomes_config)