import io
import os.path as osp
import tempfile
import zipfile

from pybacked import zip_handler


def test_archive_write():
    with tempfile.TemporaryDirectory() as tmpdir:
        archivepath = tmpdir + "/archive.zip"
        zip_handler.archive_write(archivepath, "Hello", "file1.txt",
                                  compression=zipfile.ZIP_DEFLATED,
                                  compressionlevel=9)
        # check if data was written properly
        archive = zipfile.ZipFile(archivepath, mode='r')
        file = archive.open("file1.txt")
        wrapper = io.TextIOWrapper(file, newline=None)
        result = wrapper.read()
        wrapper.close()
        file.close()
        archive.close()

    assert result == "Hello"


def test_create_archive():
    filedict = {osp.abspath("./tests/testdata/test_sample1.txt"):
                "test_sample1.txt"}
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_handler.create_archive(osp.abspath(tmpdir + "/probe_archive.zip"),
                                   filedict, compression=zipfile.ZIP_DEFLATED,
                                   compressionlevel=9)

        probe_archive = zipfile.ZipFile(tmpdir + "/probe_archive.zip")
        probe_data = probe_archive.read("data/test_sample1.txt")
        probe_archive.close()

        control_file = io.open("./tests/testdata/test_sample1.txt", "rb")
        control_data = control_file.read()
        control_file.close()

    assert probe_data == control_data


def test_read_bin():
    datadir = "./tests/testdata/"
    filelist = ["test_sample1.txt", "test_sample2.txt"]
    archivepath = osp.abspath(datadir + "test_archive2_deflate.zip")
    datadict = zip_handler.read_bin(archivepath, filelist)

    control_file1 = io.open(osp.abspath(datadir + filelist[0]), "rb")
    control_file1_wrapper = io.TextIOWrapper(control_file1, newline=None)
    control_data1 = control_file1_wrapper.read()
    control_file1_wrapper.close()
    control_file1.close()

    control_file2 = io.open(osp.abspath(datadir + filelist[1]), "rb")
    control_file2_wrapper = io.TextIOWrapper(control_file2, newline=None)
    control_data2 = control_file2_wrapper.read()
    control_file2_wrapper.close()
    control_file2.close()

    assertions = [False, False]
    assertions[0] = (datadict[filelist[0]] == control_data1)
    assertions[1] = (datadict[filelist[1]] == control_data2)

    assert assertions == [True, True]


def test_zip_extract():
    archivepath = "./tests/testdata/test_archive2_deflate.zip"
    filelist = ["test_sample1.txt", "test_sample2.txt"]
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_handler.zip_extract(osp.abspath(archivepath), filelist,
                                osp.abspath(tmpdir))

        assertions = [osp.isfile(osp.abspath(tmpdir + '/' + filelist[0])),
                      osp.isfile(osp.abspath(tmpdir + '/' + filelist[1]))]
    assert assertions == [True, True]


def test_read_diff_log():
    archivepath = osp.abspath("./tests/testdata/archive_hash/arch1.zip")
    expected = zip_handler.read_bin(archivepath,
                                    ['diff-log.csv'])['diff-log.csv']

    result = zip_handler.read_diff_log(archivepath)
    # replace carriage returns to prevent errors from inconsistent handling
    # of newlines
    assert result.replace("\r", "") == expected.replace("\r", "")


def test_extract_archdata():
    archive = osp.abspath("./tests/testdata/ext_test/archive/arch2.zip")
    archname = "data/subdir/doc3.txt"

    # create expected variables
    expected = zip_handler.read_bin(
        archive, ['data/subdir/doc3.txt'])['data/subdir/doc3.txt']

    with tempfile.TemporaryDirectory() as tmpdir:
        basename = "randomname.abc"
        destination = tmpdir + basename
        zip_handler.extract_archdata(archive, archname, destination)

        file = open(destination, 'rb')
        file_content = file.read()
        file.close()

        print("file_conten: ", file_content.replace(b"\r", b""))
        print("file_content: ", file_content.decode())
        print("expected: ", expected)
        print("expected: ", expected.encode())

    assert file_content.replace(b"\r", b"") == expected.encode()
