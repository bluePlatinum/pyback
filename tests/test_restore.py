import hashlib
import io
import os
import pytest
from pybacked import HASH_SHA256
from pybacked import DIFF_CONT, DIFF_DATE, DIFF_HASH
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


def test_get_current_state1():
    filepath = os.path.abspath("./tests/testdata/test_sample1.txt")
    expected_date = restore.get_edit_date(filepath)
    result = restore.get_current_state(filepath, DIFF_DATE)
    assert result == expected_date


def test_get_current_state2():
    filepath = os.path.abspath(
        "./tests/testdata/archive_hash/test_sample1.txt")
    expected_hash = restore.get_file_hash(filepath, HASH_SHA256)
    result = restore.get_current_state(filepath, DIFF_HASH, HASH_SHA256)
    assert result == expected_hash


def test_get_current_state_none():
    filepath = os.path.abspath("./tests/testdata/non-existent-file.txt")
    expected_state = None
    result = restore.get_current_state(filepath, DIFF_DATE)
    assert result == expected_state


def test_get_current_state_exception():
    filepath = os.path.abspath(
        "./tests/testdata/archive_hash/test_sample1.txt")
    with pytest.raises(ValueError):
        restore.get_current_state(filepath, DIFF_HASH)


def test_get_file_hash():
    filepath = os.path.abspath(
        "./tests/testdata/archive_hash/test_sample1.txt")
    file = io.open(filepath, "rb")
    hash_handler = hashlib.sha256(file.read())
    expected_hash = hash_handler.hexdigest()
    assert restore.get_file_hash(filepath, HASH_SHA256) == expected_hash


def test_get_edit_date():
    filepath = os.path.abspath("./tests/testdata/test_sample1.txt")
    expected_time = os.path.getmtime(filepath)
    assert restore.get_edit_date(filepath) == expected_time


def test_get_arch_state1():
    arch_path = os.path.abspath("./tests/testdata/archive_date")
    filename = "test_sample1.txt"
    expected_date = 31
    result = restore.get_arch_state(filename, arch_path, DIFF_DATE)
    assert result == expected_date


def test_get_arch_state2():
    arch_path = os.path.abspath("./tests/testdata/archive_date")
    filename = "test_sample2.txt"
    expected_date = 22
    result = restore.get_arch_state(filename, arch_path, DIFF_DATE)
    assert result == expected_date


def test_get_arch_state3():
    arch_path = os.path.abspath("./tests/testdata/archive_date")
    filename = "test_sample3.txt"
    expected_date = 33
    result = restore.get_arch_state(filename, arch_path, DIFF_DATE)
    assert result == expected_date


def test_get_arch_state_hash():
    arch_path = os.path.abspath("./tests/testdata/archive_hash")
    filename = "test_sample1.txt"
    expected_hash = '59d9a6df06b9f610f7db8e036896ed03662d168f'
    result = restore.get_arch_state(filename, arch_path, DIFF_HASH)
    assert result == expected_hash


def test_get_file_content():
    filepath = os.path.abspath("./tests/testdata/test_sample1.txt")

    # get expected content
    file = open(filepath, "rb")
    expected_content = file.read()
    file.close()

    result = restore.get_file_content(filepath)

    assert result == expected_content


def test_get_arch_state_content():
    archpath = os.path.abspath("./tests/testdata/archive_cont")
    filename = "test_sample1.txt"
    # get expected
    expected = "asdf".encode()
    result = restore.get_arch_state(filename, archpath, DIFF_CONT)
    assert result == expected
