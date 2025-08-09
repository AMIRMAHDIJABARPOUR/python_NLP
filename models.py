from colorama import init, Fore, Style
import utils

init(autoreset=True)


# =================add user function======================
def add_user():
    while True:
        username = input(Fore.YELLOW + "Enter username: ")
        if not username:
            print(Fore.RED + "Username cannot be empty.Press Enter to continue...")
            input()
            continue
        elif len(username) < 3:
            print(
                Fore.RED
                + "Username must be at least 3 characters long. Press Enter to continue..."
            )
            input()
            continue
        elif utils.search_user(username):
            print(
                Fore.RED
                + "This username is already Taken . press Enter to try agein..."
            )
            input()
            continue
        else:
            break
    while True:
        password = input(Fore.YELLOW + "enter your password: ")
        if len(password) < 6:
            print(
                Fore.RED
                + "password must be at least 6 characters long. press Enter to press continue..."
            )
            input()
            continue
        else:
            password_hash = utils.password_to_hash(password)
            utils.insert_add_user(username, password_hash)
            print(Fore.RED + "User Added successfully.press Enter to continue")
            input()
            break
