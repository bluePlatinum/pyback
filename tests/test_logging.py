import pybacked.diff
import pybacked.logging


def test_serialize_diff():
    # create diffcache to be serialized
    diff1 = pybacked.diff.Diff("+", 1)
    diff2 = pybacked.diff.Diff("+", 2)
    diff3 = pybacked.diff.Diff("+", 3)
    diff4 = pybacked.diff.Diff("+", 4)
    diffcache_sub_sub = pybacked.diff.DiffCache(
        initialdict={"sub/sub/file4": diff4},
        initialdirflags={"sub/sub/file4": False})
    diffcache_sub = pybacked.diff.DiffCache(
        initialdict={"sub/file2": diff2, "sub/file3": diff3,
                     "sub/sub": diffcache_sub_sub},
        initialdirflags={"sub/file2": False, "sub/file3": False,
                         "sub/sub": True})
    diffcache = pybacked.diff.DiffCache(
        initialdict={"file1": diff1, "sub": diffcache_sub},
        initialdirflags={"file1": False, "sub": True})

    # create expected result
    expected = [["file1", "+", 1], ["sub/file2", "+", 2],
                ["sub/file3", "+", 3], ["sub/sub/file4", "+", 4]]

    result = pybacked.logging.serialize_diff(diffcache)
    assert result == expected
