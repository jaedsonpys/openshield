import os
from pathlib import Path

HOME_USER = Path.home()
CONFIG_FILEPATH = os.path.join(HOME_USER, 'openshield.ini')
HASH_DATA_PATH = os.path.join(HOME_USER, 'hashes.openshield.zip')

MD5_HASH_DOWNLOAD_URL = 'https://bazaar.abuse.ch/export/txt/md5/full/'
