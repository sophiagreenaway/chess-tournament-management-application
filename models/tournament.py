from datetime import date
import random

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
        _player_ids: list[str]| None = None,
        _completed: bool = False,

    ):
        if end_date < start_date:
            raise ValueError("end_date must be >= start_date")
        if number_of_rounds <= 0:
            raise ValueError("number_of_rounds must be > 0")

        self.name = name
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        
        self._rounds = _rounds or []
        self._current_round_index = _current_round_index
        self._player_ids = _player_ids or []
        self._completed = _completed

    def register_player(self, player):
        #if player.chess_id in self._player_ids:
        self._player_ids.append(player.chess_id)
        return player.chess_id
    
    def get_current_round(self):
        if self._current_round_index == 0:
            return None
        return self._rounds[self._current_round_index - 1]

    def generate_first_round(self):
        players = self._player_ids[:]   # copy list
        random.shuffle(players)

        new_round = []
        i = 0
        while i < len(players):
            match = {
                "players": [players[i], players[i + 1]],
                "completed": False,
                "winner": None
            }
            new_round.append(match)
            i += 2

        self._rounds.append(new_round)
        self._current_round_index = 1
        return new_round

    def generate_next_round(self):
        table = self.standings()
        players = []
        for row in table:
            players.append(row["player_id"])

        new_round = []
        i = 0
        while i < len(players):
            match = {
                "players": [players[i], players[i + 1]],
                "completed": False,
                "winner": None
            }
            new_round.append(match)
            i += 2

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
        for match in current_round:
            if not match["completed"]:
                all_done = False

        if not all_done:
            return None

        if len(self._rounds) >= self.number_of_rounds:
            self._completed = True
            return None

        return self.generate_next_round()

    def standings(self):
        points = {}
        for pid in self._player_ids:
            points[pid] = 0

        for rnd in self._rounds:
            for match in rnd:
                if not match["completed"]:
                    continue

                p1 = match["players"][0]
                p2 = match["players"][1]
                winner = match["winner"]

                if winner == p1:
                    points[p1] += 1
                elif winner == p2:
                    points[p2] += 1
                else:
                    points[p1] += 0.5
                    points[p2] += 0.5

        ranking = []

        for pid, score in points.items():
            ranking.append({"player_id": pid, "points": score})

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
        for match in last_round:
            if not match["completed"]:
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
            winner = final_table[0]["player_id"]

        return {
            "completed": True,
            "message": "Tournament finished.",
            "winner": winner,
            "standings": final_table,
        }
    
    def serialize(self):
        return {
            "name": self.name,
            "dates": {
                "from": self.start_date.strftime(self.DATE_FORMAT),
                "to": self.end_date.strftime(self.DATE_FORMAT),
            },
            "venue": self.venue,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self._current_round_index,
            "completed": self._completed,
            "players": self._player_ids,
            "rounds": self._rounds,
        }