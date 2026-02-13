from controllers import TournamentController
from views import TournamentView


def pick_tournament(controller, view, include_completed=None):
    entries = controller.list_tournaments(include_completed=include_completed)
    return view.choose_tournament(entries)


def main():
    controller = TournamentController()
    view = TournamentView()

    choice = view.show_menu()

    if choice == "1":
        player_name = view.ask_player_name()
        player = controller.get_player_by_name(player_name)
        view.show_player(player)
        return

    if choice == "2":
        tournament = pick_tournament(controller, view, include_completed=None)
        if not tournament:
            view.show_message("No tournament found.")
            return
        info = controller.get_basic_info(tournament)
        view.show_tournament_basic_info(info)
        return

    if choice == "3":
        tournament = pick_tournament(controller, view, include_completed=True)
        if not tournament:
            view.show_message("No completed tournament found.")
            return
        ranking = controller.get_points(tournament)
        view.show_points(tournament.name, ranking)
        return

    if choice == "4":
        tournament = pick_tournament(controller, view, include_completed=None)
        if not tournament:
            view.show_message("No tournament found.")
            return
        filepath = controller.export_report(tournament)
        view.show_report_written(filepath)
        return

    if choice == "5":
        tournament = pick_tournament(controller, view, include_completed=False)
        if not tournament:
            view.show_message("No in-progress tournament found.")
            return
        new_round = controller.start_or_advance_round(tournament)
        if new_round is None and not tournament._completed:
            view.show_message("Current round is not fully completed yet.")
            return
        if tournament._completed:
            view.show_message("Tournament is now completed.")
            return
        view.show_message("Round advanced and saved.")
        return

    if choice == "6":
        tournament = pick_tournament(controller, view, include_completed=False)
        if not tournament:
            view.show_message("No in-progress tournament found.")
            return

        round_number = view.ask_round_number()
        match_number = view.ask_match_number()
        winner = view.ask_winner()

        if round_number is None or match_number is None:
            view.show_message("Invalid round or match number.")
            return

        updated_match = controller.set_match_result(
            tournament=tournament,
            round_number=round_number,
            match_number=match_number,
            winner=winner,
        )

        if updated_match is None:
            view.show_message("Could not set result.")
            return
        view.show_message("Match result saved.")
        return

    view.show_message("Invalid choice.")


if __name__ == "__main__":
    main()
