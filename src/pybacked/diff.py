import csv
import io
import os
import pybacked.zip_handler
from pybacked import DIFF_HASH
from pybacked import restore


class DiffCache:
    """
    A collection of diff classes, which hold information on file version
    differences. For example DiffCache objects are used to collect Diff objects
    for all files in a directory, in order to have them in one easily acessible
    and versatile "Container"

    :param initialdict: Initial dictionary which will be copied into diffdict
    :type initialdict: dict, optional
    :param initialdirflags: Initial dir flags dictionary
    :type initialdirflags: dict, optional
    :param nested: Indicates wether the DiffCache is nested, meaning that the
        DiffCache itself can contain DiffCaches. (default is True)
    :type nested: bool, optional
    """
    def __init__(self, initialdict=None, initialdirflags=None, nested=True):
        if initialdict is None:
            self.diffdict = dict()
        else:
            self.diffdict = initialdict

        if initialdirflags is None:
            self.dirflags = dict()
        else:
            self.dirflags = initialdirflags
        self.nested = nested

    def __eq__(self, other):
        """
        Overrides the == operator to check whether the dictioaries are equal.
        This is mainly used to simplify testing.

        :param other: The other DiffCache class
        :type other: DiffCache
        :return: True if dictionaries match - False if dictionaries don't match
        :rtype: bool
        """
        checks = []

        if self.diffdict == other.diffdict:
            checks.append(True)
        else:
            checks.append(False)

        if self.dirflags == other.dirflags:
            checks.append(True)
        else:
            checks.append(False)

        return checks == [True, True]

    def __iter__(self):
        """
        Used for Iteration. This method creates a list of all the file names,
        which will then be used by __next__() to iterate over the dictionries.

        :return: self
        """
        self.index = 0
        self.pathlist = []
        for filepath, diff in self.diffdict.items():
            self.pathlist.append(filepath)
        return self

    def __next__(self):
        """
        Iterate over the DiffCache. This will iterate through the diffdict and
        the dirflags and return a list as [filepath, diffentry, dirflag] for
        each diffdict/dirflags entry.

        :return: [filepath, diffentry, dirflag] for each filepath
        :rtype: List
        """
        try:
            current_path = self.pathlist[self.index]
            diffentry = self.diffdict[current_path]
            dirflag = self.dirflags[current_path]
            self.index += 1
            return [current_path, diffentry, dirflag]
        except IndexError:
            # clean up the variables created by __iter__()
            del self.index
            del self.pathlist

            raise StopIteration

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

    def __eq__(self, other):
        """
        Check if Diff object hold same values.
        This is mostly used for testing purposes.

        :param other: The other Diff object
        :type other: Diff
        :return: True if the objects hold the same values - False if they dont
        :rtype: bool
        """
        checks = []

        if self.difftype == other.difftype:
            checks.append(True)
        else:
            checks.append(False)

        if self.state == other.state:
            checks.append(True)
        else:
            checks.append(False)

        return checks == [True, True]


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
    :rtype: Diff
    """
    if diff_algorithm == DIFF_HASH and hash_algorithm is None:
        raise ValueError("No hash algorithm selected")

    if subdir == "":
        filename = os.path.basename(filepath)
    else:
        filename = subdir + "/" + os.path.basename(os.path.abspath(filepath))

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
    :param diff_algorithm: The desired diff algorithm - one of (DIFF_DATE,
        DIFF_HASH, DIFF_CONT)
    :type diff_algorithm: int
    :param hash_algorithm: The desired hash algorithm.
    :type hash_algorithm: str
    :param subdir: The subdirectory prefix for the filename
    :type subdir: str, optional
    :return: The DiffCache object holding the diff information
    :rtype: DiffCache
    """
    # check if hash algorithm is set
    if diff_algorithm == DIFF_HASH and hash_algorithm is None:
        raise ValueError("No hash algorithm selected")

    diff_cache = DiffCache()

    for member in os.listdir(storage_dir):
        member_path = os.path.abspath(storage_dir + "/" + member)
        # if member is a directory run cullect() on said dir
        if os.path.isdir(member_path):
            new_subdir = os.path.join(subdir, os.path.basename(member_path))
            # os.path.join adds backslashes(\\) and these need to be replaced
            # as the diff logs in the archives only use slashes(/)
            new_subdir = new_subdir.replace("\\", "/")

            diff = collect(member_path, archive_dir, diff_algorithm,
                           hash_algorithm, new_subdir)
            diff_cache.add_diff(member_path, diff, True)
        # if member is a file detect the differences and add them to diff_cache
        else:
            diff = detect(member_path, archive_dir, diff_algorithm,
                          hash_algorithm, subdir)
            if diff is not None:
                diff_cache.add_diff(member_path, diff, False)
    return diff_cache


def diff_log_deserialize(archive, basepath):
    """
    Read a diff-log.csv from a given archive and create a DiffCache from the
    contents of the diff-log.

    :param archive: The path to the zip-archive
    :type archive: str
    :param basepath: The path to the storage location. This is required as the
        diff-log.csv only stores the relative filenames.
    :type basepath: str
    :return: The deserialized DiffCache object
    :rtype: DiffCache
    """
    diff_log = pybacked.zip_handler.read_diff_log(archive)
    diffcache = diff_log_deserialize_str(diff_log, basepath)
    return diffcache


def diff_log_deserialize_str(diff_log, basepath=None):
    """
    Create a DiffCache object from a given string.

    :param diff_log: A String containing the contents of the diff-log.csv
    :type diff_log: str
    :param basepath: The path to the storage location. This is required as the
        diff-log.csv only stores the relative filenames. If basepath is None
        diff_log_deserialize_str will use the the archive relative paths, just
        like in the diff-log.csv
    :type basepath: str, optional
    :return: The deserialized DiffCache object
    :rtype: DiffCache
    """
    deserialized = DiffCache(nested=False)
    wrapper = io.StringIO(diff_log)
    reader = csv.DictReader(wrapper)
    for entry in reader:
        diff_obj = Diff(entry['modtype'], entry['diff'])
        if basepath is None:
            full_file_path = entry['filename']
        else:
            full_file_path = os.path.abspath(
                basepath + "/" + entry['filename'])
        deserialized.add_diff(full_file_path, diff_obj, False)
    return deserialized
