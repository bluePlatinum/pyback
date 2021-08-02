import os.path
import pybacked
import pybacked.control
import pybacked.diff


def test_create_filedict():
    # create DiffCache object from full_storage/archive
    storage = os.path.abspath("./tests/testdata/full_storage")
    archive = os.path.abspath("./tests/testdata/full_archive")
    diffcache = pybacked.diff.collect(storage, archive, pybacked.DIFF_DATE)

    # create expected dictionary
    doc1 = os.path.abspath("./tests/testdata/full_storage/doc1.txt")
    doc2 = os.path.abspath("./tests/testdata/full_storage/subdir/doc2.txt")
    doc3 = os.path.abspath("./tests/testdata/full_storage/subdir/doc3.txt")
    doc4 = os.path.abspath(
        "./tests/testdata/full_storage/subdir/subdir/doc4.txt")
    expected = {doc1: "doc1.txt", doc2: "subdir/doc2.txt",
                doc3: "subdir/doc3.txt", doc4: "subdir/subdir/doc4.txt"}

    result = pybacked.control.create_filedict(diffcache)
    print("Expected: ", expected)
    print("Result: ", result)
    assert result == expected
