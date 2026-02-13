from .match import Match


class Round:
    # A TOURNAMENT ROUND CONSISTS OF SEVERAL MATCHES

    def __init__(self, matches=None):
        self.matches = []
        if matches:
            for match in matches:
                if isinstance(match, Match):
                    self.matches.append(match)
                else:
                    self.matches.append(Match.from_dict(match))

    def add_match(self, match):
        self.matches.append(match)

    def is_completed(self):
        if not self.matches:
            return False
        return all(match.completed for match in self.matches)

    def serialize(self):
        return [match.serialize() for match in self.matches]

    @classmethod
    def from_list(cls, data):
        return cls(matches=[Match.from_dict(item) for item in data])
