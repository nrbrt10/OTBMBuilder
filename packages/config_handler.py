import json

class Config:
    def __init__(self):
        pass

class ConfigFactory:
    @staticmethod
    def serialize_config(config: dict) -> None:
        
        try:
            with open('cfg/config.json', 'w', encoding='utf-8') as export:
                json.dump(config, export, ensure_ascii=False, indent=3)
        except Exception as e:
            print(e)
    
    @staticmethod
    def read_config() -> Config:            

        path = 'cfg/config.json'

        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        
        except FileNotFoundError:
            print(f'Error: Config file not found at {path}.')
            return None

        except json.JSONDecodeError:
            print(f'Error: Invalid JSON format in {path}.')
            return None
        
        config = Config()

        for key, value in data.items():
            setattr(config, key, value)

        return config
                
    def add_to_config(config: dict, supersede=False, name: str=None):

        data = ConfigFactory.read_config()

        for key, value in config.items():
            if supersede and key in data:
                print(f'Existing {key} config found. Replacing with new config.')
                data[key] = value
            elif supersede is None and key in data:
                pass
            else:
                print(f'Adding {key} to config.')
                data[key] = value
        
        print('Rebuilding config...')
        ConfigFactory.serialize_config(data)
        print('Config rebuilt.')


        
            

