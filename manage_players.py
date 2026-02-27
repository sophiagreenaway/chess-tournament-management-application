from models import PlayerManager

def ask_non_empty(prompt):
    while True:
        value = input(f"{prompt}? ").strip()
        if value:
            return value
        print("Please provide a value.")


def ask_email(manager):
    while True:
        value = input("Email address? ")
        normalized = manager.normalize_email(value)
        if normalized:
            return normalized
        print("Please provide a valid email address.")


def ask_chess_id(manager, club):
    while True:
        value = input("Chess ID (XXNNNNN)? ")
        normalized = manager.normalize_chess_id(value)
        if not normalized:
            print("Please provide a valid Chess ID (XXNNNNN).")
            continue

        if manager.is_chess_id_taken(club, normalized):
            print("A player with this Chess ID already exists in this club.")
            continue

        return normalized


def ask_birthday(manager):
    while True:
        value = input("Birthday (dd-mm-yyyy)? ")
        normalized = manager.normalize_birthday(value)
        if not normalized:
            print("Please provide a valid date (dd-mm-yyyy).")
            continue

        return normalized


def choose_club(manager):
    clubs = manager.list_clubs()
    if not clubs:
        print("No clubs found. Create a club first in manage_clubs.py.")
        return None

    print("Select a club:")
    for idx, club in enumerate(clubs, 1):
        print(f"{idx}. {club.name}")

    while True:
        value = input("Club number (or X to exit)? ").strip()
        if value.upper() == "X":
            return None
        if value.isdigit():
            number = int(value)
            club = manager.get_club_by_number(number)
            if club:
                return club
        print("Invalid selection.")


def create_player_flow():
    manager = PlayerManager()
    club = choose_club(manager)
    if club is None:
        return

    while True:
        print("")
        print(f"Create player in: {club.name}")
        name = ask_non_empty("Player name")
        email = ask_email(manager)
        chess_id = ask_chess_id(manager, club)
        birthday = ask_birthday(manager)

        player = manager.create_player(club, name, email, chess_id, birthday)
        print(f"Player created: {player.name} ({player.chess_id})")

        again = input("Create another player in this club? (y/N) ").strip().lower()
        if again != "y":
            break


if __name__ == "__main__":
    create_player_flow()
