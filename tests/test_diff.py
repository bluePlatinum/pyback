import time
import platform
import pybacked.zip_handler
import pytest
from os.path import abspath as abspath
from os.path import getmtime as getmtime
from pybacked import DIFF_DATE, DIFF_HASH, HASH_SHA1, HASH_SHA256
from pybacked import diff, restore


def test_diffcache_constructor_empty():
    probe_object = diff.DiffCache()
    assert probe_object.diffdict == {}
    assert probe_object.dirflags == {}
    assert probe_object.nested is True


def test_diffcache_constructor_initialdict():
    initial_dict = {"filename": "would be a diff object"}
    probe_object = diff.DiffCache(initialdict=initial_dict)
    assert probe_object.diffdict == initial_dict


def test_diffcache_constructor_initialdirflags():
    initial_dirflags = {"filename": True}
    probe_object = diff.DiffCache(initialdirflags=initial_dirflags)
    assert probe_object.dirflags == initial_dirflags


def test_diffcache_constructor_nested():
    nested = False
    probe_object = diff.DiffCache(nested=nested)
    assert probe_object.nested == nested


def test_diffcache_comparison():
    initial_dict = {"filename": "would be a diff object"}
    initial_dirflags = {"filename": True}
    cache1 = diff.DiffCache(initialdict=initial_dict,
                            initialdirflags=initial_dirflags)
    cache2 = diff.DiffCache(initialdict=initial_dict,
                            initialdirflags=initial_dirflags)
    assert cache1 == cache2


def test_diffcache_add_diff():
    initial_dict = {"filename": "would be a diff object"}
    initial_dirflags = {"filename": False}
    additional_diff = ["filename2", "would be a diff object2"]
    expected_diff = {"filename": "would be a diff object",
                     "filename2": "would be a diff object2"}
    expected_dirflags = {"filename": False, "filename2": True}
    probe_object = diff.DiffCache(initialdict=initial_dict,
                                  initialdirflags=initial_dirflags)
    probe_object.add_diff(additional_diff[0], additional_diff[1], True)
    assert probe_object.diffdict == expected_diff
    assert probe_object.dirflags == expected_dirflags


def test_diffcache_remove_diff_1():
    # test the return of .remove_diff()
    initial_diff = {"filename": "would be a diff object"}
    initial_dirflags = {"filename": False}
    probe_object = diff.DiffCache(initialdict=initial_diff,
                                  initialdirflags=initial_dirflags)
    removed_diff, removed_flags = probe_object.remove_diff("filename")
    assert removed_diff == "would be a diff object"
    assert removed_flags is False


def test_diffcache_remove_diff_2():
    # test the resulting dictionary of .remove_diff()
    initial_diff = {"filename": "would be a diff object"}
    initial_dirflags = {"filename": False}
    probe_object = diff.DiffCache(initialdict=initial_diff,
                                  initialdirflags=initial_dirflags)
    probe_object.remove_diff("filename")
    assert probe_object.diffdict == {}
    assert probe_object.dirflags == {}


def test_diffdate_constructor():
    difftype = '+'
    previous_edit = time.time()
    last_edit = time.time()
    probe_object = diff.DiffDate(difftype, last_edit, previous_edit)
    assertions = [probe_object.difftype == difftype,
                  probe_object.last_edit == last_edit,
                  probe_object.previous_edit == previous_edit]
    assert assertions == [True, True, True]


def test_diffhash_constructor():
    difftype = '+'
    current_hash = b'123456'  # would be a hash in real usage
    hash_algorithm = HASH_SHA1
    probe_object = diff.DiffHash(difftype, current_hash, hash_algorithm)
    assertions = [probe_object.difftype == difftype,
                  probe_object.currenthash == current_hash,
                  probe_object.hash_algorithm == hash_algorithm]
    assert assertions == [True, True, True]


def test_diff_constructor():
    difftype = '+'
    state = time.time()
    probe_object = diff.Diff(difftype, state)
    assertions = [probe_object.difftype == difftype,
                  probe_object.state == state]
    assert assertions == [True, True]


def test_diff_comparison():
    diff_obj1 = diff.Diff("*", 1)
    diff_obj2 = diff.Diff("*", 1)
    assert diff_obj1 == diff_obj2


class TestDetect:
    # check test_sample1.txt
    def test_detect1(self):
        filepath = abspath(
            "./tests/testdata/archive_hash/test_sample1.txt")
        archive_path = abspath(
            "./tests/testdata/archive_hash")
        expected_difftype = '*'
        expected_state = restore.get_file_hash(filepath, HASH_SHA256)

        probe_diff = diff.detect(filepath, archive_path, DIFF_HASH,
                                 HASH_SHA256)

        assert probe_diff.difftype == expected_difftype
        assert probe_diff.state == expected_state

    # check test_sample2.txt
    def test_detect2(self):
        filepath = abspath(
            "./tests/testdata/archive_hash/test_sample2.txt")
        archive_path = abspath(
            "./tests/testdata/archive_hash")
        expected_difftype = '-'
        expected_state = None

        probe_diff = diff.detect(filepath, archive_path, DIFF_HASH,
                                 HASH_SHA256)

        assert probe_diff.difftype == expected_difftype
        assert probe_diff.state == expected_state

    # check test_sample3.txt
    def test_detect3(self):
        filepath = abspath(
            "./tests/testdata/archive_hash/test_sample3.txt")
        archive_path = abspath(
            "./tests/testdata/archive_hash")

        probe_diff = diff.detect(filepath, archive_path, DIFF_HASH,
                                 HASH_SHA256)

        assert probe_diff is None

    # check test_sample4.txt
    def test_detect4(self):
        filepath = abspath(
            "./tests/testdata/archive_hash/test_sample4.txt")
        archive_path = abspath(
            "./tests/testdata/archive_hash")
        expected_difftype = '+'
        expected_state = restore.get_file_hash(filepath, HASH_SHA256)

        probe_diff = diff.detect(filepath, archive_path, DIFF_HASH,
                                 HASH_SHA256)

        assert probe_diff.difftype == expected_difftype
        assert probe_diff.state == expected_state

    # check for exception occuring if hash algorithm isn't provided but diff
    # detection is set to DIFF_HASH
    def test_detect_exception(self):
        filepath = abspath(
            "./tests/testdata/archive_hash/test_sample4.txt")
        archive_path = abspath(
            "./tests/testdata/archive_hash")
        with pytest.raises(ValueError):
            diff.detect(filepath, archive_path, DIFF_HASH)


class TestCollect:
    def test_collect1(self):
        storage = abspath("./tests/testdata/full_storage")
        archive = abspath("./tests/testdata/full_archive")

        # create main DiffCache object and add doc1.txt record
        expected_cache = diff.DiffCache()

        expected_cache.add_diff(abspath(storage + "/doc1.txt"),
                                diff.Diff("*", getmtime(
                                    abspath(storage + "/doc1.txt")
                                )), False)

        # create DiffCache for subdir/subdir
        subsub_initialdict = {abspath(storage + "/subdir/subdir/doc4.txt"):
                              diff.Diff("*", getmtime(
                                  abspath(storage + "/subdir/subdir/doc4.txt")
                              ))}

        subsub_dirflags = {abspath(storage + "/subdir/subdir/doc4.txt"): False}
        subsub_diffcache = diff.DiffCache(initialdict=subsub_initialdict,
                                          initialdirflags=subsub_dirflags)

        # create DiffCache for subdir
        sub_initialdict = {abspath(storage + "/subdir/doc2.txt"):
                           diff.Diff("*", getmtime(
                               abspath(storage + "/subdir/doc2.txt"))),
                           abspath(storage + "/subdir/doc3.txt"):
                           diff.Diff("*", getmtime(
                               abspath(storage + "/subdir/doc3.txt"))),
                           abspath(storage + "/subdir/subdir"):
                           subsub_diffcache}
        sub_initialdirflags = {abspath(storage + "/subdir/doc2.txt"): False,
                               abspath(storage + "/subdir/doc3.txt"): False,
                               abspath(storage + "/subdir/subdir"): True}
        sub_diffcache = diff.DiffCache(initialdict=sub_initialdict,
                                       initialdirflags=sub_initialdirflags)

        # add sub_diffcache to expected_cache
        expected_cache.add_diff(abspath(storage + "/subdir"),
                                sub_diffcache, True)

        diff_cache = diff.collect(storage, archive, DIFF_DATE)
        assert diff_cache == expected_cache

    def test_collect_none(self):
        """
        Test if diff.collect removes None entries (entries for files, where no
        change has been detected)
        """

        storage = abspath("./tests/testdata/ext_test/storage")
        if platform.system() != "Windows":
            archive = abspath("./tests/testdata/ext_test/archive_linux")
        else:
            archive = abspath("./tests/testdata/ext_test/archive")

        diffcache = diff.collect(storage, archive, DIFF_HASH, HASH_SHA256)

        # check if None entries (doc1.txt, doc3.txt) were successully removed
        subdir = abspath("./tests/testdata/ext_test/storage/subdir")

        assert len(diffcache.diffdict) == 1
        assert len(diffcache.diffdict[subdir].diffdict) == 2


def test_diffcache_iter():
    # generate a diff cache
    storagepath = abspath("./tests/testdata/full_storage")
    archivepath = abspath("./tests/testdata/full_archive")
    diffcache = diff.collect(storagepath, archivepath, DIFF_DATE)

    # create expected
    exp_path1 = abspath("./tests/testdata/full_storage/doc1.txt")
    exp_path2 = abspath("./tests/testdata/full_storage/subdir")
    exp_paths = [exp_path1, exp_path2]
    exp_dirflags = [False, True]

    # run iteration
    results = []
    dirs = []
    diffs = []
    dirflags = []
    for entry in diffcache:
        results.append(entry)
        dirs.append(entry[0])
        diffs.append(entry[1])
        dirflags.append(entry[2])
    # sort to unify testing for all Operating Systems
    # Linux will list the directories first, before listing files
    dirs.sort()
    dirflags.sort()

    # check if diffs is correct
    if type(diffs[0]) == diff.Diff and type(diffs[1]) == diff.DiffCache:
        dir_check = True
    elif type(diffs[0]) == diff.DiffCache and type(diffs[1]) == diff.Diff:
        dir_check = True
    else:
        dir_check = False

    assert dirs == exp_paths
    assert dir_check
    assert dirflags == exp_dirflags


def test_diff_log_deserialize_str():
    arch = abspath("./tests/testdata/full_archive/arch1.zip")
    diff_log = pybacked.zip_handler.read_diff_log(arch)

    # create expected variables
    expected = pybacked.diff.DiffCache(nested=False)
    diff1 = pybacked.diff.Diff('+', '1')
    path1 = abspath("./tests/testdata/full_storage/doc1.txt")
    diff2 = pybacked.diff.Diff('+', '2')
    path2 = abspath("./tests/testdata/full_storage/subdir/doc2.txt")
    diff3 = pybacked.diff.Diff('+', '3')
    path3 = abspath("./tests/testdata/full_storage/subdir/doc3.txt")
    diff4 = pybacked.diff.Diff('+', '4')
    path4 = abspath("./tests/testdata/full_storage/subdir/subdir/doc4.txt")
    expected.add_diff(path1, diff1, False)
    expected.add_diff(path2, diff2, False)
    expected.add_diff(path3, diff3, False)
    expected.add_diff(path4, diff4, False)

    basepath = abspath("./tests/testdata/full_storage")
    result = pybacked.diff.diff_log_deserialize_str(diff_log, basepath)

    print(result.diffdict)
    print(expected.diffdict)

    assert result == expected
