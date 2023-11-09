from clear_screen import clear
from database.orm import Database
from rich.console import Console
from rich.table import Table
from rich.text import Text

def show_stats(user):
    
    #Main loop
    name = user.username
    showing = True
    while showing:
        #clear screen
        clear()
        showing_user = True
        #Second loop
        while showing_user:
            clear()
            #Main options
            print("Enter q to exit")
            print("1. Show games played")
            print("2. Show best game played")
            print("3. Show leaderboard")
            selection = input("> ")
            if selection == "q":
                #Quit
                showing = False
                showing_user = False
            elif selection == "1":
                #Get player stats
                stats_games_played = Database.get_player_games(name)
                if stats_games_played:
                    clear()
                    #Ask player if they want to see stats and display games played
                    print(
                f"You have played {len(stats_games_played)} game{'s' if len(stats_games_played) > 1 or len(stats_games_played) == 0 else ''}, would you like to see the stats?"
                    )
                    print("Press enter to go back, or y to see stats")
                    response = input(">")
                    if response.lower() == "y":
                        clear()
                        #Create table using rich + sql data to populate table
                        table = Table(title="Player Stats")
                        # columns = ["Game Name","Time Played","Win/Loss","Score"]
                        table.add_column("Game Name")
                        table.add_column("Time Played")
                        table.add_column("Win/Loss")
                        table.add_column("Score", style="yellow")

                        # print("| Game Name | Time Played | Win/Loss | Score |")
                        win = "\033[32mWin\033[0m"
                        loss = "\033[31mLoss\033[0m"
                        for game in stats_games_played:
                            #loop through games played for stats
                            win_loss = "Win" if game[3] == 1 else "N/A" if game[3] == 3 else "Loss"
                            colored_win_loss = Text(win_loss)
                            if game[3] == 1:
                                colored_win_loss.stylize("green")
                            elif game[3] == 0:
                                colored_win_loss.stylize("red")
                            table.add_row(game[1], str(game[2]), colored_win_loss, str(game[4]))
                        console = Console()
                        console.print(table)
                        # print("\nPress enter to continue")
                        input(">")
                else:
                    clear()
                    print("You have not played any games, press enter to continue")
                    input(">")
            elif selection == "2":
                #Checks if player has any games played
                stats_games_played = Database.get_player_games(name)
                if stats_games_played:
                    #If player has games played, create table and show best game played
                    clear()
                    best_game = Database.best_game(name)
                    if best_game:
                        table = Table(title="Best Game")
                        table.add_column("Game Name")
                        table.add_column("Time Played")
                        table.add_column("Win/Loss")
                        table.add_column("Score", style="yellow")

                        win_loss = "Win" if best_game[2] == 1 else "N/A" if best_game[2] == 3 else "Loss"
                        colored_win_loss = Text(win_loss)
                        if best_game[2] == 1:
                            colored_win_loss.stylize("green")
                        elif best_game[2] == 2:
                            colored_win_loss.stylize("red")
                        table.add_row(best_game[0], str(best_game[1]) + " seconds", colored_win_loss, str(best_game[3]))
                        console = Console()
                        console.print(table)
                        print("Press enter to continue")
                        input("> ")
                else:
                    #if no games played, dont display anything
                    clear()
                    print("You haven't played any games, press enter to continue")
                    input("> ")
            elif selection == "3":
                #Checks if player has any games played
                top_players = Database.get_top_players()
                # if best_game:
                table = Table(title="Leaderboard")
                table.add_column("Player")
                table.add_column("Total Score", style="yellow")
                table.add_column("Best Game Title")
                table.add_column("Best Game Score")

                # win_loss = "Win" if best_game[2] == 1 else "Loss"
                # colored_win_loss = Text(win_loss)
                # if best_game[2] == 1:
                #     colored_win_loss.stylize("green")
                # else:
                    # colored_win_loss.stylize("red")
                for player in top_players:
                    best_game = Database.best_game(player[0])
                    table.add_row(player[0], str(round(player[1], 2)), best_game[0], str(round(best_game[3], 2)))
                # , str(best_game[1]) + " seconds", colored_win_loss, str(best_game[3])

                console = Console()
                console.print(table)
                print("Press enter to continue")
                input("> ")
