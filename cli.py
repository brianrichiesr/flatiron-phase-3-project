from wordle import start_wordle

def main():
    print("Before true")
    while True:

        print("1. Play Wordle")
        print("17. Exit program")
        choice = input("> ")
        if choice == "1":
            start_wordle()
        elif choice == "17":
            exit()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()