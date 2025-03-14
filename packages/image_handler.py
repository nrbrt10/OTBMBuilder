from PIL import Image

class ImageHandler:
    def load_image() -> Image:
        from packages.config_handler import ConfigFactory as cf

        path = cf.read_config(config='image_properties')['image_properties']['name']

        try:
            return Image.open(path).convert('RGB')
        except FileNotFoundError:
            print(f'No file found at {path}')
        except Exception as e:
            print(e)

    def match_pixels(image: Image, color_config: dict[tuple, object]) -> dict:
        from numpy import ndindex, array
        
        X = [[rgb for rgb in color] for color in color_config.keys()]
        y = [biome.base_color for biome in color_config.values()]
        color_classifier = ImageHandler.__train_colorKNN(X=X, y=y)

        im_array = array(image)

        matches = {}

        for ij in ndindex(im_array.shape[:2]):
            pixel = tuple(im_array[ij])
            if pixel in color_config:
                matches[ij] = color_config[pixel].get_tile()
            else:
                biome_color = color_classifier.predict(im_array[ij])
                if color_config[biome_color].name in ['DEEP_WATER', 'DEEPER_WATER']:
                    pass
                else:
                    matches[ij] = color_config[biome_color].get_tile()

        return matches
    
    def __train_colorKNN(X, y):
        from sklearn.neighbors import KNeighborsClassifier
        
        colorKNN = KNeighborsClassifier(n_neighbors=2)
        colorKNN.fit(X=X, y=y)
        
        return colorKNN