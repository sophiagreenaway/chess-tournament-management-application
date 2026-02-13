from pathlib import Path

from models import ClubManager, TournamentManager


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

    def list_tournaments(self, include_completed=None):
        return self.tournament_manager.list_tournaments(include_completed=include_completed)

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
            player_id = row["player_id"]
            rows.append(
                {
                    "player_id": player_id,
                    "player_name": self._player_name(player_id),
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
        updated_match = tournament.set_match_result(round_number, match_number, winner)
        if updated_match is not None:
            self.tournament_manager.save_tournament(tournament)
        return updated_match
