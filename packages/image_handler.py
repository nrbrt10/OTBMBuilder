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

    def match_pixels(image: Image, color_config: dict[tuple, object], color_exclusions: list[str]=None) -> dict:
        from numpy import array, where, unravel_index
            
        im_array = array(image)

        X = array(list(color_config.keys()))
        y = array([config.base_color for config in color_config.values()])
        color_classifier = ImageHandler.__train_colorKNN(X, y)
        
        h, w, _ = im_array.shape
        pixels = im_array.reshape(-1, 3)
        known_mask = array([tuple(pixel) in color_config for pixel in pixels])
        
        known_pixels = pixels[known_mask]
        known_indices = where(known_mask)[0]
        
        matches = {}

        for idx, pixel in zip(known_indices, known_pixels):
            config = color_config[tuple(pixel)]
            if config.name not in color_exclusions:
                matches[tuple(unravel_index(idx, (h,w)))] = config.get_tile()
        
        unknown_pixels = pixels[~known_mask]
        if unknown_pixels.shape[0] > 0:
            predicted_colors = array(color_classifier.predict(unknown_pixels))

            for idx, predicted_color in zip(where(~known_mask)[0], predicted_colors):
                predicted_config = color_config[tuple(predicted_color)]

                if predicted_config.name not in color_exclusions:
                    matches[tuple(unravel_index(idx, (h,w)))] = predicted_config.get_tile()
        
        return matches

    def __train_colorKNN(X, y):
        from sklearn.neighbors import KNeighborsClassifier
        
        colorKNN = KNeighborsClassifier(n_neighbors=1)
        colorKNN.fit(X=X, y=y)
        
        return colorKNN