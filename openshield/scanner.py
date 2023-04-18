import os, gzip
from pathlib import Path
from configparser import ConfigParser
from datetime import datetime, timedelta

import requests

HOME_USER = Path.home()
OPENSHIELD_DIR = os.path.join(HOME_USER, '.openshield')
CONFIG_FILEPATH = os.path.join(OPENSHIELD_DIR, 'openshield.ini')
HASH_DATA_PATH = os.path.join(OPENSHIELD_DIR, 'hashes.openshield.zip')

MD5_HASH_DOWNLOAD_URL = 'https://bazaar.abuse.ch/export/txt/md5/full/'


class Scanner:
    def __init__(self) -> None:
        if not os.path.isdir(OPENSHIELD_DIR):
            os.mkdir(OPENSHIELD_DIR)

        self._config = ConfigParser()
        self._config.read(CONFIG_FILEPATH)

        if not self._config['DEFAULT']:
            self._config['DEFAULT']['lastUpdate'] = '2000-01-01 00:00:00'
            self._update_config()

    def _update_config(self) -> None:
        with open(CONFIG_FILEPATH, 'w') as _config:
            self._config.write(_config)

    def require_hashes_update(self) -> bool:
        config = self._config['DEFAULT']
        last_update = datetime.strptime(config['lastUpdate'], '%Y-%m-%d %H:%M:%S')
        return datetime.now() >= (last_update + timedelta(hours=1))

    def update_database(self) -> None:
        response = requests.get(MD5_HASH_DOWNLOAD_URL)
        
        with open(HASH_DATA_PATH, 'wb') as _zip:
            _zip.write(response.content)

        last_update = datetime.now()
        self._config['DEFAULT']['lastUpdate'] = last_update.replace(microsecond=0)
