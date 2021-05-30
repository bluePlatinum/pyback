class DiffCache:
    """
    Used to hold file difference information.

    :param initialdict: Initial dictionary which will be copied into diffdict
    :type initialdict: dict, optional
    """
    def __init__(self, initialdict=None):
        if initialdict is None:
            self.diffdict = dict()
        else:
            self.diffdict = initialdict

    def add_diff(self, filename, diffobj):
        """
        Add a diff reference to diffdict

        :param filename: The filename of the diff to be added
        :type filename: str
        :param diffobj: The diff-object which will hold different information
                depending on the diff-detection algorithm
        :type diffobj: Diff object
        :return: void
        """
        self.diffdict[filename] = diffobj

    def remove_diff(self, filename):
        """
        Remove a diff reference from diffdict

        :param filename: The filename of the diff to be removed
        :type filename: str
        :return: the diff under the filename key
        :rtype: Diff object
        """
        return self.diffdict.pop(filename)


class DiffDate:
    """
    Holds data to describe differences between file-versions detected by
    comparing last edited date.

    :param filename_: The filename of the file where a diff was detected
    :type filename_: str
    :param difftype_: The type of difference that was detetcted. (ie.
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
    def __init__(self, filename_, difftype_, last_edit_, previous_edit_=None):
        self.filename = filename_
        self.difftype = difftype_
        self.last_edit = last_edit_
        self.previous_edit = previous_edit_
