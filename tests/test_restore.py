import io
import os
from pybacked import HASH_SHA256
from pybacked import DIFF_DATE, DIFF_HASH
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


def test_get_file_hash():
    filepath = os.path.abspath(
        "./tests/testdata/archive_hash/test_sample1.txt")
    expected_hash = \
        'a5479f2103b803ed4e100ee67f6c266fc1aa92a8ab86c88a46ba9f3f168e196f'
    assert restore.get_file_hash(filepath, HASH_SHA256) == expected_hash


def test_get_last_edit():
    filepath = os.path.abspath("./tests/testdata/test_sample1.txt")
    expected_time = os.path.getmtime(filepath)
    assert restore.get_last_ed(filepath) == expected_time


def test_get_last_state1():
    arch_path = os.path.abspath("./tests/testdata/archive_date")
    filename = "test_sample1.txt"
    expected_date = 31
    result = restore.get_last_state(filename, arch_path, DIFF_DATE)
    assert result == expected_date


def test_get_last_state2():
    arch_path = os.path.abspath("./tests/testdata/archive_date")
    filename = "test_sample2.txt"
    expected_date = 22
    result = restore.get_last_state(filename, arch_path, DIFF_DATE)
    assert result == expected_date


def test_get_last_state3():
    arch_path = os.path.abspath("./tests/testdata/archive_date")
    filename = "test_sample3.txt"
    expected_date = 33
    result = restore.get_last_state(filename, arch_path, DIFF_DATE)
    assert result == expected_date


def test_get_last_state_hash():
    arch_path = os.path.abspath("./tests/testdata/archive_hash")
    filename = "test_sample1.txt"
    expected_hash = '59d9a6df06b9f610f7db8e036896ed03662d168f'
    result = restore.get_last_state(filename, arch_path, DIFF_HASH)
    assert result == expected_hash
