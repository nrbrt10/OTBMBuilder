def biomes_config():

    from packages import colors as c
    from packages.map_elements import BiomeFactory

    biome_definitions = {
        'COLD_DESERT': {
            'color': c.COLD_DESERT,
            'palettes': {
                    'grass': {'type': 'tile', 'data': {25004: 200, 25005: 20, 25006: 20, 25007: 5, 25010: 5, 25008: 5, 25009: 5}},
                    'snow': {'type': 'tile', 'data': {670: 240, 6580: 10, 6581: 10, 6582: 10, 6583: 10, 6584: 10, 6585: 10, 6586: 10, 6587: 10, 6588: 10, 6589: 10, 6590: 10, 6591: 10, 6592: 10, 6593: 10}},
                    'sand': {'type': 'tile', 'data': {21605: 100, 21606: 10, 21607: 10, 21608: 10, 21609: 10, 21610: 5, 21611: 10, 21612: 10}}
            }
        },
        'GLACIER': {
            'color': c.GLACIER,
            'palettes': {
                    'snow': {'type': 'tile', 'data': {670: 240, 6580: 10, 6581: 10, 6582: 10, 6583: 10, 6584: 10, 6585: 10, 6586: 10, 6587: 10, 6588: 10, 6589: 10, 6590: 10, 6591: 10, 6592: 10, 6593: 10}}
            }
        },
        'TUNDRA': {
            'color': c.TUNDRA,
            'palettes': {
                    'snow': {'type': 'tile', 'data': {670: 240, 6580: 10, 6581: 10, 6582: 10, 6583: 10, 6584: 10, 6585: 10, 6586: 10, 6587: 10, 6588: 10, 6589: 10, 6590: 10, 6591: 10, 6592: 10, 6593: 10}},
                    'muddy_floor': {'type': 'tile', 'data': {11561: 20}}
            }
        },
        'HOT_DESERT': {
            'color': c.HOT_DESERT,
            'palettes': {
                    'sand': {'type': 'tile', 'data': {231: 10}},
                    'dry_earth': {'type': 'tile', 'data': {836: 1}}
            }
        },
        'GRASSLAND': {
            'color': c.GRASSLAND,
            'palettes': {
                    'grass': {'type': 'tile', 'data': {9043: 2500, 9044: 10, 9045: 25, 9046: 25, 9047: 25, 9048: 25, 9049: 25, 9050: 25, 9051: 15, 9052: 25, 9053: 25, 9054: 25, 9055: 20, 9056: 20, 9057: 20, 9058: 20}},
                    'dirt': {'type': 'tile', 'data': {103: 60}}
            }
        },
        'SAVANNA': {
            'color': c.SAVANNA,
            'palettes': {
                    'dried_grass': {'type': 'tile', 'data': {8326: 2500, 8327: 2500, 8328: 2500, 8329: 2500, 8330: 2500, 8331: 2500, 8332: 2500, 8333: 2500, 8334: 2500, 8347: 2500, 8348: 2500}},
                    'dry_earth': {'type': 'tile', 'data': {836: 200}},
                    'mud_sand': {'type': 'tile', 'data': {11077: 100}}
            }
        },
        'TROPICAL_SEASONAL_FOREST': {
            'color': c.TROPICAL_SEASONAL_FOREST,
            'palettes': {
                    'jungle_grass': {'type': 'tile', 'data': {3263: 50}},
                    'jungle_dirt': {'type': 'tile', 'data': {3264: 11, 3265: 1}}
            }
        },
        'TROPICAL_RAINFOREST': {
            'color': c.TROPICAL_RAINFOREST,
            'palettes': {
                    'jungle_grass': {'type': 'tile', 'data': {3263: 100}},
                    'jungle_dirt': {'type': 'tile', 'data': {3264: 11, 3265: 1}}
            }
        },
        'WETLAND': {
            'color': c.WETLAND,
            'palettes': {
                    'lush_grass': {'type': 'tile', 'data': {12698: 2500, 12699: 25, 12700: 25, 12702: 25, 12704: 25, 12705: 25}},
                    'shallow_water': {'type': 'tile', 'data': {15401: 2500, 15401: 2500}}
            }
        },
        'RIVER': {
            'color': c.RIVER,
            'palettes': {
                    'water': {'type': 'tile', 'data': {4608: 3, 4609: 1, 4610: 1, 4611: 1, 4612: 1, 4613: 1, 4614: 1, 4615: 1, 4616: 1, 4617: 1, 4618: 1, 4619: 1, 4664: 1, 4665: 1, 4666: 1}}
            }
        },
        'TEMPERATE_DECIDUOUS_FOREST': {
            'color': c.TEMPERATE_DECIDUOUS_FOREST,
            'palettes': {
                    'grass': {'type': 'tile', 'data': {9043: 2500, 9044: 10, 9045: 25, 9046: 25, 9047: 25, 9048: 25, 9049: 25, 9050: 25, 9051: 15, 9052: 25, 9053: 25, 9054: 25, 9055: 20, 9056: 20, 9057: 20, 9058: 20}},
                    'dirt': {'type': 'tile', 'data': {103: 1}},
                    'forest_floor': {'type': 'tile', 'data': {20776: 2000, 20777: 25, 20778: 25, 20779: 25, 20780: 25, 20781: 25}}

            }
        },
        'TEMPERATE_RAINFOREST': {
            'color': c.TEMPERATE_RAINFOREST,
            'palettes': {
                    'grass': {'type': 'tile', 'data': {9043: 2500, 9044: 10, 9045: 25, 9046: 25, 9047: 25, 9048: 25, 9049: 25, 9050: 25, 9051: 15, 9052: 25, 9053: 25, 9054: 25, 9055: 20, 9056: 20, 9057: 20, 9058: 20}},
                    'dirt': {'type': 'tile', 'data': {103: 100}},
                    'forest_floor': {'type': 'tile', 'data': {20776: 2000, 20777: 25, 20778: 25, 20779: 25, 20780: 25, 20781: 25}}
            }
        },
        'TAIGA': {
            'color': c.TAIGA,
            'palettes': {
                    'grass': {'type': 'tile', 'data': {9043: 2500, 9044: 10, 9045: 25, 9046: 25, 9047: 25, 9048: 25, 9049: 25, 9050: 25, 9051: 15, 9052: 25, 9053: 25, 9054: 25, 9055: 20, 9056: 20, 9057: 20, 9058: 20}},
                    'dirt': {'type': 'tile', 'data': {103: 1}},
                    'forest_floor': {'type': 'tile', 'data': {20776: 2000, 20777: 100, 20778: 120, 20779: 120, 20780: 250, 20781: 200}}

            }
        },
        'LITTORAL_WATER': {
            'color': c.LITTORAL_WATER,
            'palettes': {
                'water': {'type': 'tile', 'data': {4608: 3, 4609: 1, 4610: 1, 4611: 1, 4612: 1, 4613: 1, 4614: 1, 4615: 1, 4616: 1, 4617: 1, 4618: 1, 4619: 1, 4664: 1, 4665: 1, 4666: 1}}
            }
        },
        'DEEP_LITTORAL_WATER': {
            'color': c.DEEP_LITTORAL_WATER,
            'palettes': {}
        },
        'DEEP_WATER': {
            'color': c.DEEP_WATER,
            'palettes': {}
        },
        'DEEPER_WATER': {
            'color': c.DEEPER_WATER,
            'palettes': {}
        },
        'ICE_LAKE': {
            'color': c.ICE_LAKE,
            'palettes': {
                'ice': {'type': 'tile', 'data': {671: 2, 6683: 1, 6684: 1, 6685: 1, 6686: 1}}
            }
        },
        
    }

    biomes = [BiomeFactory.init_biome(name, data['color'], data['palettes']) for name, data in biome_definitions.items()]

    config = BiomeFactory.to_config(biomes)

    return config

def image_config():
    image_config = {
        'image_properties': 'Loulives 2025-03-13-23-55.png',
        'color_exclusions': [
         "DEEP_LITTORAL_WATER",
         "DEEP_WATER",
         "DEEPER_WATER"
      ]
    }

    from packages.config_handler import ConfigFactory as cf

    cf.add_to_config(image_config)

biomes_config()
image_config()