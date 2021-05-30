class DiffCache:
    """
    Used to hold file difference information.

    :param initialdict: initial dictionary which will be copied into diffdict
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

        :param filename: the filename of the diff to be added
        :type filename: str
        :param diffobj: the diff-object which will hold different information
                depending on the diff-detection algorithm
        :type diffobj: diff object
        :return: void
        """
        self.diffdict[filename] = diffobj

    def remove_diff(self, filename):
        """
        Remove a diff reference from diffdict

        :param filename: the filename of the diff to be removed
        :type filename: str
        :return: the diff under the filename key
        :rtype: diff object
        """
        return self.diffdict.pop(filename)
