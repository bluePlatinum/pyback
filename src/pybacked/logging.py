import csv
import io
import json
import os.path
import pybacked.zip_handler


class MetadataContainer:
    """
    A container class to hold metadata of a given archive.

    :param timestamp: The timestamp at the creation of the archive
    :type timestamp: float
    """
    def __init__(self, timestamp=None):
        self.timestamp = timestamp

    def __eq__(self, other):
        """
        Overrides the == operator. This will check wether the values of the
        instance variables are identical.

        :param other: The other MetadataContainer class
        :type other: MetadataContainer
        :return: True if all values match and False if a single (or more)
            values are non-identical.
        :rtype: bool
        """
        if self.timestamp == other.timestamp:
            pass
        else:
            return False
        return True


def create_log(diffcache):
    """
    Create a diff-log from a given diffcache. This function only returns the
    content of the diff-log.txt, it does not create or write the
    diff-file itself.

    :param diffcache: The DiffCachhe object returned by diff.collect()
    :type diffcache: DiffCache
    :return: The Content of the diff-log in string form.
    :rtype: str
    """
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(['filename', 'modtype', 'diff'])
    serialized = serialize_diff(diffcache)
    for row in serialized:
        writer.writerow(row)
    stream.seek(0)
    log = stream.read()
    stream.close()
    return log


def create_metadata_string(metadata):
    """
    Create a serialized json string from the given metadata.

    :param metadata: The metadata which should be serialized.
    :type metadata: MetadataContainer
    :return: Returns the string containing the json-style metadata
    :rtype: str
    """
    top_level_object = {"timestamp": metadata.timestamp}
    json_string = json.dumps(top_level_object)
    return json_string


def serialize_diff(diffcache, subdir=""):
    """
    Serialize the information in the diffcache for csv writing. Return a list
    of rows which can be written to the csv without further processing.

    :param diffcache: The DiffCache object to be serialized
    :type diffcache: DiffCache
    :param subdir: The subdir seriaize_diff is currently working in. Mainly
        used for recursion
    :type subdir: str
    :return: A List of csv-rows (3-element-Lists)
    :rtype: List
    """
    rows = []
    for element in diffcache:
        path = subdir + os.path.basename(element[0])
        if element[2]:
            sub_list = serialize_diff(element[1], subdir=path + "/")
            for item in sub_list:
                rows.append(item)
        else:
            modtype = element[1].difftype
            diffstate = element[1].state
            rows.append([path, modtype, diffstate])
    return rows


def write_log(diffcache, archivepath, compression, compresslevel):
    """
    Writes the log created by create_log() directly to the diff-log.csv in
    the given zip-archive.

    :param diffcache: The DiffCache from which the log will be created
    :type diffcache: DiffCache
    :param archivepath: The path to the archive
    :type archivepath: str
    :param compression: The chosen compression algorithm
    :type compression: int
    :param compresslevel: The chosen compression level (0-9)
    :type compresslevel: int
    """
    log = create_log(diffcache)
    pybacked.zip_handler.archive_write(archivepath, log, "diff-log.csv",
                                       compression, compresslevel)


def write_metadata(metadata, archpath, compression, compresslevel):
    """
    Writes the metadata created by create_metadata_string to a metadata.json
    file in the archive.

    :prarm archpath: The path to the archive
    :type archpath: str
    :param metadata: The metadata to be written to the file.
    :type metadata: MetadataContainer
    :param compression: The chosen compression algorithm
    :type compression: int
    :param compresslevel: The chosen compression level (0-9)
    :type compresslevel: int
    :return: Doesn't return anything
    """
    serialized = create_metadata_string(metadata)
    pybacked.zip_handler.archive_write(archpath, serialized, "metadata.json",
                                       compression, compresslevel)
