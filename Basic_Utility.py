## add function like dump and load the yaml file
import yaml
from pathlib import Path
class Bais_utility():
    
    @staticmethod
    def load_yaml_file(path:Path):
        with open(path,'r') as f:
            file = yaml.safe_load(f)
            return file
        
    
    @staticmethod
    def dump_into_yaml_file(path:Path,data:dict):
        with open(path,'w') as f:
            yaml.dump(data,f)