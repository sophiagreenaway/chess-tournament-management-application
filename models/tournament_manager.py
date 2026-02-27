import json
from pathlib import Path

from .tournament import Tournament


class TournamentManager:
    # LOAD TOURNAMENTS FROM .JSON FILES

    def __init__(self, data_folder="data/tournaments"):
        datadir = Path(data_folder)
        self.data_folder = datadir
        self.tournaments = []

        for filepath in datadir.iterdir():
            if filepath.is_file() and filepath.suffix == ".json":
                with open(filepath) as fp:
                    data = json.load(fp)
                self.tournaments.append((filepath, Tournament.from_dict(data, filepath=filepath)))

    def list_tournaments(self, include_completed=None):
        if include_completed is None:
            return self.tournaments[:]

        filtered = []
        for filepath, tournament in self.tournaments:
            if tournament._completed == include_completed:
                filtered.append((filepath, tournament))
        return filtered

    def save_tournament(self, tournament):
        tournament.save()
        for index, (filepath, _) in enumerate(self.tournaments):
            if filepath == tournament.filepath:
                self.tournaments[index] = (filepath, tournament)
                return
        self.tournaments.append((tournament.filepath, tournament))
