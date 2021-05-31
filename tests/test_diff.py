import time
from pybacked import diff, HASH_SHA1


def test_diffcache_constructor_empty():
    probe_object = diff.DiffCache()
    assert probe_object.diffdict == {}


def test_diffcache_constructor_initial():
    initial_dict = {"filename": "would be a diff object"}
    probe_object = diff.DiffCache(initialdict=initial_dict)
    assert probe_object.diffdict == initial_dict


def test_diffcache_add_diff():
    initial_dict = {"filename": "would be a diff object"}
    additional_diff = ["filename2", "would be a diff object2"]
    expected_dict = {"filename": "would be a diff object",
                     "filename2": "would be a diff object2"}
    probe_object = diff.DiffCache(initialdict=initial_dict)
    probe_object.add_diff(additional_diff[0], additional_diff[1])
    assert probe_object.diffdict == expected_dict


def test_diffcache_remove_diff_1():
    # test the return of .remove_diff()
    initial_dict = {"filename": "would be a diff object"}
    probe_object = diff.DiffCache(initialdict=initial_dict)
    assert probe_object.remove_diff("filename") == "would be a diff object"


def test_diffcache_remove_diff_2():
    # test the resulting dictionary of .remove_diff()
    initial_dict = {"filename": "would be a diff object"}
    probe_object = diff.DiffCache(initialdict=initial_dict)
    probe_object.remove_diff("filename")
    assert probe_object.diffdict == {}


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
