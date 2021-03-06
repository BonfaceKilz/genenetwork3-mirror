"""Test cases for procedures defined in file_utils.py"""
import os
import unittest

from unittest import mock
from gn3.file_utils import jsonfile_to_dict
from gn3.file_utils import lookup_file
from gn3.file_utils import get_dir_hash


class TestFileUtils(unittest.TestCase):
    """Test cases for procedures defined in file_utils.py"""
    def test_get_dir_hash(self):
        """Test that a directory is hashed correctly"""
        test_dir = os.path.join(os.path.dirname(__file__), "test_data")
        self.assertEqual("fd9d74a9554b7f13bfeffbdda8e61486",
                         get_dir_hash(test_dir))

    def test_get_dir_hash_non_existent_dir(self):
        """Test thata an error is raised when the dir does not exist"""
        self.assertRaises(FileNotFoundError,
                          get_dir_hash,
                          "/non-existent-file")

    @mock.patch("os.path.isfile")
    @mock.patch.dict(os.environ, {"GENENETWORK_FILES": "/tmp/"})
    def test_lookup_genotype_file_exists(self, mock_isfile):
        """Test whether genotype file exists if file is present"""
        mock_isfile.return_value = True
        self.assertEqual(lookup_file("GENENETWORK_FILES",
                                     "genotype_files", "genotype.txt"),
                         "/tmp/genotype_files/genotype.txt")

    @mock.patch("os.path.isfile")
    @mock.patch.dict(os.environ, {"GENENETWORK_FILES": "/tmp"})
    def test_lookup_genotype_file_does_not_exist(self, mock_isfile):
        """Test whether genotype file exists if file is absent"""
        mock_isfile.return_value = False
        self.assertRaises(FileNotFoundError,
                          lookup_file,
                          "GENENETWORK_FILES",
                          "genotype_files",
                          "genotype.txt")

    def test_lookup_genotype_file_env_does_not_exist(self):
        """Test whether genotype file exists if GENENETWORK_FILES is absent"""
        self.assertRaises(FileNotFoundError,
                          lookup_file,
                          "GENENETWORK_FILES",
                          "genotype_files",
                          "genotype.txt")

    def test_jsonfile_to_dict(self):
        """Test that a json file is parsed correctly"""""
        json_file = os.path.join(os.path.dirname(__file__),
                                 "test_data", "metadata.json")
        self.assertEqual("Longer description",
                         jsonfile_to_dict(json_file).get("description"))

    def test_jsonfile_to_dict_nonexistent_file(self):
        """Test that a ValueError is raised when the json file is
non-existent"""
        self.assertRaises(FileNotFoundError,
                          jsonfile_to_dict,
                          "/non-existent-dir")
