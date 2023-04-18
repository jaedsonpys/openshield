import os
import typing
import hashlib
from configparser import ConfigParser
from datetime import datetime, timedelta
from pathlib import Path
from zipfile import ZipFile

import requests

HOME_USER = Path.home()
OPENSHIELD_DIR = os.path.join(HOME_USER, '.openshield')
CONFIG_FILEPATH = os.path.join(OPENSHIELD_DIR, 'openshield.ini')
HASH_DATA_PATH = os.path.join(OPENSHIELD_DIR, 'hashes.openshield.zip')

# This project uses MalwareBazaar (https://bazaar.abuse.ch/)
# to get malware MD5 hash list.
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

    def scan_files(self, filepaths: list) -> typing.List[typing.Tuple[str]]:
        database = self.load_database()
        malwares = []

        for file in filepaths:
            with open(file, 'rb') as _file:
                file_hash = hashlib.md5(_file.read()).hexdigest()

            if file_hash in database:
                malwares.append((file, file_hash))

        return malwares

    def load_database(self) -> typing.Generator:
        with ZipFile(HASH_DATA_PATH) as _zip:
            hash_txt = _zip.read('full_md5.txt')
            filelines = hash_txt.split(b'\r\n')
            _zip.close()

        for _hash in filelines[9:]:
            yield _hash.decode()

    def require_hashes_update(self) -> bool:
        """Checks if it is necessary to use the
        `update_database` method. If the last database
        update was an hour ago, the function will return `True`.

        :return: If an update is required
        :rtype: bool
        """

        config = self._config['DEFAULT']
        last_update = datetime.strptime(config['lastUpdate'], '%Y-%m-%d %H:%M:%S')
        return datetime.now() >= (last_update + timedelta(hours=1))

    def update_database(self) -> None:
        """Update hash database.

        The website [MalwareBazaar](https://bazaar.abuse.ch/export)
        reports that the hashes are updated every **one hour**. Please
        consider using this method every hour.
        """

        response = requests.get(MD5_HASH_DOWNLOAD_URL)
        
        with open(HASH_DATA_PATH, 'wb') as _zip:
            _zip.write(response.content)

        last_update = datetime.now()
        self._config['DEFAULT']['lastUpdate'] = last_update.replace(microsecond=0)
