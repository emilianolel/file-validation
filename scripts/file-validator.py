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
from typing import Text, List, Tuple, Dict
import yaml
import csv
import pandas as pd

class FileValidator:

    def __init__(self, data_file_path, metadata_file_path):
        if not self._data_file_exists(data_file_path):
            raise FileNotFoundError(f'Error: File {data_file_path} does not exist.')

        self.data_file_path = data_file_path
        self.metadata_file_path = metadata_file_path

        (
            self.filename,
            self.file_extension,
            self.separator,
            self.num_columns,
            self.columns,
            self.not_null_cols
        ) = self._get_metadata_info()


    @staticmethod
    def _data_file_exists(data_file_path: Text) -> bool:
        return os.path.isfile(data_file_path)


    @staticmethod
    def _get_column_names(meta_dict: Dict) -> List:
        return [column.get('name') for column in meta_dict]


    def _get_metadata_info(self) -> Tuple[Text, Text, Text, int, List, List]:
        with open(self.metadata_file_path, 'r') as stream:
            try:
                metadata_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise ValueError(f'Metadata Error: {exc}')

        meta_dict = metadata_dict['metadata']

        if not meta_dict:
            raise ValueError('Metadata Error: Metadata not found in the YAML file.')

        meta_file_dict = meta_dict.get('file')
        meta_struct_dict = meta_dict.get('structure')
        meta_col_dict = meta_dict.get('columns')
        meta_not_null_dict = meta_dict.get('not_null')

        filename = meta_file_dict.get('filename')
        file_extension = meta_file_dict.get('extension')
        separator = meta_file_dict.get('separator')
        number_of_columns = meta_struct_dict.get('num_columns')

        columns = FileValidator._get_column_names(meta_col_dict)
        not_null_cols = FileValidator._get_column_names(meta_not_null_dict)

        return filename, file_extension, separator, number_of_columns, columns, not_null_cols


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


    @staticmethod
    def _check_not_null_column(df: pd.DataFrame, column_name: Text) -> bool:
        if any(df[column_name].isnull()):
            raise ValueError(f'Not Null Error: There are null values in column {column_name}.')

        return True


    def validate_not_null_columns(self) -> bool:
        df = pd.read_csv(self.data_file_path, sep=self.separator)

        for column in self.not_null_cols:
            if not FileValidator._check_not_null_column(df, column):
                return False

        return True


    def perform_validation(self) -> None:
        if not self.validate_header():
            raise ValueError('Header error')

        if not self.validate_not_null_columns():
            raise ValueError('Not null column error')

        print('Validation Successful!')


if __name__ == "__main__":
    data_file_path = '../files/survey_lung_cancer.csv'
    metadata_file_path = '../metadata/survey_lung_cancer_metadata.yaml'

    df = pd.read_csv(data_file_path, sep='|')

    file_validator = FileValidator(data_file_path, metadata_file_path)

    file_validator.perform_validation()

