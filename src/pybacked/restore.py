import csv
import os


def find_diff(logfile, filename):
    """
    Find a diff-log occurance in a file. If one exists return the diff line.
    If the filename given is not found return 0
    :param logfile: the csv log-file to be searched
    :param filename: the name of the desired file
    :return: the diff-entry or None depending if filename was found
    :rtype: dict
    """
    csv_reader = csv.DictReader(logfile, delimiter=',')
    for entry in csv_reader:
        if entry["filename"] == filename:
            return entry
    else:
        return None


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
