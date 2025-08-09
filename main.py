from collections import Counter
from colorama import init, Fore, Style
import models
import utils
import pyfiglet

Welcome = "welcome to the Application"
init(autoreset=True)

for i in range(3):
    # ==========start-of-choice-handling==========
    print(Fore.YELLOW + pyfiglet.figlet_format(Welcome))
    print(
        Fore.GREEN
        + "[1] User Management\n[2] Notes Management\n[3] Text Analysis\n[4] Search Engine\n[5] Backup & Archive\n[6] Reports\n[7] Custom Tools\n[0] Exit"
    )
    choice = int(input(Fore.YELLOW + "Please select an option: " + Style.RESET_ALL))
    # ==============User Management===============
    if choice == 1:
        print(
            Fore.GREEN
            + "[1] Add New User \n[2] Edit User \n[3] Delete User \n[4] List All Users\n[5] Back \n"
        )
        user_choice = int(
            input(Fore.YELLOW + "Please select an option: " + Style.RESET_ALL)
        )
        if user_choice == 1:
            models.add_user()
        elif user_choice == 2:
            models.edit_user()
        elif user_choice == 3:
            models.delete_user()
        elif user_choice == 4:
            models.list_users()
        elif user_choice == 5:
            continue
        else:
            utils.InvalidChoice()

    elif choice == 2:
        print(Fore.GREEN + "User Management selected.")
    elif choice == 3:
        pass
    elif choice == 4:
        pass
    elif choice == 5:
        pass
    elif choice == 6:
        pass
    elif choice == 7:
        pass
    elif choice == 0:
        pass
    else:
        utils.InvalidChoice()
