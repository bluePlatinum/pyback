import os
from pybacked import restore


def test_get_archive_list():
    archivedir = os.path.abspath("./tests/testdata")
    expected_list = [
        os.path.abspath("./tests/testdata/test_archive1_deflate.zip"),
        os.path.abspath("./tests/testdata/test_archive2_deflate.zip")]
    archive_list = restore.get_archive_list(archivedir)
    assert archive_list == expected_list


def test_find_diff_success():
    log_dir = os.path.abspath("./tests/testdata/log.csv")
    filename = "test_sample1.txt"
    expected_dir = {'filename': 'test_sample1.txt', 'modtype': '+',
                    'diff': '1622567933.365362'}
    assert restore.find_diff(log_dir, filename) == expected_dir


def test_find_diff_failure():
    log_dir = os.path.abspath("./tests/testdata/log.csv")
    filename = "non_existent_file"
    assert restore.find_diff(log_dir, filename) is None
