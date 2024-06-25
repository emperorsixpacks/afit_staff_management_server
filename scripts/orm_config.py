import os
import yaml
import dotenv

from management_server.server.settings import DBSettings
from management_server.constants import APP_BASE_URL

db_settings = DBSettings()

ENV_LOCATION = os.path.join(APP_BASE_URL, ".env")

if db_settings.tortoise_config is None:
    CONFIG_FILE = os.path.join(APP_BASE_URL, "extras/tortoise.yml")
else:
    CONFIG_FILE = db_settings.tortoise_config

DEFAULT_CONFIG = {
    "connections": {
        "master": db_settings.database_url
    },
    "apps": {
        "models": {
            "models": ["management_server.models",  "aerich.models"],
            "default_connection": "master",
        }
    },
}


def write_config_file(path):
    """
    Open a configuration file specified by the `path` using the specified `mode`.

    Parameters:
        path (str): The path to the configuration file.
        mode (str): The mode in which the file should be opened. Default is 'r'.

    Returns:
        TextIOWrapper: The opened file object.
    """
    with open(path, mode="w", encoding="utf-8") as f:
        yaml.dump(DEFAULT_CONFIG, f)


def create_config_file():
    """
    Create a configuration file if it does not already exist.

    This function checks if the configuration file specified by `CONFIG_FILE` exists. If it does not exist,
    the function opens the file in read mode and uses the `yaml.dump()` function to write the `DEFAULT_CONFIG`
    dictionary to the file.

    Parameters:
        None

    Returns:
        None
    """
    if os.path.exists(CONFIG_FILE):
        return
    write_config_file(CONFIG_FILE)
    print("Created new config file at", CONFIG_FILE)


if __name__ == "__main__":
    create_config_file()
    dotenv.set_key(ENV_LOCATION, "TORTOISE_CONFIG", CONFIG_FILE)