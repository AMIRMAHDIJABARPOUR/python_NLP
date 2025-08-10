from collections import Counter
from colorama import init, Fore, Style
import models, utils, pyfiglet, sqlite3


Welcome = "welcome to the Application"
init(autoreset=True)
utils.build_database()
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
        print(Fore.BLUE + pyfiglet.figlet_format("User Management"))
        print(
            Fore.BLUE
            + "*************************************************************\n"
        )
        print(
            Fore.GREEN
            + "[1] Add New User \n[2] Edit User \n[3] Delete User \n[4] List All Users\n[5] Back \n"
        )
        user_choice = int(
            input(Fore.YELLOW + "Please select an option: " + Style.RESET_ALL)
        )
        if user_choice == 1:  # adding user
            models.add_user()
            print(Fore.GREEN + "adding user successfully")
            input()
        elif user_choice == 2:  # edit user(only admin , editor can edit)
            while True:
                username = input(Fore.YELLOW + "username: ")
                if not utils.search_user(username):
                    print(Fore.RED + "invalid username")
                    input()
                    continue
                password = utils.get_password_with_username(username=username)
                if not utils.guss_password(password):
                    print(Fore.RED + "Incorrect password. Press Enter to try again...")
                    input()
                    continue
                role = utils.get_role_with_username(username=username)
                if not utils.check_promise(username, "admin", "editor"):
                    print(Fore.RED + "you must be admin or editor to edit Uesr...")
                    input()
                else:
                    models.edit_user(username, password)
                    break
        elif user_choice == 3:  # delete user (only admin can delete user)
            my_username, password_hash, role = utils.login()
            if role == "admin":
                while True:
                    deleted_username = input(
                        Fore.YELLOW + "Who do you want to delete? "
                    )
                    if utils.search_user(deleted_username):
                        models.delete_user(deleted_username)
                        print(Fore.RED + f"{deleted_username} was deleted ...")
                        input()
                        break
                    else:
                        print(Fore.RED + "wrong username ....")
                        input()
                        continue
            else:
                print(Fore.RED + "Do not have access (only admin can delete user) ...")
                input()
                continue
        elif user_choice == 4:  # users list(all roles can see this part)
            conn = sqlite3.connect("db/Notes.db")
            cursor = conn.cursor()
            Notes = cursor.execute(
                "select U.username , N.note from USERS as U join NOTES as N on U.username=N.username"
            )
            for note in Notes:
                print(Fore.BLUE + f"{note[0]} note : " + Fore.WHITE + note[1])
            print(Fore.LIGHTGREEN_EX + "press enter to continue...")
            input()
            continue
        elif user_choice == 5:
            continue
        else:
            utils.InvalidChoice()
    # ==============Notes Management===============

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
        print(Fore.RED + "Goodbye...")
    else:
        utils.InvalidChoice()
