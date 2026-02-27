from controllers import TournamentController
from views import TournamentView

def pick_tournament(controller, view, include_completed=None):
    entries = controller.list_tournaments(include_completed=include_completed)
    return view.choose_tournament(entries)

def main():
    controller = TournamentController()
    view = TournamentView()

    while True:
        choice = view.show_menu().lower()

        if choice in {"x", "exit"}:
            view.show_message("Bye!")
            return

        if choice == "1":
            while True:
                player_name = view.ask_player_name()
                player = controller.get_player_by_name(player_name)
                view.show_player(player)
                if view.ask_main_menu_or_exit() == "exit":
                    view.show_message("Bye!")
                    return
                break
            continue

        if choice == "2":
            while True:
                tournament = pick_tournament(controller, view, include_completed=None)
                if not tournament:
                    view.show_message("No tournament found.")
                else:
                    info = controller.get_basic_info(tournament)
                    view.show_tournament_basic_info(info)
                if view.ask_main_menu_or_exit() == "exit":
                    view.show_message("Bye!")
                    return
                break
            continue

        if choice == "3":
            while True:
                tournament = pick_tournament(controller, view, include_completed=True)
                if not tournament:
                    view.show_message("No completed tournament found.")
                else:
                    ranking = controller.get_points(tournament)
                    view.show_points(tournament.name, ranking)
                if view.ask_main_menu_or_exit() == "exit":
                    view.show_message("Bye!")
                    return
                break
            continue

        if choice == "4":
            while True:
                tournament = pick_tournament(controller, view, include_completed=None)
                if not tournament:
                    view.show_message("No tournament found.")
                else:
                    filepath = controller.export_report(tournament)
                    view.show_report_written(filepath)
                if view.ask_main_menu_or_exit() == "exit":
                    view.show_message("Bye!")
                    return
                break
            continue

        if choice == "5":
            while True:
                tournament = pick_tournament(controller, view, include_completed=False)
                if not tournament:
                    view.show_message("No in-progress tournament found.")
                else:
                    new_round = controller.start_or_advance_round(tournament)
                    if new_round is None and not tournament._completed:
                        view.show_message("Current round is not fully completed yet.")
                    elif tournament._completed:
                        view.show_message("Tournament is now completed.")
                    else:
                        view.show_message("Round advanced and saved.")
                if view.ask_main_menu_or_exit() == "exit":
                    view.show_message("Bye!")
                    return
                break
            continue

        if choice == "6":
            tournament = pick_tournament(controller, view, include_completed=False)
            if not tournament:
                view.show_message("No in-progress tournament found.")
                if view.ask_main_menu_or_exit() == "exit":
                    view.show_message("Bye!")
                    return
                continue

            while True:
                round_number = view.ask_round_number()
                match_number = view.ask_match_number()
                winner = view.ask_winner()

                if round_number is None or match_number is None:
                    view.show_message("Invalid round or match number.")
                else:
                    updated_match = controller.set_match_result(
                        tournament=tournament,
                        round_number=round_number,
                        match_number=match_number,
                        winner=winner,
                    )

                    if updated_match is None:
                        view.show_message("Could not set result.")
                    else:
                        view.show_message("Match result saved.")

                next_action = view.ask_match_result_next_action()
                if next_action == "record":
                    continue
                if next_action == "exit":
                    view.show_message("Bye!")
                    return
                break
            continue

        if choice == "7":
            while True:
                name = view.ask_tournament_name()
                venue = view.ask_tournament_venue()
                start_date_text = view.ask_tournament_start_date()
                end_date_text = view.ask_tournament_end_date()
                number_of_rounds = view.ask_number_of_rounds()
                player_names = view.ask_tournament_player_names()

                result = controller.create_tournament(
                    name=name,
                    venue=venue,
                    start_date_text=start_date_text,
                    end_date_text=end_date_text,
                    number_of_rounds=number_of_rounds,
                    player_names=player_names,
                )
                if not result["ok"]:
                    view.show_message(result["message"])
                else:
                    view.show_message(f"Tournament created: {result['filepath']}")

                if view.ask_main_menu_or_exit() == "exit":
                    view.show_message("Bye!")
                    return
                break
            continue

        view.show_message("Invalid choice.")


if __name__ == "__main__":
    main()
