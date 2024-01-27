#!../.venv/bin/python

from typing import Text, Dict, Optional, Union
import os
import pandas as pd
import yaml


'''
    TODO: Add warnings and errors to the methods defined below
'''

class FileLoader:

    def __init__(self, file: Text) -> None:
        self.file = file
        self.type = file.split('.')[-1]

        print('file type: ', self.type)
        print('file path: ', self.file)

    
    def validate_file_existance(self) -> bool:
        return os.path.isfile(self.file)


    '''
        TODO: create a way to infer the delimiter (sep) character. Now '|' is hardcoded.
    '''
    def _load_csv(self) -> pd.DataFrame:
       return pd.read_csv(self.file, sep='|')

    
    def _load_yaml(self) -> Dict:
        with open(self.file, 'r') as stream:
            metadata_dict = yaml.safe_load(stream)
        return metadata_dict


    def load_data(self) -> Optional[Union[pd.DataFrame, Dict]]:
        if not self.validate_file_existance():
            print(f'The specified file {self.file} can not be found.')
            return None
        
        if self.type == 'csv':
            return self._load_csv()
        
        if self.type == 'yaml' or self.type == 'yml':
            return self._load_yaml()

        print(f'File type not supported.')

        return None





if __name__ == "__main__":
    
    yaml_file = '../tests/test_data/metadata/survey_lung_cancer_metadata.yaml'
    csv_file = '../tests/test_data/files/survey_lung_cancer.csv'

    yaml_file_loader = FileLoader(yaml_file)

    csv_file_loader = FileLoader(csv_file)
    
    print(csv_file_loader.validate_file_existance())

    print(yaml_file_loader.validate_file_existance())

    print(csv_file_loader._load_csv().columns)

    print(csv_file_loader.load_data())

    print(yaml_file_loader.load_data())
