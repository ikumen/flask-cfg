import pytest

from mock import patch
from .. import SimpleConfig
from flask_cfg import core


default_conf_paths = 'flask_cfg/tests/default.yaml'
override_conf_paths = 'flask_cfg/tests/override.yaml'
secret_conf_paths = 'flask_cfg/tests/secret.yaml'


def test_should_load_default_config():
    config = SimpleConfig(default_conf_paths=default_conf_paths)

    # Validate loading config values in general
    assert hasattr(config, 'TRUE_VAL') and getattr(config, 'TRUE_VAL')
    assert hasattr(config, 'FALSE_VAL') and not getattr(config, 'FALSE_VAL')
    assert hasattr(config, 'INT_VAL') and getattr(config, 'INT_VAL') == 1
    assert hasattr(config, 'STR_VAL') and getattr(config, 'STR_VAL') == 'foo'
    assert hasattr(config, 'OVERRIDE_ME') and getattr(config, 'OVERRIDE_ME') == 'hello'
    assert hasattr(config, 'MAP') and 'KEY1' in getattr(config, 'MAP') \
        and getattr(config, 'MAP')['KEY1'] == 'value1'
    assert hasattr(config, 'MAP') and 'KEY2' in getattr(config, 'MAP') \
        and getattr(config, 'MAP')['KEY2'] == 'value2'
    assert hasattr(config, 'LIST') and len(getattr(config, 'LIST')) == 3 \
        and getattr(config, 'LIST')[0] == 'item1' \
        and getattr(config, 'LIST')[1] == 'item2'
    # validate ignoring all non-uppercase config values
    assert not hasattr(config, 'igNore_ME')
    # validate loading list values
    assert hasattr(config, 'MISSING_VAL') and getattr(config, 'MISSING_VAL') is None


def test_should_load_config_with_overrides():
    config = SimpleConfig(default_conf_paths=default_conf_paths,
        override_conf_paths=override_conf_paths)

    # make sure default_conf values are still loaded
    assert hasattr(config, 'TRUE_VAL') and getattr(config, 'TRUE_VAL')
    assert hasattr(config, 'FALSE_VAL') and not getattr(config, 'FALSE_VAL')
    assert hasattr(config, 'INT_VAL') and getattr(config, 'INT_VAL') == 1
    assert hasattr(config, 'STR_VAL') and getattr(config, 'STR_VAL') == 'foo'
    # validate that override val was overriden
    assert hasattr(config, 'OVERRIDE_ME') and getattr(config, 'OVERRIDE_ME') == 'goodbye'
    # validate map was overriden correctly
    assert hasattr(config, 'MAP') and 'KEY1' in getattr(config, 'MAP') \
        and getattr(config, 'MAP')['KEY1'] == 'new value1'
    assert hasattr(config, 'MAP') and 'KEY2' in getattr(config, 'MAP') \
        and getattr(config, 'MAP')['KEY2'] == 'new value2'
    assert hasattr(config, 'LIST') and len(getattr(config, 'LIST')) == 3 \
        and getattr(config, 'LIST')[0] == 'item1' \
        and getattr(config, 'LIST')[1] == 'new item2'
    # validate still ignoring all non-uppercase config values
    assert not hasattr(config, 'igNore_ME')
    # validate loading list values
    assert hasattr(config, 'MISSING_VAL') and getattr(config, 'MISSING_VAL') == 'not missing anymore'


@patch('flask_cfg.core.SimpleConfig.resolve_missing_value')
def test_should_call_resolve_missing_value(resolve_missing_value_mock):
    SimpleConfig(default_conf_paths=default_conf_paths)
    resolve_missing_value_mock.assert_called()


@patch('flask_cfg.core.SimpleConfig.on_process_loaded_configs_failure')
def test_should_fail_when_ignore_errors_is_false(on_process_loaded_configs_failure_mock):
    """Expect a raise LookupError is we have missing value and ignore_errors is False. 
    Also make sure the failure hook is called.
    """
    with pytest.raises(LookupError):
        SimpleConfig(default_conf_paths=default_conf_paths, ignore_errors=False)

    # failure hook, called when there's an error
    on_process_loaded_configs_failure_mock.assert_called_with({
        'MAP': {'KEY2': 'value2', 'KEY1': 'value1'}, 
        'STR_VAL': 'foo', 
        'INT_VAL': 1, 
        'MISSING_VAL': None, 
        'TRUE_VAL': True, 
        'LIST': ['item1', 'item2', 'item3'], 
        'OVERRIDE_ME': 'hello', 
        'FALSE_VAL': False}, ['MISSING_VAL'])


@patch('flask_cfg.core.SimpleConfig.on_process_loaded_configs_failure')
def test_should_call_post_process_loaded_config_failure_hook(on_process_loaded_configs_failure_mock):
    SimpleConfig(default_conf_paths=default_conf_paths)
    on_process_loaded_configs_failure_mock.assert_called()


@patch('flask_cfg.core.SimpleConfig.on_process_loaded_configs_complete')
def test_should_call_post_process_loaded_config_complete_hook(on_process_loaded_configs_complete_mock):
    # override_conf_paths have no missing values
    SimpleConfig(default_conf_paths=override_conf_paths)
    on_process_loaded_configs_complete_mock.assert_called()

