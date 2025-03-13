from packages.map_elements import Biome

class ImageHandler:
    def load_image(path):
        from PIL import Image
        try:
            return Image.open(path).convert('RGB')
        except FileNotFoundError:
            print(f'No file found at {path}')
        except Exception as e:
            print(e)

    def find_matches(biome_colors: dict[Biome]):
        ImageHandler

        from numpy import ndindex
        matches = {}
        for ij in ndindex(image_array.shape[:2]):
            pixel = tuple(image_array[ij])
            if pixel in biomes_color:
                matches[ij] = biomes_color[pixel].get_tile()

        
