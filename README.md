# Introduction

This is the code base for aio-http framework

# Getting start

## Requirements

```bash
    Docker
    Python >= 3.10
```

# Build local

## Build docker

```bash

$ cp .env.example .env
$ docker-compose up --build

```

## Swagger

Open swagger at [http://localhost:8080/docs](http://localhost:8080/docs)

## Run unittest local

```bash

$ python -m pytest src/

# Run unittest with coverage report
$ python -m pytest --cov src/

```

## Run format code after change files

```bash
# format sort for import
$ poetry run ruff format src/


```

# Project Structure

```bash
code-base/
|-- app/
|   |-- database/                           # Define database
|   |   |-- base_model.py
|   |   |-- base_repository.py
|   |   |-- base_schema.py
|   |   |-- connection.py
|   |-- user/                               # Contain everything of user feature
|   |   |-- schemas/
|   |   |-- controller.py
|   |   |-- model.py
|   |   |-- repository.py
|   |   |-- router.py
|   |-- utilities/                          # Contain some utilities, common using in project
|   |   |-- middlewares/
|   |   |-- schemas/
|   |   |-- configs.py
|   |   |-- logger.py
|   |-- tests/                              # Contain all testcase unittest in project
|   |-- conftest.py                         # Define and config Base test for unittest
|   |-- main.py                             # The main of project
|   |-- router.py
|-- README.md
|-- requirements.txt                        # Save library info
|-- Dockerfile
```

# Thank you!
