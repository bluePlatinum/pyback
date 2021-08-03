import os.path
import pybacked
import pybacked.backup
import pybacked.config
import pybacked.diff
import pybacked.logging
import shutil
import tempfile
import zipfile


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

    result = pybacked.backup.create_filedict(diffcache)
    print("Expected: ", expected)
    print("Result: ", result)
    assert result == expected


def test_get_archive_name():
    archive_path = os.path.abspath("./tests/testdata/archive_date")
    result = pybacked.backup.get_new_archive_name(archive_path)
    expected = "arch4.zip"
    assert result == expected


def test_backup():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = os.path.abspath(tmpdir + "/storage")
        archive = os.path.abspath(tmpdir + "/archive")
        # os.mkdir(storage)
        # os.mkdir(archive)
        full_storage = os.path.abspath("./tests/testdata/full_storage")
        full_archive = os.path.abspath("./tests/testdata/full_archive")

        # copy contents of full_storage to tmpdir
        shutil.copytree(full_storage, os.path.abspath(storage))
        shutil.copytree(full_archive, os.path.abspath(archive))

        # create configuration object
        config = pybacked.config.Configuration("test1", storage, archive,
                                               pybacked.DIFF_DATE,
                                               zipfile.ZIP_DEFLATED, 9)

        # create expected variables
        expected_diffcache = pybacked.diff.collect(storage, archive,
                                                   pybacked.DIFF_DATE)
        expected_log = pybacked.logging.create_log(expected_diffcache)

        # perform a backup
        pybacked.backup.backup(config)

        # test wether the files were backed up successfully (multiple stages)
        new_archive = os.path.abspath(archive + "/arch2.zip")

        # STAGE 1: was the new archive created?
        assert os.path.isfile(new_archive)

        # STAGE 2: check if files are identical to the files in storage
        doc1_file = open(os.path.abspath(tmpdir + "/storage/doc1.txt"), 'rb')
        doc2_file = open(os.path.abspath(
            tmpdir + "/storage/subdir/doc2.txt"), 'rb')
        doc3_file = open(os.path.abspath(
            tmpdir + "/storage/subdir/doc3.txt"), 'rb')
        doc4_file = open(os.path.abspath(
            tmpdir + "/storage/subdir/subdir/doc4.txt"), 'rb')
        doc1 = doc1_file.read()
        doc2 = doc2_file.read()
        doc3 = doc3_file.read()
        doc4 = doc4_file.read()
        doc1_file.close()
        doc2_file.close()
        doc3_file.close()
        doc4_file.close()

        arch = zipfile.ZipFile(new_archive, mode='r')
        doc1_arch_file = arch.open("doc1.txt", 'r')
        doc2_arch_file = arch.open("subdir/doc2.txt", 'r')
        doc3_arch_file = arch.open("subdir/doc3.txt", 'r')
        doc4_arch_file = arch.open("subdir/subdir/doc4.txt", 'r')
        doc1_arch = doc1_arch_file.read()
        doc2_arch = doc2_arch_file.read()
        doc3_arch = doc3_arch_file.read()
        doc4_arch = doc4_arch_file.read()
        doc1_arch_file.close()
        doc2_arch_file.close()
        doc3_arch_file.close()
        doc4_arch_file.close()
        arch.close()

        assert doc1 == doc1_arch
        assert doc2 == doc2_arch
        assert doc3 == doc3_arch
        assert doc4 == doc4_arch

        # STAGE 3: diff log
        arch = zipfile.ZipFile(new_archive, mode='r')
        print(arch.namelist())
        diff_log_file = arch.open("diff-log.txt", 'r')
        diff_log = diff_log_file.read()
        diff_log_file.close()
        arch.close()
        assert diff_log == expected_log.encode()
