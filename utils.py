import sqlite3
import hashlib
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
        """CREATE TABLE IF NOT EXISTS NOTES (id integer primary key,username TEXT, subject text, note text , FOREIGN KEY (username) REFERENCES USERS(username))"""
    )
    conn.commit()


def search_user(username):
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


def password_to_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def insert_add_user(username, password_hash):
    conn = sqlite3.connect("db/Notes.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO USERS (username,password) VALUES (?,?)", (username, password_hash)
    )
    conn.commit()
