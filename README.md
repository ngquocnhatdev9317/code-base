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

$ docker build . -t code-base-app  # code-base-app is name of image
$ docker run code-base-app

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
|   |   |-- tests/
|   |   |-- controller.py
|   |   |-- model.py
|   |   |-- repository.py
|   |   |-- router.py
|   |-- utilities/                          # Contain some utilities, common using in project
|   |   |-- middlewares/
|   |   |-- schemas/
|   |   |-- configs.py
|   |   |-- logger.py
|   |-- main.py                             # The main of project
|   |-- router.py
|-- README.md
|-- requirements.txt                        # Save library info
|-- Dockerfile
```

# Thank you!
