import utils, spacy, sqlite3, re, json, sys, pickle, zipfile, os, time, logging, argparse, shutil, datetime, spacy
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
            Fore.CYAN + "Enter username to edit: " + Style.RESET_ALL
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
                Fore.CYAN + "Choose an option to edit: " + Style.RESET_ALL
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
                        Fore.CYAN
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
                    logging.info(
                        f"Username edited for {target_username} to {new_username} by {admin_username}"
                    )
                    print(Fore.GREEN + "Username successfully edited")
                    break
            elif choice == 2:
                while True:
                    password_input = input(
                        Fore.CYAN
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
                    logging.info(
                        f"Password edited for {target_username} by {admin_username}"
                    )
                    print(Fore.GREEN + "Password successfully edited")
                    break
            elif choice == 3:
                acceptable_roles = ["admin", "editor", "viewer"]
                while True:
                    role_input = input(
                        Fore.CYAN
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
                    logging.info(
                        f"Role edited for {target_username} to {new_role} by {admin_username}"
                    )
                    print(Fore.GREEN + "Role successfully edited")
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
            logging.info(f"User {target_username} updated by {admin_username}")
            print(Fore.GREEN + "User updated successfully! Press Enter to return...")
            input()
        else:
            print(Fore.YELLOW + "No changes made. Press Enter to return...")
            input()
        break


def delete_user(username, *args):  # delete user function
    if utils.search_user(username):
        with sqlite3.connect("db/Notes.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM NOTES WHERE username = ?", (username,))
            cursor.execute("DELETE FROM USERS WHERE username = ?", (username,))
            conn.commit()
        logging.info(f"User {username} successfully deleted by {args[0]}")
        print(f"{Fore.GREEN}User {username} successfully deleted")
    else:
        logging.warning(f"User {username} not found")
        print(f"{Fore.RED}User {username} not found")


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
                if utils.check_id_in_notes(note_id):
                    break
                else:
                    print(Fore.RED + "invalid id ...")
                    input()
            except:
                print(Fore.RED + "invalid id ....")
                input()
        note = utils.return_notes_custom(2, int(note_id))
        if not note:
            print(Fore.RED + "Note not found ...")
            input()
            return
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
                    try:
                        for tag in json.loads(note[4]):
                            print(tag, end="  ")
                    except:
                        print(None)
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
    utils.print_two_member_tuple_to_dictionary(tuple_index)
    input(Fore.GREEN + "\n continue...")


def save_index(inverted_index):  # save index
    with open("index/inverted_index.pkl", "wb") as file:
        pickle.dump(inverted_index, file)
    print(Fore.GREEN + "Inverted index saved successfully.")
    input()


def load_index():
    index_file = "index/inverted_index.pkl"
    if not os.path.exists(index_file):
        logging.warning("Inverted index file not found: index/inverted_index.pkl")
        print(f"{Fore.RED}Inverted index file not found: index/inverted_index.pkl")
        input(f"{Fore.YELLOW}Press Enter to continue...")
        return {}
    with open(index_file, "rb") as f:
        index = pickle.load(f)
        logging.info("Inverted index loaded: index/inverted_index.pkl")
        print(
            f"{Fore.GREEN}Inverted index loaded successfully: index/inverted_index.pkl"
        )
        input(f"{Fore.YELLOW}Press Enter to continue...")
        return index


####################################################section five #########################################################


def create_backup(backup_path="backups/"):  # create bckup

    try:
        backup_file = os.path.join(
            backup_path, f"backup_{time.strftime("%Y%m%d_%H%M%S")}.zip"
        )

        zip_files_list = [
            "db/Notes.db",
            "index/inverted_index.pkl",
            "logs/logs.txt",
            "reports/report.txt",
        ]

        files_backed_up = []

        with zipfile.ZipFile(backup_file, "w", zipfile.ZIP_DEFLATED) as z:
            for file in zip_files_list:
                if os.path.exists(file):
                    z.write(file, arcname=os.path.basename(file))
                    files_backed_up.append(file)
                else:
                    logging.warning(f"File not found for backup: {file}")

        if not files_backed_up:
            logging.warning(f"No files were backed up in {backup_file}")
            print(f"{Fore.RED}No files were backed up.")
            return

        print(f"{Fore.GREEN}Backup created successfully: {backup_file}")
        input()

    except:
        logging.error(f"Failed to create backup")
        print(f"{Fore.RED}Error creating backup")


def restore_backup(backup_path="backups/"):
    try:

        if not os.path.exists(backup_path):
            logging.error(f"Backup directory not found: {backup_path}")
            print(f"{Fore.RED}Backup directory not found: {backup_path}")
            input()
            return

        backups = [f for f in os.listdir(backup_path) if f.endswith(".zip")]

        if not backups:
            logging.warning(f"No backups found in {backup_path}")
            print(f"{Fore.RED}No backups found in {backup_path}")
            return

        print(f"{Fore.BLUE}Available backups:")
        for i, backup in enumerate(backups, 1):
            print(f"[{i}] {backup}")

        choice = input(f"{Fore.YELLOW}Enter backup number to restore: ")

        try:
            choice = int(choice) - 1
            if 0 <= choice < len(backups):
                backup_file = os.path.join(backup_path, backups[choice])

                with zipfile.ZipFile(backup_file, "r") as z:
                    for file in z.namelist():
                        if file in [
                            "Notes.db",
                            "logs.txt",
                            "report.txt",
                            "inverted_index.pkl",
                        ]:
                            dest_dir = {
                                "Notes.db": "db",
                                "logs.txt": "logs",
                                "report.txt": "reports",
                                "inverted_index.pkl": "index",
                            }[file]
                            os.makedirs(dest_dir, exist_ok=True)

                            z.extract(file, dest_dir)

                logging.info(f"Backup restored: {backup_file}")
                print(f"{Fore.GREEN}Backup restored successfully: {backup_file}")
                input()
            else:

                logging.warning(f"Invalid backup number: {choice + 1}")
                print(f"{Fore.RED}Invalid backup number")
        except ValueError:

            logging.warning(f"Invalid input for restore: {choice}")
            print(f"{Fore.RED}Invalid input")

    except Exception as e:
        logging.error(f"Failed to restore backup: {str(e)}")
        print(f"{Fore.RED}Error restoring backup: {str(e)}")


def list_backups(backup_path="backups/"):

    try:
        if not os.path.exists(backup_path):
            logging.error(f"Backup directory not found: {backup_path}")
            print(f"{Fore.RED}Backup directory not found: {backup_path}")
            return
        backups = [f for f in os.listdir(backup_path) if f.endswith(".zip")]
        if not backups:
            logging.warning(f"No backups found in {backup_path}")
            print(f"{Fore.RED}No backups found in {backup_path}")
            return
        print(f"{Fore.BLUE}Available backups:")
        for i, backup in enumerate(backups, 1):
            print(f"[{i}] {backup}")
        logging.info(f"Listed backups in {backup_path}")
    except Exception as e:
        logging.error(f"Failed to list backups: {str(e)}")
        print(f"{Fore.RED}Error listing backups: {str(e)}")
    input()


def configure_backup_path():

    parser = argparse.ArgumentParser(description="Configure backup path")

    parser.add_argument(
        "--backup-path", default="backups/", help="Path to store backups"
    )

    args = parser.parse_args()
    backup_path = args.backup_path

    try:
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
            logging.info(f"Created backup directory: {backup_path}")
            print(f"{Fore.YELLOW}Created backup directory: {backup_path}")

        if not os.access(backup_path, os.W_OK):
            raise PermissionError(f"No write permission for {backup_path}")

        logging.info(f"Backup path configured: {backup_path}")
        print(f"{Fore.GREEN}Backup path set to: {backup_path}")
        input()
        return backup_path

    except Exception as e:
        logging.error(f"Failed to configure backup path: {str(e)}")
        print(f"{Fore.RED}Error configuring backup path: {str(e)}")
        return "backups/"


def generate_text_report():
    os.makedirs("reports", exist_ok=True)
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM USERS")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM NOTES")
        total_notes = cursor.fetchone()[0]
        cursor.execute("SELECT note FROM NOTES")
        notes = [row[0] for row in cursor.fetchall()]

    all_words = []
    for note in notes:
        words = [word.lower() for word in note.split() if word.isalpha()]
        all_words.extend(words)
    total_words = len(all_words)
    top_words = Counter(all_words).most_common(5)

    report_content = f"Smart Notebook Report\n"
    report_content += (
        f"Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    report_content += f"{'-' * 50}\n"
    report_content += f"Total Users: {total_users}\n"
    report_content += f"Total Notes: {total_notes}\n"
    report_content += f"Total Words: {total_words}\n"
    report_content += f"Top 5 Frequent Words:\n"
    for word, count in top_words:
        report_content += f"  {word}: {count}\n"

    with open("reports/report.txt", "w", encoding="utf-8") as f:
        f.write(report_content)

    try:
        logging.info("Text report generated: reports/report.txt")
        print(f"{Fore.GREEN}Text report generated successfully: reports/report.txt")
        input()
    except Exception as e:
        print("log failed")
        input()


def show_logs():
    if not os.path.exists("logs/logs.txt"):
        logging.warning("Log file not found: logs/logs.txt")
        print(f"{Fore.RED}Log file not found: logs/logs.txt")
        return

    with open("logs/logs.txt", "r", encoding="utf-8") as f:
        logs = f.readlines()
        if not logs:
            print(f"{Fore.YELLOW}Log file is empty.")
            return
        print(f"{Fore.BLUE}Log Contents:")
        for log in logs:
            print(f"{Fore.CYAN}{log.strip()}")
        input()

        logging.info("Displayed log file: logs/logs.txt")


def generate_pdf_report():
    print(f"{Fore.GREEN} coming soon...")
    input()
