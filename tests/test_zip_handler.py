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
        control_archive = io.open(
            osp.abspath("./tests/testdata/test_archive1_deflate.zip"), "rb")
        control = control_archive.read()
        control_archive.close()

        probe_archive = io.open(
            osp.abspath(tmpdir + "/probe_archive.zip"), "rb")
        probe = probe_archive.read()
        probe_archive.close()

    assert control == probe
