from simpleconfig import load_or_create
import os.path as path

CONFIG_DEFAULTS = {
    "logging": {
        "file": {
            "file_location": "./uls.log"
        },
        "db": {
            "rethinkdb": {
                "host": "10.0.0.4",
                "port": 28015,
                "db": "uls",
                "username": "uls",
                "password": "uls",
                "timeout": '',
                "ssl": None
            },
        },
    }
}


def get_configuration(configuration_location=None, load_env=False):
    if not configuration_location:
        configuration_location = path.join(path.abspath(path.dirname(__file__)), 'configuration.json')
    return load_or_create(configuration_location, defaults=CONFIG_DEFAULTS, load_env=load_env)
