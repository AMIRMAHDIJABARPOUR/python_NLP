from colorama import init, Fore, Style
import utils, spacy, sqlite3
from collections import Counter

init(autoreset=True)
################################################section one#########################################################


def add_user():  # add user function
    username = utils.set_username(massage="Enter username: ", edit=False)  # setusername
    password = utils.set_passwoed("enter your password:")
    role = utils.set_role("please Enter The role:")
    utils.insert_add_user(username, password, role)
    print(Fore.GREEN + "User Added successfully.press Enter to continue")
    input()


def edit_user(admin_username, admin_password_hash):  # edit user funcrion

    while True:
        if not utils.search_user(admin_username):
            print(
                Fore.RED + "Error: Admin username not found. Press Enter to return..."
            )
            input()
            return
        if not utils.check_promise(admin_username, "admin", "editor"):
            print(
                Fore.RED
                + "Error: You must be an admin or editor to edit users. Press Enter to return..."
            )
            input()
            return
        target_username = input(
            Fore.YELLOW + "Enter username to edit: " + Style.RESET_ALL
        )
        if not utils.search_user(target_username):
            print(
                Fore.RED + "Error: Target username not found. Press Enter to return..."
            )
            input()
            return
        current_role = utils.get_role_with_username(target_username)
        print(Fore.CYAN + f"Editing user: {target_username}")
        print(Fore.CYAN + f"Current role: {current_role}")
        new_username = target_username
        new_password = utils.get_password_with_username(target_username)
        new_role = current_role
        while True:
            print(
                Fore.GREEN
                + "[1] Change Username\n[2] Change Password\n[3] Change Role\n[4] Save and Exit"
            )
            choice_input = input(
                Fore.YELLOW + "Choose an option to edit: " + Style.RESET_ALL
            )
            if not choice_input.isdigit():
                print(
                    Fore.RED
                    + "Invalid option. Please enter a number. Press Enter to try again..."
                )
                input()
                continue
            choice = int(choice_input)
            if choice == 1:
                while True:
                    username_input = input(
                        Fore.YELLOW
                        + "Enter new username (Enter to keep current): "
                        + Style.RESET_ALL
                    )
                    if not username_input:
                        break
                    if len(username_input) < 3:
                        print(
                            Fore.RED
                            + "Username must be at least 3 characters long. Press Enter to try again..."
                        )
                        input()
                        continue
                    if (
                        utils.search_user(username_input)
                        and username_input != target_username
                    ):
                        print(
                            Fore.RED
                            + "Username already taken. Press Enter to try again..."
                        )
                        input()
                        continue
                    new_username = username_input
                    break
            elif choice == 2:
                while True:
                    password_input = input(
                        Fore.YELLOW
                        + "Enter new password (Enter to keep current): "
                        + Style.RESET_ALL
                    )
                    if not password_input:
                        break
                    if len(password_input) < 6:
                        print(
                            Fore.RED
                            + "Password must be at least 6 characters long. Press Enter to try again..."
                        )
                        input()
                        continue
                    new_password = utils.password_to_hash(password_input)
                    break
            elif choice == 3:
                acceptable_roles = ["admin", "editor", "viewer"]
                while True:
                    role_input = input(
                        Fore.YELLOW
                        + "Enter new role (admin/editor/viewer, Enter to keep current): "
                        + Style.RESET_ALL
                    )
                    if not role_input:
                        break
                    if role_input.lower() not in acceptable_roles:
                        print(
                            Fore.RED
                            + "Invalid role. Choose admin, editor, or viewer. Press Enter to try again..."
                        )
                        input()
                        continue
                    new_role = role_input.lower()
                    break
            elif choice == 4:
                break
            else:
                print(
                    Fore.RED
                    + "Invalid option. Please enter a number. Press Enter to try again..."
                )
                input()
        if (
            new_username != target_username
            or new_password != utils.get_password_with_username(target_username)
            or new_role != current_role
        ):
            utils.update_userpass(
                target_username,
                utils.get_password_with_username(target_username),
                new_username,
                new_password,
                new_role,
            )
            print(Fore.GREEN + "User updated successfully! Press Enter to return...")
            input()
        else:
            print(Fore.YELLOW + "No changes made. Press Enter to return...")
            input()
        break


def delete_user(username):  # delete user funcrion

    if utils.search_user(username):
        with sqlite3.connect("db/Notes.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM USERS WHERE Username = ?", (username,))
            conn.commit()
            conn.close()


####################################################section two#########################################################
def add_new_notes(username):  # adding new note (all roles)
    subject, note, tags = utils.get_notes()
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO NOTES (username , subject , note ,tags) VALUES(?,?,?,?)",
            (username, subject, note, tags),
        )
        conn.commit()


def edit_note(id_choice):  # edit note by getting note id

    subject, note, tags = utils.get_notes()
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE NOTES SET subject=? , note = ? , tags = ? WHERE id = ? ",
            (subject, note, tags, id_choice),
        )
        conn.commit()


def delete_note(id_choice):  # delete note by getting note id
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM NOTES WHERE id = ? ", (id_choice,))
        conn.commit()
    print(Fore.GREEN + "Note successfully Delete it.")
    input()


def top_frequent_words():
    all_words_dictionary = dict()
    nlp = spacy.load("en_core_web_sm")
    print(Fore.BLUE + "[1] for all notes\n[2] for a spacific note ")
    text_analysis_choice = int(input(Fore.YELLOW + "Please select an option: "))
    all_notes_text = ""
    if text_analysis_choice == 1:  # to see all notes analys
        text = ""
        all_text_notes = utils.return_notes_custom(1)
        for note in all_text_notes:
            text += note[0]
        doc = nlp(text)
        text_words_list = [token.text for token in doc if not token.is_punct]
        text_words_dictianary = Counter(text_words_list)
        print(Fore.BLUE + "here the top three words in all notes")
        most_common_tuple_list = text_words_dictianary.most_common()
        utils.print_two_member_tuple_to_dictionary(most_common_tuple_list, 3)
        print(Fore.BLUE + "[1] To see count of all words (press enter to go back)  ")
        discuss = input()
        if int(discuss) == 1:
            utils.print_two_member_tuple_to_dictionary(most_common_tuple_list)
    elif text_analysis_choice == 2:  # to see spacific note
        print(
            Fore.LIGHTYELLOW_EX
            + "Here are the notes. You should enter the note ID to edit it. 👇👇👇\n"
        )
        utils.print_all_notes()
        note_id = input(Fore.BLUE + "Enter note id : ")
        note = utils.return_notes_custom(2, int(note_id))
        nlp = spacy.load("en_core_web_sm")
        note_text = note[0][0]
        doc = nlp(note_text)
        custom_words_list = [token.text for token in doc if not token.is_punct]
        custom_words_dictionary = Counter(custom_words_list)
        print(Fore.BLUE + "here the top three words in this note")
        custom_words_tuple = custom_words_dictionary.most_common()
        utils.print_two_member_tuple_to_dictionary(custom_words_tuple, 3)
        print(
            Fore.BLUE
            + "[1] To see count of all words in this dictionary (press enter to go back)  "
        )
        discuss = input()
        if int(discuss) == 1:
            utils.print_two_member_tuple_to_dictionary(custom_words_tuple)

    else:
        print(Fore.RED + "invalid choice...")
        input()


print(top_frequent_words())
