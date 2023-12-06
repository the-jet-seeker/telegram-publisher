# The Jet Seeker [publisher]

[![tests](https://github.com/the-jet-seeker/telegram-publisher/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/the-jet-seeker/telegram-publisher/actions/workflows/tests.yml)
[![linters](https://github.com/the-jet-seeker/telegram-publisher/actions/workflows/linters.yml/badge.svg?branch=main)](https://github.com/the-jet-seeker/telegram-publisher/actions/workflows/linters.yml)


### Pre-requirements
- [Python 3.12+](https://www.python.org/downloads/)
- [PostgreSQL server](https://www.postgresql.org/download/)


### Local setup
```shell
$ git clone git@github.com:the-jet-seeker/telegram-publisher.git
$ cd telegram-publisher
$ python3.12 -m venv venv
$ source venv/bin/activate
$ pip install -U poetry pip setuptools
$ poetry config virtualenvs.create false --local
$ poetry install
```


### Host setup
```shell
$ add-apt-repository ppa:deadsnakes/ppa
$ apt-get update
$ apt install -y software-properties-common python3.12 python3.12-dev python3.12-venv python3-psycopg2 libpq-dev gcc postgresql-client-14
$ apt-get upgrade

$ curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
$ curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

$ python3.10 -m pip install --upgrade setuptools
$ python3.12 -m pip install --upgrade setuptools

$ adduser tjs-stage-publisher
$ adduser tjs-production-publisher
```


### Local run tests
```shell
$ pytest --cov=telegram_publisher
```


### Local run linters
```shell
$ poetry run flake8 telegram_publisher/
$ poetry run mypy telegram_publisher/
```

### Run scrapper
```shell
$ python -m telegram_publisher.publisher
```


### Setting up periodically jobs
```shell
$ crontab etc/crontab.txt
```