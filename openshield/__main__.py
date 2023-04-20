import os
import time

from argeasy import ArgEasy

from .__init__ import __version__
from .scanner import Scanner

# TODO: Criar generator para obter arquivos
def _get_files(path_list: str) -> list:
    file_list = []

    for path in path_list:
        if os.path.isdir(path):
            for root, __, files in os.walk(path):
                for file in files:
                    file_list.append(os.path.join(root, file))
        else:
            file_list.append(path)

    return file_list


def main():
    parser = ArgEasy(
        name='OpenShield',
        description='Open-source CLI Antivirus',
        version=__version__
    )

    parser.add_argument('scan', 'Scan a directories and files', action='append')
    args = parser.parse()

    if args.scan is not None:
        scanner = Scanner()
        print('\033[32m[!]\033[m Checking for database updates...', end=' ')

        if scanner.require_hashes_update():
            print('\033[32mDownloading...\033[m')
            scanner.update_database()
        else:
            print('\033[33mAll up-to-date.\033[m')

        start_scan_time = time.time()
        print(f'\033[32m[?]\033[m Discovering files...', flush=True, end=' ')
        files = _get_files(args.scan)
        print('\033[33mOK\033[m')
        print(f'\033[32m[?]\033[m Scanning {len(files)} files...', flush=True, end=' ')
        malwares = scanner.scan(files)
        scan_time = time.time() - start_scan_time

        print('\033[33mOK\033[m')

        if malwares:
            print(f'\033[31m[!] {len(malwares)} malwares found! (scan in {scan_time:.3f})\033[33m')
            for malware in malwares:
                print(f'    File {repr(malware[0])} ({malware[1]})')

            print('\033[31m[WARNING] Do not open the files mentioned above. '
                  'Delete all of them as soon as possible.\033[m')
        else:
            print(f'\033[32m[!]\033[m All right, {len(malwares)} malwares found! (scan in {scan_time:.3f})')
