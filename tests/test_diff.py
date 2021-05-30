from pybacked.control import diff


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
