import os
import typing
from io import BytesIO
from hashlib import md5
from configparser import ConfigParser
from datetime import datetime, timedelta
from pathlib import Path
from zipfile import ZipFile

import requests

HOME_USER = Path.home()
OPENSHIELD_DIR = os.path.join(HOME_USER, '.openshield')
CONFIG_FILEPATH = os.path.join(OPENSHIELD_DIR, 'openshield.ini')
HASH_DATA_PATH = os.path.join(OPENSHIELD_DIR, 'hashes.openshield')

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

    def load_database(self) -> typing.Generator:
        """Load MD5 hash list.

        :return: Generator of hash list
        :rtype: typing.Generator
        :yield: MD5 Hash
        :rtype: Iterator[typing.Generator]
        """

        with open(HASH_DATA_PATH) as _file:
            hash_txt = _file.read()
            filelines = hash_txt.split('\n')

        for _hash in filelines:
            yield _hash

    def scan(self, files: list) -> typing.List[typing.Tuple[str]]:
        """Scan a file list.

        This method generate a file MD5 hash and checks
        if this hash is in malware database.

        :param files: File list to check
        :type files: list
        :return: List of found malwares
        :rtype: typing.List[typing.Tuple[str]]
        """

        def _hash(filename: str):
            _hash = md5()
            b_array = bytearray(128*1024)
            mv = memoryview(b_array)

            with open(filename, 'rb', buffering=0) as f:
                for n in iter(lambda: f.readinto(mv), 0):
                    _hash.update(mv[:n])

            return _hash.hexdigest()

        database = self.load_database()
        malwares = [(file, _hash(file)) for file in files if _hash(file) in database]
        return malwares

    def require_hashes_update(self) -> bool:
        """Checks if it is necessary to use the
        `update_database` method. If the last database
        update was an hour ago, the function will return `True`.

        :return: If an update is required
        :rtype: bool
        """

        config = self._config['DEFAULT']
        last_update = datetime.strptime(config['lastUpdate'], '%Y-%m-%d %H:%M:%S')
        return datetime.now() >= (last_update + timedelta(hours=12))

    def update_database(self) -> None:
        """Update hash database.

        The website [MalwareBazaar](https://bazaar.abuse.ch/export)
        reports that the hashes are updated every **one hour**. Please
        consider using this method every hour.
        """

        response = requests.get(MD5_HASH_DOWNLOAD_URL)

        with ZipFile(BytesIO(response.content)) as _zip:
            hash_txt = _zip.read('full_md5.txt')
            _zip.close()

        with open(HASH_DATA_PATH, 'wb') as _file:
            hash_txt = hash_txt.split(b'\r\n')
            _file.write(b'\n'.join(hash_txt[9:]))

        last_update = datetime.now()
        self._config['DEFAULT']['lastUpdate'] = last_update.strftime('%Y-%m-%d %H:%M:%S')
        self._update_config()
