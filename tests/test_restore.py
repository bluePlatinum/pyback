import os
from pybacked import restore


def test_get_archive_list():
    archivedir = os.path.abspath("./tests/testdata")
    expected_list = [
        os.path.abspath("./tests/testdata/test_archive1_deflate.zip"),
        os.path.abspath("./tests/testdata/test_archive2_deflate.zip")]
    archive_list = restore.get_archive_list(archivedir)
    assert archive_list == expected_list
