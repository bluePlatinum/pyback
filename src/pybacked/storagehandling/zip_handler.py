import os
import zipfile


def zip_write(archivepath, filedict, compression, compressionlevel):
    """Write filedict to zip-archive. Will check wether file at filepath exists
    before writing. If file exists will return False, else will return True
    after complete write.

    :param filepath: the path to the file
    :param filedict: dictionary containing the filepath, filename key-value
    pairs
    :param compression: desired compression methods (see zipfile documentation)
    :param compressionlevel: compression level (see zipfile documentation)
    :return:
    """
    if os.path.isfile(archivepath):
        return False
    else:
        archive = zipfile.ZipFile(archivepath, mode='x',
                                  compression=compression,
                                  compresslevel=compressionlevel)
        for filepath, filename in filedict:
            archive.write(filepath, arcname=filename)
    return True
