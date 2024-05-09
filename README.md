# kickstart-flask-app

This is a simple package to kickstart a new Flask app project.
It creates a new Flask project with a simple structure and some endpoints.

## Install

```bash
pip install kickstart-flask-app
```

## Usage

You could use this package in two ways:

### 1. Command line (recommended)

Type the following in your terminal

```bash
kickstart-flask-app
```

The above will propmt you to enter some data, press enter to use defaults.
This will create a new Flask project in the path you run the python interpreter

### 2. The Python interpreter

```py
from kickstart_flask_app import console

console()

```

Same as the command line, this will prompt you to enter some data, press enter to use defaults.

## Start the server

First, setup the virtual environment and set environment variables. (APP_ENV or FLASK_ENV to 'dev' or 'prod')

```bash
cd <your_project_name>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=dev
```

Then start the server

```bash
python wsgi.py
```

The server should be running on `http://localhost:5000`

## Endpoints provided

`/` renders html template

`/api` returns json data
