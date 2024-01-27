src_path = '../../src/file-validation'

import sys

sys.path.append(src_path)

import unittest

from file_loader import FileLoader


class TestFileLoader(unittest.TestCase):

    def test_file_type(self):
        '''
        Test that the file type is correct
        '''

        file_path = '../test_data/metadata/survey_lung_cancer_metadata.csv'

        file_type = FileLoader(file_path).get_file_type()

        self.assertEqual(file_type, 'csv', 'yaml')


if __name__ == '__main__':

    unittest.main()
