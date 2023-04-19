from argeasy import ArgEasy

from .__init__ import __version__


def main():
    parser = ArgEasy(
        name='OpenShield',
        description='Open-source CLI Antivirus',
        version=__version__
    )
