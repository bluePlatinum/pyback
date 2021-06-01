import io
import os
from pybacked import restore


def test_get_archive_list():
    archivedir = os.path.abspath("./tests/testdata")
    expected_list = [
        os.path.abspath("./tests/testdata/test_archive2_deflate.zip"),
        os.path.abspath("./tests/testdata/test_archive1_deflate.zip")]
    archive_list = restore.get_archive_list(archivedir)
    assert archive_list == expected_list


def test_find_diff_success():
    log_path = os.path.abspath("./tests/testdata/diff-log.csv")
    filename = "test_sample1.txt"
    expected_dict = {'filename': 'test_sample1.txt', 'modtype': '+',
                     'diff': '1622567933.365362'}
    log_file = io.open(log_path, "r")
    diff_entry = restore.find_diff(log_file, filename)
    log_file.close()
    assert diff_entry == expected_dict


def test_find_diff_failure():
    log_path = os.path.abspath("./tests/testdata/diff-log.csv")
    filename = "non_existent_file"
    log_file = io.open(log_path, "r")
    diff_entry = restore.find_diff(log_file, filename)
    log_file.close()
    assert diff_entry is None


def test_find_diff_archive_success():
    arch_path = os.path.abspath("./tests/testdata/test_archive2_deflate.zip")
    filename = "test_sample1.txt"
    expected_dict = {'filename': 'test_sample1.txt', 'modtype': '+',
                     'diff': '1622567933.365362'}
    diff_entry = restore.find_diff_archive(arch_path, filename)
    assert diff_entry == expected_dict


def test_find_diff_archive_failure():
    arch_path = os.path.abspath("./tests/testdata/test_archive2_deflate.zip")
    filename = "non_existent_file"
    diff_entry = restore.find_diff_archive(arch_path, filename)
    assert diff_entry is None


def test_get_last_date1():
    arch_path = os.path.abspath("./tests/testdata/archive_date")
    filename = "test_sample1.txt"
    expected_date = 31
    assert restore.get_last_date(filename, arch_path) == expected_date


def test_get_last_date2():
    arch_path = os.path.abspath("./tests/testdata/archive_date")
    filename = "test_sample2.txt"
    expected_date = 22
    assert restore.get_last_date(filename, arch_path) == expected_date


def test_get_last_date3():
    arch_path = os.path.abspath("./tests/testdata/archive_date")
    filename = "test_sample3.txt"
    expected_date = 33
    assert restore.get_last_date(filename, arch_path) == expected_date
