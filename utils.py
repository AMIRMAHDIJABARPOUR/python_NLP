import sqlite3
import hashlib
from colorama import init, Fore

init(autoreset=True)


def build_database():  # creating database
    conn = sqlite3.connect("db/Notes.db")
    cursor = conn.cursor()
    cursor.execute(
        """
                   CREATE TABLE IF NOT EXISTS USERS (username text primary key, password text , role text)
                   """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS NOTES (id integer primary key,username TEXT, subject text, note text , FOREIGN KEY (username) REFERENCES USERS(username))"""
    )
    conn.commit()


def InvalidChoice():  # when chice is not correct
    print(Fore.RED + "Invalid choice. Press enter to continue.")
    input()


def search_user(username):  # searching user in database(return boolian)
    conn = sqlite3.connect("db/Notes.db")
    cursor = conn.cursor()
    cursor.execute(
        """
                   select u.username 
                   from USERS as u
                   where username =?
                   """,
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
    conn = sqlite3.connect("db/Notes.db")
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
    conn = sqlite3.connect("db/Notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM USERS WHERE username = ?", (username,))
    return cursor.fetchone()[0]


def get_role_with_username(username):  # get user role with username
    conn = sqlite3.connect("db/Notes.db")
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

    conn = sqlite3.connect("db/Notes.db")
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
