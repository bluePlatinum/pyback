import csv
import io
import os.path


def create_log(diffcache):
    """
    Create a diff-log from a given diffcache. This function only returns the
    content of the diff-log, it does not create or write the diff-file itself

    :param diffcache: The DiffCachhe object returned by diff.collect()
    :type diffcache: DiffCache
    :return: The Content of the log.
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
