class Match:
    # MATHCES BETWEEN TWO TOURNAMENT IDS

    def __init__(self, player_one_id, player_two_id, completed=False, winner=None):
        self.player_one_id = player_one_id
        self.player_two_id = player_two_id
        self.completed = completed
        self.winner = winner

    @property
    def players(self):
        return [self.player_one_id, self.player_two_id]

    def set_result(self, winner=None):
        #SETS THE MATCH RESULT. WINNER CAN BE player_one_id, player_two_id, or none to tie

        self.winner = winner
        self.completed = True

    def serialize(self):
        return {
            "players": self.players,
            "completed": self.completed,
            "winner": self.winner,
        }

    @classmethod
    def from_dict(cls, data):
        players = data.get("players", [])

        return cls(
            player_one_id=players[0],
            player_two_id=players[1],
            completed=data.get("completed", False),
            winner=data.get("winner"),
        )
