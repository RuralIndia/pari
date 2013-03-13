# Pari

People's Archive Of Rural India

[![Build Status](https://travis-ci.org/RuralIndia/pari.png)](https://travis-ci.org//RuralIndia/pari)


## Dev Setup

Clone the repo.

### Python and packages management

Use [pythonbrew](https://github.com/utahta/pythonbrew) for python runtime and packages management

```bash
pythonbrew install 2.7.3
pythonbrew use 2.7.3
pythonbrew venv create pari
pythonbrew venv use pari
```

### Install the dependencies

```bash
pip install -r requirements/dev.txt
```
**Note:**Use [autoenv](https://github.com/kennethreitz/autoenv) to simplify the above process. Just install `pythonbrew` and `cd` into the project to get started. The checked-in `.env` file will install python-2.7.3 and install dependencies in virtual environment `pari`. It also sets the `DJANGO_SETTINGS_MODULE` environment variable to `pari.settings.dev` for local development.

### Setup the database

```bash
python manage.py syncdb 
python manage.py migrate
python manage.py loaddata pari/fixtures/initial_data_1.json 
```

**Note:** Add these to your .bash_profile if you are getting "unknown locale: UTF-8" error

```bash
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```