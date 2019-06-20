
[![travis](https://api.travis-ci.org/ZettaIO/cachet-client.svg?branch=master)](https://travis-ci.org/ZettaIO/cachet-client)

*WORK IN PROGRESS*

# cachet-client

A python 3 API client for then open source status page system
[Cachet](https://github.com/CachetHQ/Cachet).

* [cachet-client on github](https://github.com/ZettaIO/cachet-client)
* cachet-client on PyPI
* Documentation

## Setup

```
pip install cachet-client
```

In development:

```
git clone ...
make and activate a virtualenv
python setup.py develop
```

Cachet can easily be set up locally with docker: https://github.com/CachetHQ/Docker

## Local Development

Local setup:

```bash
python3.7 -m virtualenv .venv
. .venv/bin/activate
pip install -e .
```


Running tests:

```bash
pip install -r tests/requirements.txt
tox

# Optionally
tox -e py36  # tests only
tox -e pep8  # for pep8 run only

# Running tests wity pytest also works, but this works poorly in combination with enviroment variables for the live test script (tox separates enviroments)
pytest tests/
```
