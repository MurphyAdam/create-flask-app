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

## Endpoints provided

`/` renders html template

`/api` returns json data
