# OpenClassrooms WPS | P3

This repository contains the current implementation of the chess tournament program.

### Data files

There are data files provided:
- JSON files for the chess clubs of Springfield and Cornville
- JSON files for tournaments in progress and completed states
- A generated reports folder for tournament export files

### Models

This package contains the domain models used by the application:
* `player.py` is a class that represents a chess player
* `club.py` is a class that represents a chess club
* `club_manager.py` is a manager class that allows management all clubs (and create new ones)
* `match.py` is a class that represents a match between two players
* `round.py` is a class that represents one tournament round and its matches
* `tournament.py` is a class that handles tournament rounds, results, standings, and serialization
* `tournament_manager.py` is a manager class that loads and saves tournament files
* `player_manager.py` is a manager class that allows the creation of players

### Screens

This package contains classes that are used by the application to display information from the models on the screen.
Each screen returns a Command instance (= the action to be carried out).

### Commands

This package contains "commands" - instances of classes that are used to perform operations from the program.
Commands follow a *template pattern*. They **must** define the `execute` method.
When executed, a command returns a context.

### Main application

The club management application is controlled by `manage_clubs.py`. Based on the current Context instance, it instantiates the screens and runs them. The command returned by the screen is then executed to obtain the next context.

The main application is an infinite loop and stops when a context has the attribute `run` set to False.

Tournament operations are available in `manage_tournaments.py`, using:
- `controllers/tournament_controller.py` for orchestration
- `views/tournament_view.py` for terminal interaction

The tournament flow includes:
- Loading players and displaying player information by name
- Loading tournaments and displaying basic tournament attributes
- Loading completed tournaments and calculating points per player
- Exporting tournament reports to `data/reports`
- Starting/advancing rounds and recording match results

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
flake8 . --format=html --htmldir=flake8-report
```

This updates `/Users/sophiagreenaway/repos/P3-Application-Developer-Skills-Bootcamp/flake8_report.txt` with a new report.
