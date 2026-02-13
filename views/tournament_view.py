class TournamentView:
    def show_menu(self):
        print("Select one:")
        print("1 Load players, ask for name, display player")
        print("2 Load tournament and display attributes")
        print("3 Load completed tournament and calculate points")
        print("4 Export tournament report to file")
        print("5 Start or continue a round")
        print("6 Record a match result")
        return input("Choice? ").strip()

    def ask_player_name(self):
        while True:
            value = input("Player name? ").strip()
            if value:
                return value
            print("Please provide a name.")

    def show_player(self, player):
        if not player:
            print("Player not found.")
            return
        print("Name:", player.name)
        print("Email:", player.email)
        print("Chess ID:", player.chess_id)
        print("Birthday:", player.birthday)

    def choose_tournament(self, tournament_entries):
        if not tournament_entries:
            return None

        print("Choose a tournament:")
        for idx, (filepath, tournament) in enumerate(tournament_entries, 1):
            print(f"{idx}. {tournament.name} ({filepath.name})")

        while True:
            raw_value = input("Number? ").strip()
            if raw_value.isdigit():
                number = int(raw_value)
                if 1 <= number <= len(tournament_entries):
                    return tournament_entries[number - 1][1]
            print("Invalid choice.")

    def show_tournament_basic_info(self, info):
        if not info:
            print("No tournament found.")
            return
        print("Name:", info["name"])
        print("Venue:", info["venue"])
        print("From:", info["from"])
        print("To:", info["to"])
        print("Number of rounds:", info["number_of_rounds"])
        print("Current round:", info["current_round"])
        print("Completed:", info["completed"])

    def show_points(self, tournament_name, ranking):
        if not ranking:
            print("No completed tournament found.")
            return
        print("Tournament:", tournament_name)
        print("Points by player:")
        for row in ranking:
            print(f"- {row['player_name']}: {row['points']}")

    def show_report_written(self, filepath):
        print("Report written to:", filepath)

    def ask_round_number(self):
        raw_value = input("Round number? ").strip()
        if raw_value.isdigit():
            return int(raw_value)
        return None

    def ask_match_number(self):
        raw_value = input("Match number? ").strip()
        if raw_value.isdigit():
            return int(raw_value)
        return None

    def ask_winner(self):
        value = input("Winner Chess ID (leave empty for draw)? ").strip().upper()
        if value == "":
            return None
        return value

    def show_message(self, message):
        print(message)
