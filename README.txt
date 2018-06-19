===========
flask-cfg
===========

A little package for loading Flask configurations from YAML files. Comes 
with an abstract class with base functionality for loading YAML base 
configurations. You can extend the base functionality to dynamically load
additional configurations (e.g. from a database). Typical usage looks like
this::

    from flask import Flask
    from flask_cfg import SimpleConfig

    app = Flask() 
    config = SimpleConfig(default_conf_paths='default.yaml', 
        override_conf_paths='some/path/staging.yaml',
        secret_conf_paths='instance/local.yaml')
    app.config.from_object(config)




