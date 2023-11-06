from clear_screen import clear
from database.orm import Database
import time


def show_stats():
    showing = True
    while showing:
        clear()
        print("Please enter your username, or enter q to exit")
        inp = input("> ")
        if Database.get_player(inp):
            showing_user = True
            while showing_user:
                name = inp
                clear()
                print("Enter q to exit")
                print("1. Show games played")
                print("2. Show best game played")
                selection = input("> ")
                if selection == "q":
                    showing = False
                    showing_user = False
                elif selection == "1":
                    stats_games_played = Database.get_player_games(name)
                    if stats_games_played:
                        clear()
                        print(
                    f"You have played {len(stats_games_played)} game{'s' if len(stats_games_played) > 1 or len(stats_games_played) == 0 else ''}, would you like to see the stats?"
                        )
                        print("Press enter to go back, or y to see stats")
                        f = input(">")
                        if f.lower() == "y":
                            clear()
                            print("| Game Name | Time Played | Win/Loss | Score |")
                            for game in stats_games_played:
                                print(
                                    f'| {game[1]} | {game[2]} seconds | {"Win" if game[3] == 1 else "Loss"} | {game[4]} points|'
                                )
                            print("\nPress enter to continue")
                            input(">")
                    else:
                        clear()
                        print("You have not played any games, press enter to continue")
                        input(">")
                elif selection == "2":
                    stats_games_played = Database.get_player_games(name)
                    if stats_games_played:
                        clear()
                        best_game = Database.best_game(name)
                        print("Here is your best game")
                        print(f'| {best_game[0]} | {best_game[1]} seconds | {"Win" if best_game[2] == 1 else "Loss"} | {best_game[3]} points|')
                        print("\nPress enter to go continue")
                        input(">")
        else:
            if inp == "q":
                showing = False
            else:
                clear()
                print("No user with that name exists")
                time.sleep(2)
