import os
from pathlib import Path
from configparser import ConfigParser
from datetime import datetime, timedelta

HOME_USER = Path.home()
CONFIG_FILEPATH = os.path.join(HOME_USER, 'openshield.ini')
HASH_DATA_PATH = os.path.join(HOME_USER, 'hashes.openshield.zip')

MD5_HASH_DOWNLOAD_URL = 'https://bazaar.abuse.ch/export/txt/md5/full/'


class Scanner:
    def __init__(self) -> None:
        self._config = ConfigParser()
        self._config.read(CONFIG_FILEPATH)

    def require_hashes_update(self) -> bool:
        config = self._config['DEFAULT']
        last_update = datetime.strptime(config['lastUpdate'], '%Y-%m-%d, %H:%M:%S')
        return datetime.now() >= (last_update + timedelta(hours=1))
