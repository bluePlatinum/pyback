import os
import shutil
import tempfile
import zipfile


def archive_write(archivepath, data, filename, compression, compressionlevel):
    """
    Create a file named filename in the archive and write data to it

    :param archivepath: The path to the zip-archive
    :type archivepath: str
    :param data: The data to be written to the file
    :type data: str
    :param filename: The filename for the newly created file
    :type filename: str
    :param compression: The desired compression for the zip-archive
    :type compression: int
    :param compressionlevel: The desired compression level for the zip-archive
    :type compressionlevel: int
    :return: void
    """
    archive = zipfile.ZipFile(archivepath, mode='a',
                              compression=compression,
                              compresslevel=compressionlevel)
    archive.writestr(filename, data)
    archive.close()


def create_archive(archivepath, filedict, compression, compressionlevel):
    """
    Write filedict to zip-archive data subdirectory. Will check wether archive
    at archivepath exists before writing. If file exists will raise a
    FileExistsError.

    :param archivepath: the path to the file
    :param filedict: dictionary containing the filepath, filename key-value
            pairs
    :param compression: desired compression methods (see zipfile documentation)
    :param compressionlevel: compression level (see zipfile documentation)
    :return: void
    """
    if os.path.isfile(archivepath):
        raise FileExistsError("Specified file already exists")
    else:
        archive = zipfile.ZipFile(archivepath, mode='x',
                                  compression=compression,
                                  compresslevel=compressionlevel)
        for filepath, filename in filedict.items():
            archive.write(filepath, arcname="data/" + filename)
    archive.close()


def extract_archdata(archivepath, filename, destination):
    """
    Extract a file from a archive and write it to the destination. If the
    destination path already exists extract_archdata will not overwrite but
    will throw a "FileExists" error.

    :param archivepath: The path to the archive containing the file
    :type archivepath: str
    :param filename: The archive name of the desired file.
    :type filename: str
    :param destination: The path at which the extracted file is to be placed.
    :type destination: str
    :return: void
    :rtype: None
    """
    # check if destination path already exists
    if os.path.exists(destination):
        raise FileExistsError("The specified destination is already in use")
    archive = zipfile.ZipFile(archivepath, mode='r')
    with tempfile.TemporaryDirectory() as tmpdir:
        archive.extract(filename, path=tmpdir)

        # create directories for the destination
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        shutil.copy(os.path.abspath(tmpdir + "/" + filename), destination)


def read_bin(archivepath, filelist):
    """
    Read a list of files from an archive and return the file data as a
    dictionary of filename, data key-value pairs.

    :param archivepath: the path to the archive
    :param filelist: list of filenames to read
    :return: dictionary with filename, data key-value pairs
    :rtype: dict
    """
    datadict = dict()
    if os.path.isfile(archivepath):
        archive = zipfile.ZipFile(archivepath, mode='r')
    else:
        raise FileNotFoundError("Specified file does not exist")
    for filename in filelist:
        try:
            file = archive.open(filename)

            datadict[filename] = file.read().decode()

            file.close()
        except KeyError:
            datadict[filename] = None
    archive.close()
    return datadict


def read_diff_log(archivepath):
    """
    Read the diff-log.csv from a given archive file.

    :param archivepath: The path to the zip-archive
    :type archivepath: str
    :return: The diff-log.csv contents in ascii string form.
    :rtype: str
    """
    arch = zipfile.ZipFile(archivepath, mode='r')
    diff_log_file = arch.open("diff-log.csv")
    diff_log_bin = diff_log_file.read()
    diff_log = diff_log_bin.decode()
    diff_log_file.close()
    arch.close()
    return diff_log


def zip_extract(archivepath, filelist, extractpath):
    """
    Extract a list of files to a specific location

    :param archivepath: the path to the zip-archive
    :param filelist: list of member filenames to extract
    :param extractpath: path for the extracted files
    :return: void
    """
    if os.path.isfile(archivepath):
        archive = zipfile.ZipFile(archivepath, mode='r')
    else:
        raise FileNotFoundError("Specified file does not exist")
    archive.extractall(path=extractpath, members=filelist)
    archive.close()
