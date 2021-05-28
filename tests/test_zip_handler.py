import io
import os.path as osp
import tempfile
import zipfile

from pybacked.storagehandling import zip_handler


def test_zip_write():
    filedict = {osp.abspath("./tests/testdata/test_sample1.txt"):
                "test_sample1.txt"}
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_handler.zip_write(osp.abspath(tmpdir + "/probe_archive.zip"),
                              filedict, compression=zipfile.ZIP_DEFLATED,
                              compressionlevel=9)

        probe_archive = zipfile.ZipFile(tmpdir + "/probe_archive.zip")
        probe_data = probe_archive.read("test_sample1.txt")
        probe_archive.close()

        control_file = io.open("./tests/testdata/test_sample1.txt", "rb")
        control_data = control_file.read()
        control_file.close()

    assert probe_data == control_data
