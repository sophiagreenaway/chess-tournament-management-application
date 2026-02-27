import re
from datetime import datetime

from .club_manager import ClubManager


class PlayerManager:
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    CHESS_ID_REGEX = re.compile(r"^[A-Z]{2}[0-9]{5}$")
    DATE_FORMAT = "%d-%m-%Y"

    def __init__(self, club_manager=None):
        self.club_manager = club_manager or ClubManager()

    def list_clubs(self):
        return self.club_manager.clubs[:]

    def get_club_by_number(self, number):
        if number < 1 or number > len(self.club_manager.clubs):
            return None
        return self.club_manager.clubs[number - 1]

    def normalize_email(self, value):
        normalized = value.strip().lower()
        if self.EMAIL_REGEX.match(normalized):
            return normalized
        return None

    def normalize_chess_id(self, value):
        normalized = value.strip().upper()
        if self.CHESS_ID_REGEX.match(normalized):
            return normalized
        return None

    def is_chess_id_taken(self, club, chess_id):
        return any(player.chess_id == chess_id for player in club.players)

    def normalize_birthday(self, value):
        normalized = value.strip()
        try:
            parsed = datetime.strptime(normalized, self.DATE_FORMAT)
        except ValueError:
            return None

        if parsed > datetime.now():
            return None
        return normalized

    def create_player(self, club, name, email, chess_id, birthday):
        return club.create_player(
            name=name,
            email=email,
            chess_id=chess_id,
            birthday=birthday,
        )
