import os.path


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
