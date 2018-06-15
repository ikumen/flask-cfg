import pytest

from .. import SimpleConfig

default_conf_paths = 'flask_cfg/tests/default.yaml'
override_conf_paths = 'flask_cfg/tests/override.yaml'
secret_conf_paths = 'flask_cfg/tests/secret.yaml'

def test_should_load_default_config():
    config = SimpleConfig(default_conf_paths=default_conf_paths)

    # validate loading config values in general
    assert hasattr(config, 'FOO') and getattr(config, 'FOO') == 'ack'
    assert hasattr(config, 'DEBUG') and getattr(config, 'DEBUG') is False

    # validate ignoring all non-uppercase config values
    assert hasattr(config, 'FOO') and hasattr(config, 'DEBUG') \
        and not hasattr(config, 'ignore_me')

    # validate loading list values
    assert hasattr(config, 'CURRENCIES') \
        and getattr(config, 'CURRENCIES')[0]['NAME'] == 'Bitcoin' \
        and getattr(config, 'CURRENCIES')[1]['NAME'] == 'Ethereum' 


def test_should_load_config_with_overrides():
    config = SimpleConfig(default_conf_paths=default_conf_paths,
        override_conf_paths=override_conf_paths)

    # make sure file specific configs are loaded
    assert hasattr(config, 'FOO') and hasattr(config, 'DEBUG') \
        and hasattr(config, 'A') and hasattr(config, 'B')
    
    # default FOO == 'ack' overriden with 'bar'
    assert getattr(config, 'FOO') == 'bar' 

def test_should_load_config_with_override_n_secrets():
    config = SimpleConfig(default_conf_paths=default_conf_paths,
        override_conf_paths=override_conf_paths,
        secret_conf_paths=secret_conf_paths)

    assert hasattr(config, 'FOO') and hasattr(config, 'DEBUG') \
        and hasattr(config, 'A') and hasattr(config, 'B') \
        and hasattr(config, 'SECRET') and hasattr(config, 'ANOTHER_SECRET')
    
    assert getattr(config, 'SECRET') == '*****'
    assert getattr(config, 'ANOTHER_SECRET') == 1234


