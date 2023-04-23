# OpenShield

OpenShield is a simple and fast antivirus that allows you to scan various files to find malware on your computer. The database used to perform the malware search comes from [MalwareBazaar](https://bazaar.abuse.ch/export). The project is written in Python and open-source, it can be used via command-line interface (CLI).

## Getting started

Install the program using the PIP package manager or install it manually by cloning the repository:

```
pip install openshield
```
```
git clone https://github.com/jaedsonpys/openshield.git
cd openshield/
python3 setup.py install
```

## How to use

To scan files and/or directories, use the `openshield scan` command and pass as argument the name of the directory or file. Here is an example:

```
openshield scan ~/Downloads
```

Now scanning multiple files at once:

```
openshield scan script.py MyAplication.exe
```

You will receive a warning message if malware is found, the advice is to delete the file as soon as possible and **do not run or open** it.