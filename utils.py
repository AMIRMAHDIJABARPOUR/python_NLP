import sqlite3
from colorama import init, Fore, Style

init(autoreset=True)


def InvalidChoice():
    print(Fore.RED + "Invalid choice. Press enter to continue.")
    input()


def build_database():
    conn = sqlite3.connect("db/Notes.db")
    cursor = conn.cursor()
    cursor.execute(
        """
                   CREATE TABLE IF NOT EXISTS USERS (username text primary key, password text)
                   """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS NOTES (id integer primary key,username text foreign key references USERS(username), subject text, note text)"""
    )
    conn.commit()
