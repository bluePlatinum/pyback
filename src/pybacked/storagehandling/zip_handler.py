import io
import os
import zipfile


def zip_write(archivepath, filedict, compression, compressionlevel):
    """
    Write filedict to zip-archive. Will check wether file at filepath exists
    before writing. If file exists will return False, else will return True
    after complete write.

    :param filepath: the path to the file
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
            archive.write(filepath, arcname=filename)
    archive.close()


def read_bin(archivepath, filelist):
    """
    Read a list of files from an archive and return the file data as a
    dictionary of filename, data key-value pairs.

    :param archivepath: the path to the archive
    :param filename: list of filenames to read
    :return: dictionary with filename, data key-value pairs
    """
    datadict = dict()
    if os.path.isfile(archivepath):
        archive = zipfile.ZipFile(archivepath, mode='r')
    else:
        raise FileNotFoundError("Specified file does not exist")
    for filename in filelist:
        try:
            buffer = archive.open(filename)
            wrapper = io.TextIOWrapper(buffer, newline=None)

            datadict[filename] = wrapper.read()

            wrapper.close()
            buffer.close()
        except KeyError:
            datadict[filename] = None
    archive.close()
    return datadict


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
