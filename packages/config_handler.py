import json

class ConfigFactory:
    @staticmethod
    def serialize_config(config: dict) -> None:
        
        try:
            with open('cfg/config.json', 'w', encoding='utf-8') as export:
                json.dump(config, export, ensure_ascii=False, indent=3)
        except Exception as e:
            print(e)
    
    @staticmethod
    def read_config(**config_items) -> dict:            

        path = 'cfg/config.json'

        try:
            with open(path, 'r', encoding='utf-8') as file:
                config = json.load(file)
        
        except FileNotFoundError:
            print(f'Error: Config file not found at {path}.')
            return None

        except json.JSONDecodeError:
            print(f'Error: Invalid JSON format in {path}.')
            return None
        
        if config_items:
            return {key : value for key, value in config.items() if key in config_items.values()}
        else:
            return config

        
    def add_to_config(config: dict, supersede=False):

        data = ConfigFactory.read_config()

        for key, value in config.items():
            if supersede and key in data:
                print(f'Existing {key} config found. Replacing with new config.')
                data[key] = value
            elif supersede and key in data:
                pass
            else:
                print(f'Adding {key} to config.')
                data[key] = value
        
        print('Rebuilding config...')
        ConfigFactory.serialize_config(data)
        print('Config rebuilt.')


        
            

