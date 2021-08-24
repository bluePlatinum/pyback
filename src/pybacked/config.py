import json


class Configuration:
    """
    Class to hold all the data of a specific backup configuration. This can be
    seen as a collection of global variables which hold configuration data.

    :param name: The name that is given to the configuration. This is mainly a
        UI element to help the User distinguish between multiple
        configurations.
    :type name: str
    :param storage: The directory on which to perform backups
    :type storage: str
    :param archive: The directory where for the backup-archive
    :type archive: str
    :param diff_algorithm: The desired diff method. One of (DIFF_CONT,
        DIFF_DATE, DIFF_HASH)
    :type diff_algorithm: int
    :param compression_algorithm: The desired zip compression algorithm as
        given by the zipfile module.
    :type compression_algorithm: int
    :param compresslevel: The desired zip compression level. Possible Values
        vary between compression algorithms but are always between in the span
        of 1-9. More information on the compression level can be found in the
        python documentation for the zipfile module
    :type compresslevel: int
    :param hash_algorithm: The desired hashing algorithm (only needed if
        DIFF_HASH is selected as the diff method). The available options can
        be found in the __init__.py file.
    :type hash_algorithm: str, optional
    """
    def __init__(self, name, storage, archive, diff_algorithm,
                 compression_algorithm, compresslevel, hash_algorithm=None):
        self.name = name
        self.storage = storage
        self.archive = archive
        self.diff_algorithm = diff_algorithm
        self.compression_algorithm = compression_algorithm
        self.compresslevel = compresslevel
        self.hash_algorithm = hash_algorithm

    def __eq__(self, other):
        if self.name != other.name:
            return False
        elif self.storage != other.storage:
            return False
        elif self.archive != other.archive:
            return False
        elif self.diff_algorithm != other.diff_algorithm:
            return False
        elif self.compression_algorithm != other.compression_algorithm:
            return False
        elif self.compresslevel != other.compresslevel:
            return False
        elif self.hash_algorithm != other.hash_algorithm:
            return False
        else:
            return True

    def get_dict(self):
        """
        Get a dictionary with all fields of the Configuration class
        represented as fieldname-value pairs.

        :return: Returns the dictionary of all fields of the Configuration
            class
        :rtype: dict
        """
        name = self.name
        storage = self.storage
        archive = self.archive
        diff_algorithm = self.diff_algorithm
        compression_alg = self.compression_algorithm
        compresslevel = self.compresslevel
        hash_algorithm = self.hash_algorithm

        configuration_dir = {"name": name, "storage": storage,
                             "archive": archive,
                             "diff_algorithm": diff_algorithm,
                             "compression_algorithm": compression_alg,
                             "compresslevel": compresslevel,
                             "hash_algorithm": hash_algorithm}

        return configuration_dir


def read_config(filepath):
    """
    Read the config from a given config file.

    :param filepath: The path to the config file.
    :type filepath: str
    :return: The json deserialized list.
    :rtype: list
    """
    file = open(filepath, 'r')
    file_content = file.read()
    config_list = json.loads(file_content)
    file.close()
    return config_list


def serialize_config(config):
    """
    Returns the json-serialized string from Configuration object. This string
    can then be directly written to the .json file.

    :param config: The Configuration object
    :type config: Configuration
    :return: The json-serialized string of the Configuration object
    :rtype: str
    """
    # write the fileds to variables for improved readability

    json_string = json.dumps(config.get_dict())
    return json_string


def serialize_config_list(config_list):
    """
    Serialize a list of configs. This is used so that the user has the option
    to save multiple configs in a single file.

    :param config_list: A list of Configuration class objects
    :type config_list: list
    :return: A serialized json string which can directly be written to a config
        file.
    :rtype: str
    """
    config_dict = dict()
    for element in config_list:
        config_dict[element.name] = element.get_dict()
    json_string = json.dumps(config_dict)
    return json_string


def write_config(config_list, filepath):
    """
    Get the json string returned by serialize_config_list and write it to a
    given file.

    :param config_list: A list of Configuration objects
    :type config_list: list
    :param filepath: The path to the config file, which will hold the config
        information.
    :type filepath: str
    :return: void
    :rtype: None
    """
    json_string = serialize_config_list(config_list)
    file = open(filepath, 'w')
    file.write(json_string)
