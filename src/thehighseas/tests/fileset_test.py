import unittest
import inspect

from bencode import bdecode
from hamcrest import *

from domain import FileSet

class FileSetTest(unittest.TestCase):
    def single_fileset(self):
        single_file_metainfo_path = "/".join(
            __file__.split("/")[:-1] + ["pg10.txt.torrent"])
        with open(single_file_metainfo_path, "rb") as f:
            return FileSet.from_info_dict(bdecode(f.read())["info"])

    def multi_fileset(self):
        metainfo_path = "/".join(
            __file__.split("/")[:-1] + ["dictionaries.torrent"])
        with open(metainfo_path, "rb") as f:
            return FileSet.from_info_dict(bdecode(f.read())["info"])

    def test_file_size_with_single(self):
        fileset = self.single_fileset()
        assert_that(fileset.size(), is_(4452069))

    def test_file_size_with_multi(self):
        fileset = self.multi_fileset()
        assert_that(fileset.size(), is_(1877817))
