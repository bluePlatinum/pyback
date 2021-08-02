class Configuration:
    """
    Class to hold all the data of a specific backup configuration. This can be
    seen as a collection of global variables which hold configuration data.

    :param name: The name that is given to the configuration. This is mainly a
        UI element to help the User distinguish between multiple
        configurations.
    :type name: str
    :param storage_dir: The directory on which to perform backups
    :type storage_dir: str
    :param archive_dir: The directory where for the backup-archive
    :type archive_dir: str
    :param diff_algorithm: The desired diff method. One of (DIFF_CONT,
        DIFF_DATE, DIFF_HASH)
    :type diff_algorithm: int
    :param compression_algorithm: The desired zip compression algorithm as
        given by the zipfile module.
    :type compression_algorithm: int
    :param compresslevel: The desired zip compression level. Possible Values
        vary between compression algorithms but are always between in the span
        of 1-9. More information on the compression level can be found in the
        python documentation for the zipfile module
    :type compresslevel: int
    :param hash_algorithm: The desired hashing algorithm (only needed if
        DIFF_HASH is selected as the diff method). The available options can
        be found in the __init__.py file.
    :type hash_algorithm: str, optional
    """
    def __init__(self, name, storage_dir, archive_dir, diff_algorithm,
                 compression_algorithm, compresslevel, hash_algorithm=None):
        self.name = name
        self.storage_dir = storage_dir
        self.archive_dir = archive_dir
        self.diff_algorithm = diff_algorithm
        self.compression_algorithm = compression_algorithm
        self.compresslevel = compresslevel
        self.hash_algorithm = hash_algorithm
