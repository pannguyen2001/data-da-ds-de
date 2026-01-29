from helpers import check_file_exist
import unittest

class TestCheckFileExist(unittest.TestCase):
    def test_file_exist(self):
        # Test case 1: File exists
        self.assertTrue(check_file_exist("./configs/test/data_source.xlsx"))

    def test_file_not_exist(self):
        # Test case 2: File does not exist
        self.assertFalse(check_file_exist("./configs/test/data_source_not_exist.xlsx"))

    def test_empty_input(self):
        # Test case 3: File path is empty
        self.assertFalse(check_file_exist(""))

    def test_invalid_input(self):
        # Test case 4: File path is not string
        self.assertFalse(check_file_exist(None))
        self.assertFalse(check_file_exist(123))
        self.assertFalse(check_file_exist(3.14))
        self.assertFalse(check_file_exist([1, 2, 3]))
        self.assertFalse(check_file_exist({"key": "value"}))
        self.assertFalse(check_file_exist(True))



# def test_check_file_exist():
#     # Test case 1: File exists
#     assert check_file_exist("./configs/test/data_source.xlsx") == True

#     # Test case 2: File does not exist
#     assert check_file_exist("./configs/test/data_source_not_exist.xlsx") == False

#     # Test case 3: File path is empty
#     assert check_file_exist("") == False
