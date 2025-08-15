import utils, spacy, sqlite3, re, json, sys, pickle
from colorama import init, Fore, Style
from collections import Counter, defaultdict


init(autoreset=True)
################################################section one#########################################################


def add_user():  # add user function

    username = utils.set_username(massage="Enter username: ", edit=False)  # setusername
    password = utils.set_passwoed("enter your password:")
    role = utils.set_role("please Enter The role:")
    utils.insert_add_user(username, password, role)
    print(Fore.GREEN + "User Added successfully.press Enter to continue")
    utils.build_log(username=f"User Added ", message=f"{username} Added successfully")
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
                    utils.build_database(
                        username=admin_username, message="Username Successfuly eddited"
                    )
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
                    utils.build_database(
                        username=admin_username, message="Password successfuly edited "
                    )
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
                    utils.build_database(
                        username=admin_username, message="Role successfuly edited "
                    )
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


def delete_user(username, *args):  # delete user funcrion

    if utils.search_user(username):
        with sqlite3.connect("db/Notes.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM USERS WHERE Username = ?", (username,))
            conn.commit()
            conn.close()
        utils.build_database(
            username=args[0], message=f"{username} successfuly deleted"
        )


def list_of_all_users():
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


####################################################section three#########################################################


def top_frequent_words():  # print frequent word
    all_words_dictionary = dict()
    nlp = spacy.load("en_core_web_sm")
    print(Fore.BLUE + "[1] for all notes\n[2] for a spacific note ")
    while True:
        try:
            text_analysis_choice = int(input(Fore.YELLOW + "Please select an option: "))
            if text_analysis_choice in [1, 2]:
                break
            else:
                print(Fore.RED + "invalid choice")
                input()
                continue
        except ValueError:
            print(Fore.RED + "invalid choice")
            input()
            continue
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

        if discuss == "1":
            utils.print_two_member_tuple_to_dictionary(most_common_tuple_list)
            input()
    elif text_analysis_choice == 2:  # to see spacific note
        print(
            Fore.LIGHTYELLOW_EX
            + "Here are the notes. You should enter the note ID to edit it. 👇👇👇\n"
        )
        utils.print_all_notes()
        while True:
            try:
                note_id = int(input(Fore.BLUE + "Enter note id : "))
                break
            except:
                print(Fore.RED + "invalid id ....")
                input()
                continue
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
        if discuss == "1":
            utils.print_two_member_tuple_to_dictionary(custom_words_tuple)
            input()

    else:
        print(Fore.RED + "invalid choice...")
        input()


def custom_tokenizer(my_token: str, *args):  # Escape special regex characters
    my_token = re.escape(my_token)  # Escape special regex characters
    note_ids = []
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        if not args:
            cursor.execute("SELECT id, subject, note FROM NOTES")
            database_notes_tuples = cursor.fetchall()
            for note in database_notes_tuples:
                try:
                    if (note[1] and re.findall(my_token, note[1], re.IGNORECASE)) or (
                        note[2] and re.findall(my_token, note[2], re.IGNORECASE)
                    ):
                        note_ids.append(note[0])
                except:
                    print(Fore.RED + "invalid token ...")
                    input()
                    continue
            if not note_ids:
                print(Fore.RED + f"No notes found containing the token '{my_token}'...")
                input()
                return
            for note_id in note_ids:
                note = utils.return_all_notes_elemans_custom(2, note_id)
                if not note:
                    print(Fore.RED + f"Note with ID {note_id} not found...")
                    input()
                    continue
                try:
                    print(
                        Fore.BLUE
                        + "note id: "
                        + Fore.GREEN
                        + str(note[0])
                        + "         "
                        + Fore.BLUE
                        + "username: "
                        + Fore.GREEN
                        + note[1]
                        + Fore.BLUE
                        + "         "
                        + "subject: "
                        + Fore.GREEN
                        + note[2]
                    )
                    for i in range(0, len(note[3]), 80):
                        print(Fore.WHITE + note[3][i : i + 80])
                    print(Fore.GREEN + "tags: ", end="")
                    for tag in json.loads(note[4]):
                        print(tag, end="  ")
                    print(
                        "\n================================================================================\n"
                    )
                except:
                    print(Fore.RED + "invalid token ...")
                    input()
                    continue
        else:
            try:
                user_note_id_choice = int(args[0])
                if not utils.check_id_in_notes(user_note_id_choice):
                    print(Fore.RED + f"Note with ID {user_note_id_choice} not found...")
                    input()
                    return
                note = utils.return_all_notes_elemans_custom(2, user_note_id_choice)
                if not note:
                    print(Fore.RED + f"Note with ID {user_note_id_choice} not found...")
                    input()
                    return
                if (note[2] and re.findall(my_token, note[2], re.IGNORECASE)) or (
                    note[3] and re.findall(my_token, note[3], re.IGNORECASE)
                ):
                    print(
                        Fore.GREEN
                        + f"Your custom token '{my_token}' exists in note ID {user_note_id_choice}..."
                    )
                    print(
                        Fore.BLUE
                        + "note id: "
                        + Fore.GREEN
                        + str(note[0])
                        + "         "
                        + Fore.BLUE
                        + "username: "
                        + Fore.GREEN
                        + note[1]
                        + Fore.BLUE
                        + "         "
                        + "subject: "
                        + Fore.GREEN
                        + note[2]
                    )
                    for i in range(0, len(note[3]), 80):
                        print(Fore.WHITE + note[3][i : i + 80])
                    print(Fore.GREEN + "tags: ", end="")
                    for tag in json.loads(note[4]):
                        print(tag, end="  ")
                    print(
                        "\n================================================================================\n"
                    )
                else:
                    print(
                        Fore.RED
                        + f"No token '{my_token}' found in note ID {user_note_id_choice}..."
                    )
                    input()
            except:
                print(Fore.RED + "invalid token ...")
                input()
                return


####################################################section four#########################################################


from multiprocessing import Pool


def build_inverted_index():
    batch_size = 1000
    offset = 0
    inverted_index = defaultdict(list)

    # شمارش تعداد کل نوت‌ها
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM NOTES")
        total_notes = cursor.fetchone()[0]

    # پردازش بچ‌ها
    with Pool() as pool:
        while offset < total_notes:
            all_notes = utils.return_all_notes_elemans_custom(
                1, offset=offset, limit=batch_size
            )
            if not all_notes:
                break
            for note in all_notes:
                note_tokens = utils.convert_sentence_to_word(note=note[2])
                note_tokens.extend(utils.convert_sentence_to_word(note=note[3]))
                utils.append_dictionary_with_id(
                    main_dict=inverted_index, append_list=note_tokens, note_id=note[0]
                )
            offset += batch_size
            sys.stdout.write(
                f"\r{Fore.BLUE}{min(offset, total_notes)} notes out of {total_notes} notes were processing!"
            )
            sys.stdout.flush()

    sys.stdout.write("\r\nfinish\n")
    sys.stdout.flush()
    return inverted_index


def search_keyword(user_search, inverted_index):
    Tokens = utils.convert_sentence_to_word(user_search)
    searched_note_ids_list = []
    if inverted_index:
        for word in Tokens:
            if word in inverted_index:
                searched_note_ids_list.extend(inverted_index[word])

    return searched_note_ids_list


def show_search_stats(search_status):

    tuple_index = tuple(search_status.items())
    print(utils.two_member_tuple_to_dictionary(tuple_index))
    input(Fore.GREEN + "\n continue...")


def save_index(inverted_index):  # save index
    with open("index/inverted_index.pkl", "wb") as file:
        pickle.dump(inverted_index, file)
    print(Fore.GREEN + "Inverted index saved successfully.")
    input()


def load_index():
    pickle_file_path = "index/inverted_index.pkl"
    try:
        with open(pickle_file_path, "rb") as file:
            inverted_index = pickle.load(file)
        print(Fore.GREEN + "Inverted index loaded successfully.")
        return inverted_index
    except FileNotFoundError:
        print(Fore.RED + "Inverted index file not found. Please build the index first.")
        input()
        return None
