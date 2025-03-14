from PIL import Image
from map_elements import Biome

class ImageHandler:
    def load_image(path):
        from PIL import Image
        
        try:
            return Image.open(path).convert('RGB')
        except FileNotFoundError:
            print(f'No file found at {path}')
        except Exception as e:
            print(e)

    def match_pixels(image: Image, color_config: dict[tuple, Biome]):
        from numpy import ndindex, array
        
        im_array = array(image)

        matches = {}

        for ij in ndindex(im_array.shape[:2]):
            pixel = tuple(im_array[ij])
            if pixel in color_config:
                matches[ij] = color_config[pixel].get_tile()

        return matches

            
