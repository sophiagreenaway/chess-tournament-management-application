# Starter code - OpenClassrooms WPS | P3

This repository contains the work that has been done so far on the chess tournament program.

### Data files

There are data files provided:
- JSON files for the chess clubs of Springfield and Cornville
- JSON files for two tournaments: one completed, and one in progress

### Models

This package contains the models already defined by the application:
* `Player` is a class that represents a chess player
* `Club` is a class that represents a chess club (including `Player`s)
* `ClubManager` is a manager class that allows to manage all clubs (and create new ones)

### Screens

This package contains classes that are used by the application to display information from the models on the screen.
Each screen returns a Command instance (= the action to be carried out).

### Commands

This package contains "commands" - instances of classes that are used to perform operations from the program.
Commands follow a *template pattern*. They **must** define the `execute` method.
When executed, a command returns a context.

### Main application

The main application is controlled by `manage_clubs.py`. Based on the current Context instance, it instantiates the screens and runs them. The command returned by the screen is then executed to obtain the next context.

The main application is an infinite loop and stops when a context has the attribute `run` set to False.

# Setup

## Create and activate a virtual environment

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install tooling with pip

```bash
python -m pip install --upgrade pip
python -m pip install flake8
```

If you add third-party dependencies later, install them with `pip` in this same environment.

## Run the program

Main existing application:

```bash
python manage_clubs.py
```

Tournament flow script:

```bash
python manage_tournaments.py
```

## Generate a new flake8 report

Run:

```bash
flake8 . --exclude=.venv,__pycache__ --output-file=flake8_report.txt
```

This updates `/Users/sophiagreenaway/repos/P3-Application-Developer-Skills-Bootcamp/flake8_report.txt` with a new report.
