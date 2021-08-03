import os.path
import pybacked.restore


def create_filedict(diffcache, subdir=""):
    """
    Create a dictionary of filepath, filename key-value pairs for each enty
    (and subdirectory-entry) in the DiffCache. Here the filename refers to the
    name that the file is given in the archive and is derived from the
    basename of the path.

    :param diffcache: The DiffCache from which the dictionary should be
        created.
    :type diffcache: DiffCache
    :param subdir: A subdirectory prefix, which will be prepended to the
        filenames. This is mainly used for recursion.
    :type subdir: str
    :return: Returns a dictionary of filepath, filename key-value pairs which,
        can be passed to zip_handler.archive_write().
    :rtype: dict
    """
    dictionary = {}
    for element in diffcache:
        if element[2]:
            sub_path = subdir + os.path.basename(element[0]) + "/"
            sub_dict = create_filedict(element[1], subdir=sub_path)
            for path, filename in sub_dict.items():
                dictionary[path] = filename
        else:
            dictionary[element[0]] = subdir + os.path.basename(element[0])
    return dictionary


def get_new_archive_name(archive_dir):
    """
    Checks for existing archives and returns the name of the next archive to
    be created.

    :param archive_dir: The directory in which the archives are located
    :type archive_dir: str
    :return: Returns the name, that the next archive should have
    :rtype: str
    """
    archive_list = pybacked.restore.get_archive_list(archive_dir)
    last_archive = os.path.basename(archive_list[0])
    archive_number = int(last_archive.split('.')[0][-1]) + 1
    archive_name = "arch" + str(archive_number) + ".zip"
    return archive_name
