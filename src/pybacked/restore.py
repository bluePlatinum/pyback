import os


def get_archive_list(archivedir):
    """
    Return a list of paths to all the backup archives.
    :param archivedir:
    :return: a list of paths to all the backup archives
    :rtype: list
    """
    raw_list = os.listdir(archivedir)
    final_list = []
    for member in raw_list:
        if os.path.isfile(os.path.abspath(archivedir + '/' + member)):
            if member.find(".zip") > -1:
                final_list.append(os.path.abspath(archivedir + '/' + member))
    return final_list


def get_last_state(filename, archivedir, diff_detection_type):
    """
    Get the last state of the archived files
    :param filename: the name of the file
    :type filename: str
    :param archivedir: the directory of the backup archive
    :type archivedir: str
    :param diff_detection_type: the diff algorithm used to detect changes to
            the file
    :type diff_detection_type: int
    :return: the last state of the object (ie. last edited date, hash, etc.)
    """
    # populate as soon as you can!
    # this is just created to have a signature for the function
    pass
