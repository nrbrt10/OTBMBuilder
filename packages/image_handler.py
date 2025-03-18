import numpy as np
from PIL import Image

class ImageHandler:
    def load_image(path: str=None) -> Image:
        from packages.config_handler import ConfigFactory as cf

        if not path:
            path = cf.read_config(config_item='image_path')['image_path']

        try:
            return Image.open(path).convert('RGB')
        except FileNotFoundError:
            print(f'No file found at {path}')
            raise
        except Exception as e:
            print(e)
            raise

    def train_colorKNN(X, y):
        from sklearn.neighbors import KNeighborsClassifier
        colorKNN = KNeighborsClassifier(n_neighbors=1)
        colorKNN.fit(X=X, y=y)
        
        return colorKNN
    
    def flatten_image(image: np.ndarray):
        return image.reshape(-1, 3)
    
    def to_array(image: Image):
        return np.array(image)
    
