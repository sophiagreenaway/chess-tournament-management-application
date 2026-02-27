import json
from datetime import date, datetime
import random
from .player import Player
from .round import Round
from .match import Match

class Tournament:
    
    DATE_FORMAT = "%d-%m-%Y"

    def __init__(
        self, 
        name: str,
        venue: str,
        start_date: date,
        end_date: date,
        number_of_rounds: int,

        # Class attributes below are private
        _rounds: list["Round"]| None = None,
        _current_round_index: int = 0,
        _player_names: list[str]| None = None,
        _completed: bool = False,
        filepath=None,

    ):
        if end_date < start_date:
            raise ValueError("end_date must be >= start_date")
        if number_of_rounds <= 0:
            raise ValueError("number_of_rounds must be > 0")

        self.name = name
        self.filepath = filepath
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        
        self._rounds = []
        if _rounds:
            for round_data in _rounds:
                # Default function isinstance to check if object is 
                # of a given class/subclass. in this case round_data for
                # class Round
                if isinstance(round_data, Round):
                    self._rounds.append(round_data)
                else:
                    self._rounds.append(Round.from_list(round_data))
        self._current_round_index = _current_round_index
        self._player_names = _player_names or []
        self._completed = _completed

    def register_player(self, player):
        if self._completed:
            return None
        if not isinstance(player, Player):
            return None
        if player.name not in self._player_names:
            self._player_names.append(player.name)
        return player.name
    
    def get_current_round(self):
        if self._current_round_index == 0:
            return None
        return self._rounds[self._current_round_index - 1]

    def generate_first_round(self):
        if self._rounds:
            return self._rounds[0]
        if len(self._player_names) < 2:
            return None
        if len(self._player_names) % 2 != 0:
            return None

        players = self._player_names[:]   # copy list
        random.shuffle(players)

        new_round = Round()
        i = 0
        while i < len(players):
            match = Match(players[i], players[i + 1])
            new_round.add_match(match)
            i += 2

        self._rounds.append(new_round)
        self._current_round_index = 1
        return new_round

    def _played_pairs(self):
        played = set()
        for rnd in self._rounds:
            for match in rnd.matches:
                played.add(frozenset(match.players))
        return played

    def generate_next_round(self):
        if self._completed:
            return None
        if not self._rounds:
            return self.generate_first_round()
        if len(self._rounds) >= self.number_of_rounds:
            return None

        table = self.standings()
        players = []
        for row in table:
            players.append(row["player_name"])

        played_pairs = self._played_pairs()
        waiting = players[:]
        new_round = Round()

        while len(waiting) > 0:
            p1 = waiting.pop(0)
            candidate_indexes = []

            i = 0
            while i < len(waiting):
                p2 = waiting[i]
                pair_key = frozenset([p1, p2])
                if pair_key not in played_pairs:
                    candidate_indexes.append(i)
                i += 1

            if candidate_indexes:
                chosen_index = random.choice(candidate_indexes)
            else:
                chosen_index = 0

            p2 = waiting.pop(chosen_index)
            match = Match(p1, p2)
            new_round.add_match(match)

        self._rounds.append(new_round)
        self._current_round_index = len(self._rounds)
        return new_round

    def advance_round(self):
        if self._completed:
            return None

        if len(self._rounds) == 0:
            return self.generate_first_round()

        current_round = self.get_current_round()

        all_done = True
        for match in current_round.matches:
            if not match.completed:
                all_done = False

        if not all_done:
            return None

        if len(self._rounds) >= self.number_of_rounds:
            self._completed = True
            return None

        return self.generate_next_round()

    def set_match_result(self, round_number, match_number, winner=None):
        round_index = round_number - 1
        match_index = match_number - 1

        if round_index < 0 or round_index >= len(self._rounds):
            return None

        current_round = self._rounds[round_index]
        if match_index < 0 or match_index >= len(current_round.matches):
            return None

        match = current_round.matches[match_index]
        if winner is not None and winner not in match.players:
            return None

        match.set_result(winner)
        return match

    def standings(self):
        points = {}
        for name in self._player_names:
            points[name] = 0

        for rnd in self._rounds:
            for match in rnd.matches:
                if not match.completed:
                    continue

                p1 = match.players[0]
                p2 = match.players[1]
                winner = match.winner

                if winner == p1:
                    points[p1] += 1
                elif winner == p2:
                    points[p2] += 1
                else:
                    points[p1] += 0.5
                    points[p2] += 0.5

        ranking = []

        for name, score in points.items():
            ranking.append({"player_name": name, "points": score})

        def get_points(item):
            return item["points"]
        ranking.sort(key=get_points, reverse=True)
        return ranking

    def finish_tournament(self):
        # Already finished
        if self._completed:
            return {
                "completed": True,
                "message": "Tournament already finished.",
                "standings": self.standings(),
            }

        # Do all rounds exist
        if len(self._rounds) < self.number_of_rounds:
            return {
                "completed": False,
                "message": "Not all rounds have been generated yet.",
                "standings": self.standings(),
            }

        # Is last round completed
        last_round = self._rounds[-1]
        for match in last_round.matches:
            if not match.completed:
                return {
                    "completed": False,
                    "message": "Last round is not fully completed yet.",
                    "standings": self.standings(),
                }

        # Finish tournament
        self._completed = True
        final_table = self.standings()

        winner = None
        if len(final_table) > 0:
            winner = final_table[0]["player_name"]

        return {
            "completed": True,
            "message": "Tournament finished.",
            "winner": winner,
            "standings": final_table,
        }
    
    def serialize(self):
        current_round = self._current_round_index
        if self._completed:
            current_round = None

        return {
            "name": self.name,
            "dates": {
                "from": self.start_date.strftime(self.DATE_FORMAT),
                "to": self.end_date.strftime(self.DATE_FORMAT),
            },
            "venue": self.venue,
            "number_of_rounds": self.number_of_rounds,
            "current_round": current_round,
            "completed": self._completed,
            "players": self._player_names[:],
            "rounds": [rnd.serialize() for rnd in self._rounds],
        }

    def save(self):
        with open(self.filepath, "w") as fp:
            json.dump(self.serialize(), fp)

    @classmethod
    def from_dict(cls, data, filepath=None):
        dates = data.get("dates", {})
        start_date = datetime.strptime(dates["from"], cls.DATE_FORMAT).date()
        end_date = datetime.strptime(dates["to"], cls.DATE_FORMAT).date()

        return cls(
            name=data["name"],
            venue=data["venue"],
            start_date=start_date,
            end_date=end_date,
            number_of_rounds=data["number_of_rounds"],
            _rounds=data.get("rounds", []),
            _current_round_index=data.get("current_round") or 0,
            _player_names=data.get("players", []),
            _completed=data.get("completed", False),
            filepath=filepath,
        )
