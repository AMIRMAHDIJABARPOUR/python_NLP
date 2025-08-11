from collections import Counter
from colorama import init, Fore, Style
import models, utils, pyfiglet, sqlite3


Welcome = "welcome to the Application"
init(autoreset=True)
utils.build_database()
while True:
    # ==========start-of-choice-handling==========
    print(Fore.YELLOW + pyfiglet.figlet_format(Welcome))
    print(
        Fore.GREEN
        + "[1] User Management\n[2] Notes Management\n[3] Text Analysis\n[4] Search Engine\n[5] Backup & Archive\n[6] Reports\n[7] Custom Tools\n[0] Exit"
    )
    choice = int(input(Fore.YELLOW + "Please select an option: " + Style.RESET_ALL))
    # ==============User Management===============
    if choice == 1:  # User Management condition
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
        elif user_choice == 2:  # edit user(only admin , editor can edit)
            username, password, role = utils.login()
            if role in ["admin", "editor"]:
                models.edit_user(username, password)
                break
            else:
                print(Fore.RED + "you must be admin or editor to edit Uesr...")
                input()
                continue
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
            users = cursor.execute("SELECT username , role FROM USERS")
            for user in users:
                print(
                    Fore.BLUE
                    + f"username: {Fore.WHITE+user[0]} {Fore.LIGHTBLUE_EX}role : "
                    + Fore.WHITE
                    + user[1]
                )
            print(Fore.LIGHTGREEN_EX + "press enter to continue...")
            input()
            continue
        elif user_choice == 5:
            continue
        else:
            utils.InvalidChoice()
    # ==============Notes Management===============

    elif choice == 2:  # Notes Management condition
        print(Fore.BLUE + pyfiglet.figlet_format("Notes Management"))
        print(
            Fore.BLUE
            + "********************************************************************"
        )
        print(
            Fore.GREEN
            + "[1] Add New Note\n[2] Edit Note \n[3] Delete Note\n[4] List All Notes\n[5] Back"
        )
        user_choice = int(input(Fore.YELLOW + "Please select an option: "))
        if user_choice == 1:  # add note
            username, password, role = utils.login()
            models.add_new_notes(username)
            print(Fore.GREEN + "adding note was successful ...")
            input()
        elif (
            user_choice == 2
        ):  # edit note(only editor and admin can edit all notes viewers can edit their own note)
            username, password, role = utils.login()
            if role == "admin" or role == "editor":
                print(
                    Fore.LIGHTYELLOW_EX
                    + "Here are the notes. You should enter the note ID to edit it. 👇👇👇\n"
                )
                utils.print_all_notes()
                while True:
                    id_choice = int(
                        input("Enter the ID of the note you want to edit: ")
                    )
                    if utils.check_id_in_notes(user_id=id_choice):
                        models.edit_note(id_choice)
                        print(Fore.GREEN + "\n Note was edited successfully...")
                        input()
                        break
                    else:
                        print(Fore.RED + "invalid id")
                        input()
                        continue
            elif role == "viewer":
                print(
                    Fore.LIGHTYELLOW_EX
                    + "Here are the notes. You should enter the note ID to edit it. 👇👇👇"
                )
                utils.print_user_notes(username=username)
                while True:
                    id_choice = int(input("Enter the ID of the note you want to edit."))
                    if utils.check_id_in_notes(
                        user_id=id_choice
                    ) and utils.check_note_ownership(
                        note_id=id_choice, username=username
                    ):
                        models.edit_note(id_choice)
                        print(Fore.GREEN + "\n Note was edited successfully...")
                        input()
                        break
                    else:
                        print(Fore.RED + "invalid id")
                        input()
                        continue

        elif (
            user_choice == 3
        ):  # DELETE note (Only users and admins can delete all notes; viewers can edit their own notes.)
            username, password, role = utils.login()
            if role == "admin" or role == "editor":
                print(
                    Fore.LIGHTYELLOW_EX
                    + "Here are the notes. You should enter the note ID to DELETE it. 👇👇👇"
                )
                utils.print_all_notes()
                while True:
                    id_choice = int(
                        input("Enter the ID of the note you want to Delete: ")
                    )
                    if utils.check_id_in_notes(user_id=id_choice):
                        models.delete_note(id_choice)
                        break
                    else:
                        print(Fore.RED + "invalid id...")
                        input()
                        continue
            elif role == "viewer":
                print(
                    Fore.LIGHTYELLOW_EX
                    + "Here are the notes. You should enter the note ID to Delete it. 👇👇👇"
                )
                utils.print_user_notes(username=username)
                while True:
                    id_choice = int(
                        input("Enter the ID of the note you want to Delete: ")
                    )
                    if utils.check_id_in_notes(
                        user_id=id_choice
                    ) and utils.check_note_ownership(
                        note_id=id_choice, username=username
                    ):
                        models.delete_note(id_choice)
                        break
                    else:
                        print(Fore.RED + "invalid id...")
                        input()
                        continue

        elif user_choice == 4:  # LIST OF NOTES (Viewers can see only their notes)
            username, password, role = utils.login()
            if role == "admin" or role == "editor":
                utils.print_all_notes()
                print(Fore.GREEN + "continue... ")
                input()
            elif role == "viewer":
                utils.print_user_notes(username=username)
                print(Fore.GREEN + "continue... ")
                input()
        elif user_choice == 5:
            continue
        else:
            print(Fore.RED + "invalid choice...")
            input()

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
        input()
        break
    else:
        utils.InvalidChoice()
