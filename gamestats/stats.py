from clear_screen import clear
from database.orm import Database
import curses
import time


def show_stats(user):
    showing = True
    while showing:
        clear()
        showing_user = True
        while showing_user:
            name = user.username
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
                    response = input(">")
                    if response.lower() == "y":
                        clear()
                        print("| Game Name | Time Played | Win/Loss | Score |")
                        win = "\033[32mWin\033[0m"
                        loss = "\033[31mLoss\033[0m"
                        for game in stats_games_played:
                            points = '\033[33m' + str(game[4]) + '\033[0m'
                            print(
                                f'| {game[1]} | {game[2]} seconds | {win if game[3] == 1 else "N/A" if game[3] == 3 else loss} | {points} points|'
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
                    win = "\033[32mWin\033[0m"
                    loss = "\033[31mLoss\033[0m"
                    print("Here is your best game")
                    print(f'| {best_game[0]} | {best_game[1]} seconds | {win if best_game[2] == 1 else loss} | {best_game[3]} points|')
                    print("\nPress enter to continue")
                    input(">")
