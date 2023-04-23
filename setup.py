from setuptools import setup

from openshield.__init__ import __version__

setup(
    author='Jaedson Silva',
    author_email='jaedson.dev@proton.me',
    name='openshield',
    description='OpenShield, a fast and easy-to-use CLI antivirus.',
    version=__version__,
    packages=['openshield'],
    url='https://github.com/jaedsonpys/openshield',
    license='MIT',
    python_requires='>=3.7',
    install_requires=['argeasy==3.0.0', 'requests==2.28.2'],
    entry_points={
        'console_scripts': [
            'openshield = openshield.__main__:main'
        ]
    },
    keywords=['antivirus', 'malware', 'scanner', 'cli'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Security'
    ],
)
