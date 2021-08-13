import io
import os.path
import pybacked.diff
import pybacked.logging
import shutil
import tempfile
import time
import zipfile


class TestObject:
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


def test_serialize_diff():
    expected = [["file1", "+", 1], ["sub/file2", "+", 2],
                ["sub/file3", "+", 3], ["sub/sub/file4", "+", 4]]
    result = pybacked.logging.serialize_diff(TestObject.diffcache)
    assert result == expected


def test_create_log():
    expected = \
        'filename,modtype,diff\r\nfile1,+,1\r\nsub/file2,+,' \
        '2\r\nsub/file3,+,3\r\nsub/sub/file4,+,4\r\n'
    result = pybacked.logging.create_log(TestObject.diffcache)
    assert result == expected


def test_write_log():
    expected = "filename,modtype,diff\nfile1,+,1\n" \
               "sub/file2,+,2\nsub/file3,+,3\nsub/sub/file4,+,4\n"

    with tempfile.TemporaryDirectory() as tmpdir:
        archivepath = tmpdir + "/archive.zip"
        pybacked.logging.write_log(TestObject.diffcache, archivepath,
                                   zipfile.ZIP_DEFLATED, 9)
        # check if write was successfull
        archive = zipfile.ZipFile(archivepath, mode='r')
        diff_log = archive.open("diff-log.csv")
        wrapper = io.TextIOWrapper(diff_log, newline=None)
        result = wrapper.read()
        wrapper.close()
        diff_log.close()
        archive.close()

    assert result == expected


def test_create_metadata_string():
    timestamp = time.time()
    metadata = pybacked.logging.MetadataContainer(timestamp=timestamp)
    expected = "{" + f'"timestamp": {timestamp}' + "}"
    result = pybacked.logging.create_metadata_string(metadata)
    assert result == expected


def test_write_metadata():
    with tempfile.TemporaryDirectory() as tmpdir:
        timestamp = time.time()
        metadata_container = pybacked.logging.MetadataContainer(timestamp)

        # copy the archive from full archive to the tmpdir
        archive_template = os.path.abspath(
            "./tests/testdata/full_archive/arch1.zip")
        arch_path = os.path.abspath(tmpdir + "/arch1.zip")
        shutil.copy(archive_template, arch_path)

        # create expected variables
        expected_json = "{" + f'"timestamp": {timestamp}' + "}"

        # write metadata to archive
        pybacked.logging.write_metadata(metadata_container, arch_path,
                                        zipfile.ZIP_DEFLATED, 9)

        # Check if files were written successfully (multiple stages)
        # STAGE 1: Does the archive contain a file called metadata.json
        archive = zipfile.ZipFile(arch_path, mode='r')
        namelist = archive.namelist()
        archive.close()
        assert namelist.count("metadata.json") == 1

        # STAGE 2: Does metadata.json contain the correct information
        archive = zipfile.ZipFile(arch_path, mode='r')
        metadata_file = archive.open("metadata.json", mode='r')
        metadata = metadata_file.read()
        metadata_file.close()
        archive.close()
        assert metadata == expected_json.encode()


class TestMetadataContainer:
    def test_constructor_empty(self):
        instance = pybacked.logging.MetadataContainer()
        assert instance.timestamp is None

    def test_constructor_full(self):
        timestamp = time.time()
        instance = pybacked.logging.MetadataContainer(timestamp=timestamp)
        assert instance.timestamp == timestamp

    def test_equal(self):
        timestamp = time.time()
        instance1 = pybacked.logging.MetadataContainer(timestamp=timestamp)
        instance2 = pybacked.logging.MetadataContainer(timestamp=timestamp)
        assert instance1 == instance2
