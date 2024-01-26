#!../.venv/bin/python

"""
FileValidator Class:

This class is designed for validating data files based on metadata information. It performs checks on the structure of
the data file, such as validating the header and ensuring specified columns do not contain null values. Metadata about
the file structure is provided through a YAML file.

Usage:
- Instantiate the FileValidator class with paths to the data file and its corresponding metadata.
- Call the 'validation' method to perform checks on the data file.

Example:
    path = '../files/survey_lung_cancer.csv'
    metadata = '../metadata/survey_lung_cancer_metadata.yaml'

    df = pd.read_csv(path, sep='|')

    file_val = FileValidator(path, metadata)

    file_val.validation()
"""



import os
from typing import Text, Dict, List, Tuple
import yaml
import csv
import pandas as pd



class FileValidator:


    DATE_FORMAT = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|1\d|2\d|3[0-1])$'

    def __init__(self, data_file_path, metadata_file_path):
        if not self._data_file_exists(data_file_path):
            raise FileNotFoundError(f'Error: File {data_file_path} does not exist.')

        self.data_file_path = data_file_path
        self.metadata_file_path = metadata_file_path

        self._load_metadata()
        self.data_df = pd.read_csv(data_file_path, sep=self.separator)


    @staticmethod
    def _get_status(processed_columms_status: List[Tuple]) -> bool:
        status_list = []
        for key, value in processed_columms_status:
            print(f'Column: {key} -> Status: {value}')
            status_list.append(value)
        return all(status_list)


    @staticmethod
    def _data_file_exists(data_file_path: Text) -> bool:
        return os.path.isfile(data_file_path)


    def _load_metadata(self) -> None:
        with open(self.metadata_file_path, 'r') as stream:
            try:
                metadata_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise ValueError(f'Metadata Error: {exc}')

        meta_dict = metadata_dict.get('metadata', {})
        validation_dict = metadata_dict.get('validations', {})

        self.filename = meta_dict.get('file', {}).get('filename')
        self.file_extension = meta_dict.get('file', {}).get('extension')
        self.separator = meta_dict.get('file', {}).get('separator')
        self.num_columns = meta_dict.get('structure', {}).get('num_columns')
        self.columns = [column.get('name') for column in meta_dict.get('columns', {})]

        self.not_null_cols = [column.get('name') for column in validation_dict.get('not_null', {})]
        self.date_format_cols = [column.get('name') for column in validation_dict.get('date_format', {})]
        self.string_length_cols_dict = [column.get('column') for column in validation_dict.get('string_length', {})]
        

    def validate_header(self) -> bool:

        with open(self.data_file_path) as file:
            reader = csv.reader(file, delimiter=self.separator)
            header = next(reader)

        normalized_header = [column.upper() for column in header]

        if len(normalized_header) != self.num_columns:
            raise ValueError(f'File Format Error: File has {len(normalized_header)} columns and must be {self.num_columns}.')

        if not set(normalized_header) <= set(self.columns):
            invalid_columns = set(normalized_header) - set(self.columns)
            raise ValueError(f'File Format Error: Invalid column name(s): {invalid_columns}. Possible column names: {self.columns}')

        if normalized_header != self.columns:
            raise ValueError(f'File Format Error: Wrong column order. It must be {self.columns}')

        return True


    def validate_not_null_columns(self) -> bool:

        print('NOT NULL COLUMNS VALIDATION STARTED')
        _check_not_null_values = lambda x: (x, not any(self.data_df[x].isnull()))
        status = list(map(_check_not_null_values, self.not_null_cols))

        return self._get_status(status)


    def validate_date_format_columns(self) -> bool:
        
        print('DATE FORMAT COLUMNS VALIDATION STARTED')
        _date_format_check = lambda x: (x, all(self.data_df[x].str.match(FileValidator.DATE_FORMAT)))
        status = list(map(_date_format_check, self.date_format_cols))
        return self._get_status(status)
    
    
    # @staticmethod
    # def _check_string_length(df: pd.DataFrame, col_info: Dict) -> bool:
    #     column = col_info.get('name')
    #     length = col_info.get('length')
    #     string_length_check = lambda x: len(x) <= length
    #     print(df[column].map(string_length_check).all())
    #     return True


    def validate_string_length_columns(self) -> bool:

        print('STRING LENGTH COLUMNS VALIDATION STARTED')
        status_list = []
        for col_info in self.string_length_cols_dict:
            column = col_info.get('name')
            length = col_info.get('length')
            _string_length_check = all(self.data_df[column].map(lambda x: len(str(x)) <= length))
            status_list.append((column, _string_length_check))
        return self._get_status(status_list)


    def perform_validation(self) -> None:

        self.validate_header()
        print('header validation passed!\n')

        if len(self.not_null_cols):
            self.validate_not_null_columns()
            print('not null validation passed!\n')

        if len(self.date_format_cols):
            self.validate_date_format_columns()
            print('date_format validation passed!\n') 

        if len(self.string_length_cols_dict):
            self.validate_string_length_columns()
            print('string length validation passed!\n')

        print('Validation Finished!')



if __name__ == "__main__":


    data_file_path = '../files/survey_lung_cancer.csv'
    metadata_file_path = '../metadata/survey_lung_cancer_metadata.yaml'

    df = pd.read_csv(data_file_path, sep='|')

    file_validator = FileValidator(data_file_path, metadata_file_path)

    file_validator.perform_validation()
