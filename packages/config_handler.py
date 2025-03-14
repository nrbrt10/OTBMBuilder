class ConfigFactory:
    @staticmethod
    def serialize_config(config: dict):
        import json
        try:
            with open('cfg/config.json', 'w', encoding='utf-8') as export:
                json.dump(config, export, ensure_ascii=False, indent=3)
        except Exception as e:
            print(e)
    
    @staticmethod
    def read_config():
        import json

        path = 'cfg/config.json'

        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
            
        
        except FileNotFoundError:
            print(f'Error: Config file not found at {path}.')
            return None

        except json.JSONDecodeError:
            print(f'Error: Invalid JSON format in {path}.')
            return None
        
    def add_to_config(config: dict):

        data = ConfigFactory.read_config()

        
            

