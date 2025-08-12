from collections import Counter
from colorama import init, Fore, Style
import models, utils, pyfiglet, sqlite3, time, spacy
from collections import Counter

Welcome = "welcome to the Application"
init(autoreset=True)
utils.build_database()
while True:
    # ==========start-of-choice-handling==========
    print(Fore.YELLOW + pyfiglet.figlet_format(Welcome))
    print(
        Fore.GREEN
        + "[1] User Management\n[2] Notes Management\n[3] Text Analysis(only admin)\n[4] Search Engine\n[5] Backup & Archive\n[6] Reports\n[7] Custom Tools\n[0] Exit"
    )
    choice = int(input(Fore.YELLOW + "Please select an option: " + Style.RESET_ALL))
    # ====================================================== User Management ======================================================
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
    # ====================================================== Notes Management ======================================================

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
    # =================================================== Text Analysis (NLP Base) ==================================================
    elif choice == 3:  # Text Analisis (NLP Base ) only admin have access
        username, password, role = utils.login()
        if role == "admin":
            while True:
                print(Fore.BLUE + pyfiglet.figlet_format("Text Analysis"))
                print(
                    Fore.BLUE
                    + "************************************************************"
                )
                print(
                    Fore.GREEN
                    + "[1] Count Sentences \n[2] Count Words\n[3] Top Frequent Words\n[4] Custom Tokenizer\n[5] Back\n"
                )
                user_choice = int(input(Fore.YELLOW + "Please select an option: "))
                if user_choice == 1:  # Count Sentences
                    nlp = spacy.load("en_core_web_sm")
                    print(
                        "[1] Count all sentences\n[2] Counting sentences in a specific note "
                    )
                    text_analysis_choice = int(
                        input(Fore.YELLOW + "Please select an option: ")
                    )
                    all_notes_text = ""
                    if text_analysis_choice == 1:
                        for note in utils.return_notes_custom(1):
                            all_notes_text = all_notes_text + note[0]
                        doc = nlp(all_notes_text)
                        all_notes_list = [sent.text for sent in doc.sents]
                        print(
                            f"there are {len(all_notes_list)} sentence on notes was write in notebook app...\n"
                        )
                        print(
                            Fore.BLUE
                            + "[1] To see all sentences (press enter to go back)  "
                        )
                        discuss = input()
                        if int(discuss) == 1:
                            for sentence in all_notes_list:
                                if sentence != all_notes_list[-1]:
                                    print(sentence, end=" , ")
                                else:
                                    print(sentence)
                            input()
                    elif text_analysis_choice == 2:
                        print(
                            Fore.LIGHTYELLOW_EX
                            + "Here are the notes. You should enter the note ID to edit it. 👇👇👇\n"
                        )
                        utils.print_all_notes()
                        user_choice_note_id = int(
                            input(Fore.YELLOW + "Please select an option: ")
                        )
                        user_choice_note = (
                            utils.return_notes_custom(2, user_choice_note_id)
                        )[0][0]
                        nlp = spacy.load("en_core_web_sm")
                        doc = nlp(user_choice_note)
                        user_choice_note_sentences_list = [
                            sent.text for sent in doc.sents
                        ]
                        print(
                            Fore.BLUE
                            + f"there are {len(user_choice_note_sentences_list)} sentence on this note\n"
                        )
                        print(
                            Fore.BLUE
                            + "[1] To see all sentences (press enter to go back)  "
                        )
                        discuss = input()
                        if int(discuss) == 1:
                            for sentence in user_choice_note_sentences_list:
                                if sentence != user_choice_note_sentences_list[-1]:
                                    print(sentence, end=" , ")
                                else:
                                    print(sentence)
                            print("\n")
                            input()
                    else:
                        print(Fore.RED + "invalid choice...")
                        input()
                        continue
                elif user_choice == 2:  # Count Words
                    nlp = spacy.load("en_core_web_sm")
                    print(
                        Fore.BLUE
                        + "[1] Count all words\n[2] Counting words in a specific note "
                    )
                    text_analysis_choice = int(
                        input(Fore.YELLOW + "Please select an option: ")
                    )
                    all_notes_text = ""
                    if text_analysis_choice == 1:  # to see all notes analys
                        text = ""
                        all_text_notes = utils.return_notes_custom(1)
                        for note in all_text_notes:
                            text += note[0]
                        doc = nlp(text)
                        text_words_list = [
                            token.text for token in doc if not token.is_punct
                        ]
                        print(
                            Fore.BLUE
                            + f"\nthere are {len(text_words_list)} words on notes was write in notebook app...\n"
                        )
                        print(
                            Fore.BLUE
                            + "[1] To see all sentences (press enter to go back)  "
                        )
                        discuss = input()
                        if int(discuss) == 1:
                            for sentence in text_words_list:
                                if sentence != text_words_list[-1]:
                                    print(sentence, end=" , ")
                                else:
                                    print(sentence)
                            print("\n")
                            input()
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
                        custom_words_list = [
                            token.text for token in doc if not token.is_punct
                        ]
                        print(
                            Fore.BLUE
                            + f"\nthere are {len(custom_words_list)} words on notes was write in notebook app...\n"
                        )
                        print(
                            Fore.BLUE
                            + "[1] To see all sentences (press enter to go back)  "
                        )
                        discuss = input()
                        if int(discuss) == 1:
                            for word in custom_words_list:
                                if word != custom_words_list[-1]:
                                    print(word, end=" , ")
                                else:
                                    print(word)
                            print("\n")
                            input()
                    else:
                        print(Fore.RED + "invalid choice...")
                        input()
                        continue
                elif user_choice == 3:  # Top Frequent Words
                    pass
                elif user_choice == 4:  # Custom Tokenizer
                    pass
                elif user_choice == 5:  # Back
                    print(Fore.GREEN + "Back...")
                    time.sleep(3)
                    break
                else:
                    print(Fore.RED + "invalid choice...")
                    time.sleep(3)
                    continue
        else:
            print(Fore.RED + "Warning : you must be an admin to access this section")
            input()
            continue
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
