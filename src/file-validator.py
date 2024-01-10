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
from typing import Text
import yaml
import csv
import pandas as pd
import re
import numpy as np


class FileValidator:

    DATE_FORMAT = '^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|1\d|2\d|3[0-1])$'

    def __init__(self, data_file_path, metadata_file_path):
        if not self._data_file_exists(data_file_path):
            raise FileNotFoundError(f'Error: File {data_file_path} does not exist.')

        self.data_file_path = data_file_path
        self.metadata_file_path = metadata_file_path

        self._load_metadata()


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

        self.filename = meta_dict.get('file', {}).get('filename')
        self.file_extension = meta_dict.get('file', {}).get('extension')
        self.separator = meta_dict.get('file', {}).get('separator')
        self.num_columns = meta_dict.get('structure', {}).get('num_columns')

        self.columns = [column.get('name') for column in meta_dict.get('columns', {})]
        self.not_null_cols = [column.get('name') for column in meta_dict.get('not_null', {})]
        self.date_format_cols = [column.get('name') for column in meta_dict.get('date_format', {})]


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


    @staticmethod
    def _check_date_format(df: pd.DataFrame, column_name: Text) -> bool:
        not_null_df = df[df[column_name].notnull()]
        if not all(np.vectorize(lambda x: bool(re.match(FileValidator.DATE_FORMAT, str(x))))(not_null_df[column_name])):
            raise ValueError(f'Date Format Error: The date format is incorrect.')

        return True

    
    def validate_date_format_columns(self) -> bool:
        df = pd.read_csv(self.data_file_path, sep=self.separator)
        date_format_check = lambda x: bool(re.match(FileValidator.DATE_FORMAT, str(x)))
        if not df[self.date_format_cols].map(date_format_check).all().all():
            raise ValueError('Date Format Error: Incorrect date format in the specified columns.')

        return True


    def perform_validation(self) -> None:

        self.validate_header()
        print('header validation passed!')

        if len(self.not_null_cols):
            self.validate_not_null_columns()
            print('not nul validation passed!')

        if len(self.date_format_cols):
            self.validate_date_format_columns()
            print('date format validation passed!')

        print('Validation Successful!')


if __name__ == "__main__":


    data_file_path = '../files/survey_lung_cancer.csv'
    metadata_file_path = '../metadata/survey_lung_cancer_metadata.yaml'

    df = pd.read_csv(data_file_path, sep='|')

    file_validator = FileValidator(data_file_path, metadata_file_path)

    file_validator.perform_validation()
