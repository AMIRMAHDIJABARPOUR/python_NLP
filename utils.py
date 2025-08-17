import sqlite3, hashlib, json, spacy, logging, nltk
from colorama import init, Fore

init(autoreset=True)  # Initialize colorama for colored output


def build_log(username, message):
    logging.info(Fore.BLUE + f"{username} : " + Fore.GREEN + f"{message}")


def two_member_tuple_to_dictionary(
    list_of_tuples,
):  # return dictionary from list of dual member tuples
    returned_dict = {}
    for member in list_of_tuples:
        returned_dict[member[0]] = member[1]
    return returned_dict


def build_database():  # creating database
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS USERS (username text primary key, password text , role text)"
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS NOTES (id integer primary key AUTOINCREMENT ,username TEXT, subject text, note text ,Tags TEXT, FOREIGN KEY (username) REFERENCES USERS(username))"""
        )
        conn.commit()


def InvalidChoice():  # when chice is not correct
    print(Fore.RED + "Invalid choice. Press enter to continue.")
    input()


def search_user(username):  # searching username in database(return boolian)
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select u.username from USERS as u   where username =?   ",
            (username,),
        )
        if cursor.fetchall():
            return True
        else:
            return False


def password_to_hash(password):  # get password hash
    return hashlib.sha256(password.encode()).hexdigest()


def insert_add_user(
    username, password_hash, role
):  # insert data in USERS TABLE ON database
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO USERS (username,password,role) VALUES (?,?,?)",
            (username, password_hash, role),
        )
        conn.commit()


def set_username(
    massage, edit
):  # get new username (The one that doesnt exist in the database)
    while True:
        username = input(Fore.YELLOW + f"{massage} ")
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
        elif not edit and search_user(username):
            print(
                Fore.RED
                + "This username is already Taken . press Enter to try agein..."
            )
            input()
            continue
        else:
            return username


def set_passwoed(massage):  # set valid password
    while True:  # set password
        password = input(Fore.YELLOW + f"{massage} ")
        if len(password) < 6:
            print(
                Fore.RED
                + "password must be at least 6 characters long. press Enter to press continue..."
            )
            input()
            continue
        else:
            password_hash = password_to_hash(password)
            return password_hash


def set_role(massage):  # set valid role
    acceptable_roles = ["admin", "editor", "viewer"]

    while True:
        role = input(Fore.YELLOW + f"{massage}")
        if not role:
            print(Fore.RED + "you shuld set a role ")
            input()
            continue
        elif role.lower() not in acceptable_roles:
            print(Fore.RED + "Enter The valid role...")
            input()
            continue
        else:
            return role


def get_password_with_username(username):  # get password hash with username
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM USERS WHERE username = ?", (username,))
        return cursor.fetchone()[0]


def get_role_with_username(username):  # get user role with username
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select role from USERS where username = ?", (username,))
        return cursor.fetchone()[0]


def guss_password(true_password):  # chances to guss true password
    for guss_number in range(3, -1, -1):
        guss = input(Fore.YELLOW + "please enter your password: ")
        if password_to_hash(guss) == true_password:
            return True
        elif guss_number <= 0:
            return False
        else:
            print(f"invalid password {guss_number} left")


def update_userpass(
    old_username, old_password, new_username, new_password, new_role
):  # updating True username and password

    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE USERS SET username = ?, password = ?, role = ? WHERE username = ? AND password = ?",
            (new_username, new_password, new_role, old_username, old_password),
        )
        conn.commit()


def check_promise(username, *args):  # checking promise
    allowed_roles = list(args)
    role = get_role_with_username(username=username)
    if role in allowed_roles:
        return True
    else:
        return False


# =================================================== section two ====================================================
def login():  # for logging in to an account (return username , password , role )

    while True:
        username = input(Fore.YELLOW + "username: ")
        if not search_user(username):
            print(Fore.RED + "invalid username")
            input()
            continue
        password = get_password_with_username(username=username)
        if not guss_password(password):
            print(Fore.RED + "Incorrect password. Press Enter to try again...")
            input()
            continue
        role = get_role_with_username(username=username)
        return username, password, role


def get_notes():  # get subject and notes and tags(json.dumps(tags))

    while True:
        subject = input(Fore.YELLOW + "Enter the subject: ")
        if len(subject) < 5 or len(subject) > 50:
            print(Fore.RED + "The subject must be between 5 and 50 characters...")
            input()
            continue
        else:
            break
    while True:
        note = input(Fore.YELLOW + "Enter the note: ")
        if len(note) < 20 or len(note) > 5000:
            print(Fore.RED + "The note must be between 20 and 5000 characters...")
            input()
            continue
        else:
            break
    while True:
        big_tag = input(Fore.YELLOW + "Enter tags (use , to separate each element): ")
        if len(big_tag) < 10:
            print(Fore.RED + "The tag must be over 10 characters")
            input()
            continue
        else:
            temp_tags = list(big_tag.split(","))
            tags = json.dumps(list(map(lambda item: item.strip(), temp_tags)))
            break
    return subject, note, tags


def check_user_have_note(username):  # checks if the user has any notes

    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select * from NOTES WHERE username = ?", (username,))
        result = cursor.fetchall()
        if result:
            return True
        else:
            return False


def check_id_in_notes(user_id):  # Checks if the ID exists in the notes.
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select * from NOTES WHERE id = ?", (user_id,))
        result = cursor.fetchall()
        if result:
            return True
        else:
            return False


def print_user_notes(username):  # Print notes Wrriten by user
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select * FROM NOTES WHERE username = ? ORDER BY username",
            (username,),
        )
        result = cursor.fetchall()
        for note in result:
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


def print_note_by_id(note_id):  # Print a single note by its ID
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM NOTES WHERE id = ?",
            (note_id,),
        )
        note = cursor.fetchone()
        if note:
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
        else:
            print(Fore.RED + f"No note found with ID {note_id}")


def print_all_notes():  # All users Notes
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select * FROM NOTES ORDER BY username ")
        result = cursor.fetchall()
        for note in result:
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
                print("None")
            print(
                "\n================================================================================\n"
            )


def check_note_ownership(note_id, username):  # Checks if the note belongs to the user
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM NOTES WHERE id = ?", (note_id,))
        result = cursor.fetchone()
        if result and result[0] == username:
            return True
        else:
            return False


def return_notes_custom(  # return all notes(if user_input=1) else return notes with id
    user_input: int, *args
):

    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        if user_input == 1:
            cursor.execute("select note FROM NOTES ORDER BY username ")
            result = cursor.fetchall()
            return result
        elif user_input == 2:
            if args:
                if check_id_in_notes(args[0]):
                    cursor.execute("select note FROM NOTES WHERE id = ? ", (args[0],))
                    result = cursor.fetchall()
                    return result
                else:
                    print(Fore.RED + "invalid id ...")
                    input()


def return_all_notes_elemans_custom(
    user_input: int, *args, offset: int = 0, limit: int = None
):
    with sqlite3.connect("db/Notes.db") as conn:
        cursor = conn.cursor()
        if user_input == 1:
            query = (
                "SELECT id, username, subject, note, Tags FROM NOTES ORDER BY username"
            )
            if limit is not None:
                query += " LIMIT ? OFFSET ?"
                cursor.execute(query, (limit, offset))
            else:
                cursor.execute(query)
            return cursor.fetchall()
        elif user_input == 2:
            if args:
                try:
                    note_id = int(args[0])
                    if check_id_in_notes(note_id):
                        cursor.execute(
                            "SELECT id, username, subject, note, Tags FROM NOTES WHERE id = ?",
                            (note_id,),
                        )
                        result = cursor.fetchall()
                        return result[0] if result else []
                    else:
                        print(Fore.RED + "Invalid id...")
                        input()
                        return []
                except (ValueError, IndexError):
                    print(Fore.RED + "Invalid id...")
                    input()
                    return []
            return []


def edit_words_dictionary(
    all_words_dictionary, specific_note_dicionary
):  # edit dictionary(if key exist update else append)

    for key, value in specific_note_dicionary.items():
        if key.lower() in all_words_dictionary.keys():
            all_words_dictionary[key.lower()] += value
        else:
            all_words_dictionary[key.lower()] = value
    return all_words_dictionary


def print_dictionary(my_dict):  # print all dictionary data
    for key, value in my_dict.items():
        print(Fore.GREEN + f"{key}  :   {value}")


def print_two_member_tuple_to_dictionary(
    list_of_tuples, *args
):  # print dictionary from list of dual member tuples (in range args if not args print all)

    if not list_of_tuples:
        print(Fore.RED + "No items to display")
        return
    if not args:
        for member in list_of_tuples:
            print(Fore.GREEN + f"{member[0]} : " + Fore.BLUE + f"{member[1]}")
    else:
        num_items = int(args[0]) if args and args[0] and str(args[0]).isdigit() else 0
        if num_items <= 0:
            print(Fore.RED + "Invalid number of items to display")
            return
        for i in range(min(num_items, len(list_of_tuples))):
            print(
                Fore.GREEN
                + f"{list_of_tuples[i][0]} : "
                + Fore.BLUE
                + f"{list_of_tuples[i][1]}"
            )


nltk.download("punkt", quiet=True)


def convert_sentence_to_word(note):
    return [
        word.lower()
        for word in nltk.tokenize.word_tokenize(note)
        if word.isalpha() and len(word) > 1
    ]


def append_dictionary_with_id(main_dict: dict, append_list: list, note_id: int):
    for word in append_list:
        if word in main_dict:
            if not note_id in main_dict[word]:
                main_dict[word].append(note_id)
        else:
            main_dict[word] = [note_id]
    return main_dict


def append_dictionary_to_dictionary(
    main_dictionary: dict, appended_dictionary: dict
) -> dict:
    for key, value in appended_dictionary.items():
        if key in main_dictionary:
            main_dictionary[key] = list(set(main_dictionary[key] + value))
        else:
            main_dictionary[key] = value
    return main_dictionary
