from pathlib import Path
import re
from datetime import datetime

from models import ClubManager, Tournament, TournamentManager


class TournamentController:
    def __init__(self):
        self.club_manager = ClubManager()
        self.tournament_manager = TournamentManager()

    def get_player_by_chess_id(self, chess_id):
        for club in self.club_manager.clubs:
            for player in club.players:
                if player.chess_id == chess_id:
                    return player
        return None

    def get_player_by_name(self, name):
        value = name.strip().lower()
        if not value:
            return None
        for club in self.club_manager.clubs:
            for player in club.players:
                if player.name.strip().lower() == value:
                    return player
        return None

    def _player_name(self, chess_id):
        player = self.get_player_by_chess_id(chess_id)
        if player is None:
            return chess_id
        return player.name

    def _resolve_winner_for_match(self, tournament, round_number, match_number, winner):
        if winner is None:
            return None

        round_index = round_number - 1
        match_index = match_number - 1
        if round_index < 0 or round_index >= len(tournament._rounds):
            return winner

        current_round = tournament._rounds[round_index]
        if match_index < 0 or match_index >= len(current_round.matches):
            return winner

        match = current_round.matches[match_index]
        match_players = match.players

        normalized_winner = winner.strip().lower()
        for player_value in match_players:
            if player_value.strip().lower() == normalized_winner:
                return player_value

        player = self.get_player_by_name(winner)
        if player is None:
            return winner

        for player_value in match_players:
            value = player_value.strip()
            if value == player.chess_id or value.lower() == player.name.strip().lower():
                return player_value

        return winner

    def list_tournaments(self, include_completed=None):
        return self.tournament_manager.list_tournaments(include_completed=include_completed)

    def _sanitize_filename(self, text):
        normalized = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        if not normalized:
            normalized = "tournament"
        return normalized

    def _next_tournament_filepath(self, tournament_name):
        tournaments_dir = self.tournament_manager.data_folder
        tournaments_dir.mkdir(parents=True, exist_ok=True)
        base = self._sanitize_filename(tournament_name)
        filepath = tournaments_dir / f"{base}.json"
        i = 2
        while filepath.exists():
            filepath = tournaments_dir / f"{base}-{i}.json"
            i += 1
        return filepath

    def create_tournament(self, name, venue, start_date_text, end_date_text, number_of_rounds, player_names):
        if not player_names:
            return {"ok": False, "message": "Please provide at least two players."}

        unique_names = []
        seen = set()
        for raw_name in player_names:
            value = raw_name.strip()
            key = value.lower()
            if not value or key in seen:
                continue
            seen.add(key)
            unique_names.append(value)

        if len(unique_names) < 2:
            return {"ok": False, "message": "Please provide at least two unique players."}

        if len(unique_names) % 2 != 0:
            return {"ok": False, "message": "Please provide an even number of players."}

        if number_of_rounds is None or number_of_rounds <= 0:
            return {"ok": False, "message": "Number of rounds must be a positive integer."}

        try:
            start_date = datetime.strptime(start_date_text, Tournament.DATE_FORMAT).date()
            end_date = datetime.strptime(end_date_text, Tournament.DATE_FORMAT).date()
        except ValueError:
            return {"ok": False, "message": "Dates must use dd-mm-yyyy format."}

        players = []
        missing = []
        for player_name in unique_names:
            player = self.get_player_by_name(player_name)
            if player is None:
                missing.append(player_name)
            else:
                players.append(player)

        if missing:
            return {
                "ok": False,
                "message": f"Player(s) not found: {', '.join(missing)}",
            }

        filepath = self._next_tournament_filepath(name)
        tournament = Tournament(
            name=name,
            venue=venue,
            start_date=start_date,
            end_date=end_date,
            number_of_rounds=number_of_rounds,
            filepath=filepath,
        )
        for player in players:
            tournament.register_player(player)

        self.tournament_manager.save_tournament(tournament)
        return {"ok": True, "filepath": filepath, "tournament": tournament}

    def get_basic_info(self, tournament):
        data = tournament.serialize()
        return {
            "name": tournament.name,
            "venue": tournament.venue,
            "from": tournament.start_date.strftime(tournament.DATE_FORMAT),
            "to": tournament.end_date.strftime(tournament.DATE_FORMAT),
            "number_of_rounds": tournament.number_of_rounds,
            "current_round": data["current_round"],
            "completed": tournament._completed,
        }

    def get_points(self, tournament):
        ranking = tournament.standings()
        rows = []
        for row in ranking:
            player_name = row["player_name"]
            rows.append(
                {
                    "player_name": self._player_name(player_name),
                    "points": row["points"],
                }
            )
        return rows

    def export_report(self, tournament):
        safe_name = tournament.name.lower().replace(" ", "-")
        reports_dir = Path("data/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        filepath = reports_dir / f"{safe_name}-report.txt"

        lines = []
        info = self.get_basic_info(tournament)
        lines.append(f"Tournament report: {info['name']}")
        lines.append(f"Venue: {info['venue']}")
        lines.append(f"From: {info['from']}")
        lines.append(f"To: {info['to']}")
        lines.append(f"Number of rounds: {info['number_of_rounds']}")
        lines.append(f"Completed: {info['completed']}")
        lines.append("")

        lines.append("Standings:")
        ranking = self.get_points(tournament)
        for idx, row in enumerate(ranking, 1):
            lines.append(f"{idx}. {row['player_name']} - {row['points']} pts")
        lines.append("")

        lines.append("Rounds:")
        rounds_data = tournament.serialize()["rounds"]
        for round_index, round_matches in enumerate(rounds_data, 1):
            lines.append(f"Round {round_index}:")
            for match in round_matches:
                p1 = match["players"][0]
                p2 = match["players"][1]
                winner = match.get("winner")
                completed = match.get("completed", False)
                p1_name = self._player_name(p1)
                p2_name = self._player_name(p2)

                if not completed:
                    result = "not completed"
                elif winner is None:
                    result = "draw"
                else:
                    result = f"winner: {self._player_name(winner)}"

                lines.append(f"- {p1_name} vs {p2_name} ({result})")
            lines.append("")

        filepath.write_text("\n".join(lines))
        return filepath

    def start_or_advance_round(self, tournament):
        round_value = tournament.advance_round()
        if round_value is not None or tournament._completed:
            self.tournament_manager.save_tournament(tournament)
        return round_value

    def set_match_result(self, tournament, round_number, match_number, winner):
        resolved_winner = self._resolve_winner_for_match(
            tournament=tournament,
            round_number=round_number,
            match_number=match_number,
            winner=winner,
        )
        updated_match = tournament.set_match_result(round_number, match_number, resolved_winner)
        if updated_match is not None:
            self.tournament_manager.save_tournament(tournament)
        return updated_match
