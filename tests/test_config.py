import pybacked.config


def test_configuration_class():
    instance = pybacked.config.Configuration("1", "2", "3", 4, 5, 6,
                                             hash_algorithm=7)
    assert instance.name == "1"
    assert instance.storage_dir == "2"
    assert instance.archive_dir == "3"
    assert instance.diff_algorithm == 4
    assert instance.compression_algorithm == 5
    assert instance.compresslevel == 6
    assert instance.hash_algorithm == 7
