import os
from typing import Text, List
import yaml
import csv


class FileValidator:
    

    def __init__(self, data_file, metadata_file):

        self.data_file = exit(1) if not FileValidator._data_file_exists(data_file) else data_file
        self.metadata_file = metadata_file
        
        self.filename, self.file_extension, self.separator, self.num_columns, self.columns = self._get_metadata_info()


    @staticmethod
    def _data_file_exists(data_file):
        
        if not os.path.isfile(data_file):
            print(f'Error: File {data_file} does not exist.')
            exit(1)
        return True


    @staticmethod
    def _get_column_names(meta_dict):

        return [column.get('name') for column in meta_dict]


    def _get_metadata_info(self):

        with open(self.metadata_file, 'r') as stream:
            try:
                metadata_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                exit(1)

        meta_dict = metadata_dict['metadata']

        meta_file_dict = meta_dict.get('file')
        meta_struct_dict = meta_dict.get('structure')
        meta_col_dict = meta_dict.get('columns')

        filename = meta_file_dict.get('filename')
        file_extension = meta_file_dict.get('extension')
        separator = meta_file_dict.get('separator')
        number_of_columns = meta_struct_dict.get('num_columns')

        columns = FileValidator._get_column_names(meta_col_dict)

        return filename, file_extension, separator, number_of_columns, columns


    def _header_validation(self):
        with open(self.data_file) as file:
            reader = csv.reader(file, delimiter='|')
            header = next(reader)

        normalized_header = [column.lower() for column in header]

        if len(normalized_header) != self.num_columns:
            print(f'File Format Error: File has {len(normalized_header)} columns and must be {self.num_columns}.')
            return False

        if not set(normalized_header) <= set(self.columns):
            invalid_columns = set(normalized_header) - set(self.columns)
            print(f'File Format Error: Invalid column name(s): {invalid_columns}. Possible column names: {self.columns}')
            return False

        if not normalized_header == self.columns:
            print(f'File Format Error: Wrong column order. It must be {self.columns}')
            return False

        return True


if __name__ == "__main__":

    
    path = '../files/survey_lung_cancer.csv'
    metadata = '../metadata/survey_lung_cancer_metadata.yaml'

    file_val = FileValidator(path, metadata)

    metadata_dict = file_val._get_metadata_info()

    print(metadata_dict)

    print(file_val._header_validation())
