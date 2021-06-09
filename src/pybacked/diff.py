import os
from pybacked import DIFF_HASH
from pybacked import restore


class DiffCache:
    """
    Used to hold file difference information.

    :param initialdict: Initial dictionary which will be copied into diffdict
    :type initialdict: dict, optional
    :param initialdirflags: Initial dir flags dictionary
    :type initialdirflags: dict, optional
    """
    def __init__(self, initialdict=None, initialdirflags=None):
        if initialdict is None:
            self.diffdict = dict()
        else:
            self.diffdict = initialdict

        if initialdirflags is None:
            self.dirflags = dict()
        else:
            self.dirflags = initialdirflags

    def add_diff(self, location, diffobj, is_dir):
        """
        Add a diff reference to diffdict and dirflags.

        :param location: The name of the inspected location (dir or file)
        :type location: str
        :param diffobj: The diff-object which will hold different information
                depending on the diff-detection algorithm
        :type diffobj: Diff object
        :param is_dir: Flag to be set if the added location is a dir
        :type is_dir: bool
        :return: void
        :rtype: None
        """
        self.diffdict[location] = diffobj
        self.dirflags[location] = is_dir

    def remove_diff(self, location):
        """
        Remove a diff reference from diffdict and dirflags.

        :param location: The location-name of the diff to be removed
        :type location: str
        :return: the diff and the dir-flag under the location-name key
        :rtype: Diff object, bool
        """
        removed_diff = self.diffdict.pop(location)
        removed_flag = self.dirflags.pop(location)
        return removed_diff, removed_flag


class DiffDate:
    """
    LEGACY CODE
    Holds data to describe differences between file-versions detected by
    comparing last edited date.

    :param difftype_: The type of difference that was detetcted.
            '+' - file was created
            '-' - file was deleted
            '*' - file was edited
    :type difftype_: str
    :param last_edit_: The unix timestamp of the last edit.
    :type last_edit_: float
    :param previous_edit_: The last edited date (unix-timestamp) of the
            last file-version which was archived
    :type previous_edit_: float
    """
    def __init__(self, difftype_, last_edit_, previous_edit_=None):
        self.difftype = difftype_
        self.last_edit = last_edit_
        self.previous_edit = previous_edit_


class DiffHash:
    """
    LEGACY CODE
    Holds data to describe differences between file-versions detected by
    comparing binary hashes.

    :param difftype_: The type of difference that was detetcted.
            '+' - file was created
            '-' - file was deleted
            '*' - file was edited
    :type difftype_: str
    :param currenthash_: the hash of the modified file
    :type currenthash_: bytes object
    :param hash_algorithm_: the applied hash algorithm
    :type hash_algorithm_: str
    """
    def __init__(self, difftype_, currenthash_, hash_algorithm_):
        self. difftype = difftype_
        self.currenthash = currenthash_
        self.hash_algorithm = hash_algorithm_


class Diff:
    """
    Holds data to define differences between file-versions

    :param difftype_: The type of difference that was detetcted.
            '+' - file was created
            '-' - file was deleted
            '*' - file was edited
    :type difftype_: str
    :param state: The newer state of the file. Depending on the
            diff-algorithm used can either be a timestamp or a hex hash
    :type state: float or str
    """
    def __init__(self, difftype_, state):
        self.difftype = difftype_
        self.state = state


def detect(filepath, archive_dir, diff_algorithm, hash_algorithm=None,
           subdir=""):
    """
    Detect difference between a working file and an archived file. Meaning
    this function detects whether there has been a change in the file since
    the last archiving cycle

    :param filepath: The path of the inspected file
    :type filepath: str
    :param archive_dir: The directory of the archive
    :type archive_dir: str
    :param diff_algorithm: The diff-detection algorithm used - one of DIFF_DATE
            or DIFF_HASH
    :type diff_algorithm: int
    :param hash_algorithm: The desired hashing algorithm
    :type hash_algorithm: str
    :param subdir: The subdirectory prefix for the filename
    :type subdir: str, optional
    :return: The diff class which corresponds to the file change or None if the
            file didn't change.
    """
    if diff_algorithm == DIFF_HASH and hash_algorithm is None:
        raise ValueError("No hash algorithm selected")

    filename = subdir + os.path.basename(os.path.abspath(filepath))

    arch_state = restore.get_arch_state(filename, archive_dir,
                                        diff_algorithm)
    current_state = restore.get_current_state(filepath, diff_algorithm,
                                              hash_algorithm)
    if arch_state != current_state:
        if arch_state is None:
            # if the file doesn't exist in the archives, then it was added
            diff_type = "+"
        elif current_state is None:
            # if the file doesn't exist in the current state, then it was
            # removed
            diff_type = '-'
        else:
            # if the file existed in both archive and current, then it was
            # edited
            diff_type = '*'
        return Diff(diff_type, current_state)
    else:
        return None


def collect(storage_dir, archive_dir, diff_algorithm, hash_algorithm=None,
            subdir=""):
    """
    Collects all the diff information for an entire storage directory.

    :param storage_dir: The storage directory
    :type storage_dir: str
    :param archive_dir: The archive directory
    :type archive_dir: str
    :param diff_algorithm: The desired diff algorithm - one of DIFF_DATE or
            DIFF_HASH
    :type diff_algorithm: int
    :param hash_algorithm: The desired hash algorithm.
    :type hash_algorithm: str
    :param subdir: The subdirectory prefix for the filename
    :type subdir: str, optional
    :return: The DiffCache object holding the diff information
    """
    # check if hash algorithm is set
    if diff_algorithm == DIFF_HASH and hash_algorithm is None:
        raise ValueError("No hash algorithm selected")

    diff_cache = DiffCache()

    for member in os.listdir(storage_dir):
        member_path = os.path.abspath(storage_dir + "/" + member)
        # if member is a directory run cullect() on said dir
        if os.path.isdir(member_path):
            new_subdir = subdir + os.path.basename(member_path)

            diff = collect(member_path, archive_dir, diff_algorithm,
                           hash_algorithm, new_subdir),
            diff_cache.add_diff(member_path, diff, True)
        # if member is a file detect the differences and add them to diff_cache
        else:
            diff = detect(member_path, archive_dir, diff_algorithm,
                          hash_algorithm, subdir)
            diff_cache.add_diff(member_path, diff, False)
    return diff_cache
