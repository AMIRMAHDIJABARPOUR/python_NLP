def add_user():
    username = input(Fore.YELLOW + "Enter username: " )
    if not username:
        print(Fore.RED + "Username cannot be empty.Press Enter to continue...")
        input()
        add_user()
    elif len(username<3):
        print(Fore.RED + "Username must be at least 3 characters long. Press Enter to continue...")
        input()
        add_user()
    elif utils.search_user(username):
        print(Fore.RED+"This username is already Taken . press Enter to try agein...")
        input()
        add_user()
    password = input(Fore.YELLOW + "enter your password: ")
    if len(password)<6:
        print(Fore.RED +"password must be at least 6 characters long. press Enter to press continue...")
        input ()
        add_user()
    else: