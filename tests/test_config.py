import json
import os
import pybacked.config
import tempfile


class TestConfigurationClass:
    def test_constructor(self):
        instance = pybacked.config.Configuration("1", "2", "3", 4, 5, 6,
                                                 hash_algorithm=7)
        assert instance.name == "1"
        assert instance.storage == "2"
        assert instance.archive == "3"
        assert instance.diff_algorithm == 4
        assert instance.compression_algorithm == 5
        assert instance.compresslevel == 6
        assert instance.hash_algorithm == 7

    def test_get_dict(self):
        instance = pybacked.config.Configuration("1", "2", "3", 4, 5, 6,
                                                 hash_algorithm=7)

        # create expected dictionary
        expected = {"name": "1", "storage": "2", "archive": "3",
                    "diff_algorithm": 4, "compression_algorithm": 5,
                    "compresslevel": 6, "hash_algorithm": 7}

        result = instance.get_dict()
        assert result == expected


def test_serialize_config():
    instance = pybacked.config.Configuration("1", "2", "3", 4, 5, 6,
                                             hash_algorithm=7)
    expected = json.dumps(instance.get_dict())
    result = pybacked.config.serialize_config(instance)
    assert result == expected


def test_serialize_config_list():
    instance1 = pybacked.config.Configuration("1", "2", "3", 4, 5, 6,
                                              hash_algorithm=7)
    instance2 = pybacked.config.Configuration("8", "9", "10", 11, 12, 13,
                                              hash_algorithm=14)
    config_list = [instance1, instance2]

    # create expected
    config_dict = dict()
    for element in config_list:
        config_dict[element.name] = element.get_dict()
    expected = json.dumps(config_dict)

    result = pybacked.config.serialize_config_list(config_list)
    assert result == expected


def test_write_string():
    instance1 = pybacked.config.Configuration("1", "2", "3", 4, 5, 6,
                                              hash_algorithm=7)
    instance2 = pybacked.config.Configuration("8", "9", "10", 11, 12, 13,
                                              hash_algorithm=14)
    config_list = [instance1, instance2]

    # create expected file content
    expected = pybacked.config.serialize_config_list(config_list)

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.abspath(tmpdir + "/custom.json")

        # perform file write
        pybacked.config.write_config(config_list, file_path)

        file = open(file_path, 'r')
        file_content = file.read()
        file.close()

        assert file_content == expected
