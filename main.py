from collections import Counter, defaultdict
from colorama import init, Fore, Style
import models, utils, pyfiglet, sqlite3, time, spacy, logging
import nltk

nltk.download("punkt_tab")
inverted_index, search_status = defaultdict(list), defaultdict(list)
logging.basicConfig(
    filename="logs/logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
Welcome = "welcome to the Application"
init(autoreset=True)
utils.build_database()
while True:
    # ==========start-of-choice-handling==========
    print(Fore.YELLOW + pyfiglet.figlet_format(Welcome))
    print(
        Fore.GREEN
        + "[1] User Management\n[2] Notes Management\n[3] Text Analysis(only admin)\n[4] Search Engine\n[5] Backup & Archive (admin , editor)\n[6] Reports(only admin)\n[7] Custom Tools\n[0] Exit"
    )
    try:
        choice = int(input(Fore.YELLOW + "Please select an option: " + Style.RESET_ALL))
    except:
        print(Fore.RED + "invalid choice")
        input()
        continue
    # ======================================================= User Management ======================================================
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
        while True:
            try:
                user_choice = int(
                    input(Fore.YELLOW + "Please select an option: " + Style.RESET_ALL)
                )
                if user_choice in [1, 2, 3, 4, 5]:
                    break
                else:
                    print(Fore.RED + "invalid option ...")
                    input()
                    continue
            except ValueError:
                print(Fore.RED + "invalid choice")
                input()
                continue
        if user_choice == 1:  # adding user
            models.add_user()
        elif user_choice == 2:  # edit user(only admin , editor can edit)
            username, password, role = utils.login()
            if role in ["admin", "editor"]:
                models.edit_user(username, password)
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
                    if not deleted_username:
                        print(Fore.RED + "The username can not be empty")
                        input()
                        continue
                    if utils.search_user(deleted_username):
                        models.delete_user(deleted_username, my_username)
                        print(Fore.RED + f"{deleted_username} was deleted ...")
                        input()
                        break
                    else:
                        print(
                            Fore.RED
                            + "wrong username Enter 1 to back or press Enter to continue"
                        )
                        x = input()
                        if int(x) == 1:
                            break
                        else:
                            continue
            else:
                print(Fore.RED + "Do not have access (only admin can delete user) ...")
                input()
                continue
        elif user_choice == 4:  # users list(all roles can see this part)
            models.list_of_all_users()
            utils.build_log(username="user", message="View the list of useres ")
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
        try:
            while True:
                user_choice = int(input(Fore.YELLOW + "Please select an option: "))
                if user_choice in [1, 2, 3, 4, 5]:
                    break
                else:
                    print(Fore.RED + "invalid choice...")
                    input()
                    continue
        except ValueError:
            print(Fore.RED + "invalid choice...")
            input()
            continue
        if user_choice == 1:  # add note
            username, password, role = utils.login()
            models.add_new_notes(username)
            print(Fore.GREEN + "adding note was successful ...")
            utils.build_log(username=username, message="Successfuly Added the note ")
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
                    try:
                        id_choice = int(
                            input("Enter the ID of the note you want to edit: ")
                        )
                    except ValueError:
                        print(Fore.RED + "invalid id...")
                        input()
                        continue
                    if utils.check_id_in_notes(user_id=id_choice):
                        models.edit_note(id_choice)
                        print(Fore.GREEN + "\n Note was edited successfully...")
                        utils.build_log(
                            username=username, message="successfuly edited the  note "
                        )
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
                    try:
                        id_choice = int(
                            input("Enter the ID of the note you want to edit: ")
                        )
                    except ValueError:
                        print(Fore.RED + "invalid id...")
                        input()
                        continue
                    if utils.check_id_in_notes(
                        user_id=id_choice
                    ) and utils.check_note_ownership(
                        note_id=id_choice, username=username
                    ):
                        models.edit_note(id_choice)
                        print(Fore.GREEN + "\n Note was edited successfully...")
                        input()
                        utils.build_log(username=username, message=" ")

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
                    try:
                        id_choice = int(
                            input("Enter the ID of the note you want to Delete: ")
                        )
                    except ValueError:
                        print(Fore.RED + "invalid id ...")
                        input()
                        continue

                    if utils.check_id_in_notes(user_id=id_choice):
                        models.delete_note(id_choice)
                        utils.build_log(
                            username=username, message="successfuly deleted the  note "
                        )
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
                    try:
                        id_choice = int(
                            input("Enter the ID of the note you want to Delete: ")
                        )
                    except ValueError:
                        print(Fore.RED + "invalid id ...")
                        input()
                        continue

                    if utils.check_id_in_notes(
                        user_id=id_choice
                    ) and utils.check_note_ownership(
                        note_id=id_choice, username=username
                    ):
                        models.delete_note(id_choice)
                        print(Fore.RED + "successfuly edited the  note")
                        input()
                        utils.build_log(
                            username=username, message="successfuly edited the  note "
                        )
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
                utils.build_log(username=username, message=" Viewed the note ")
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
                try:
                    user_choice = int(input(Fore.YELLOW + "Please select an option: "))
                except ValueError:
                    print(Fore.RED + "invalid choice...")
                    input()
                    continue

                if user_choice == 1:  # Count Sentences
                    nlp = spacy.load("en_core_web_sm")
                    print(
                        "[1] Count all sentences\n[2] Counting sentences in a specific note "
                    )
                    try:
                        while True:
                            text_analysis_choice = int(
                                input(Fore.YELLOW + "Please select an option: ")
                            )

                            if text_analysis_choice in [1, 2]:
                                break
                            else:
                                print(Fore.RED + "invalid choice...")
                                input()
                                continue
                    except ValueError:
                        print(Fore.RED + "invalid choice...")
                        input()
                        continue

                    all_notes_text = ""
                    if text_analysis_choice == 1:
                        for note in utils.return_notes_custom(1):
                            all_notes_text = all_notes_text + note[0]
                        doc = nlp(all_notes_text)
                        all_notes_list = [sent.text for sent in doc.sents]
                        print(
                            f"there are {len(all_notes_list)} sentence on notes was write in notebook app...\n"
                        )
                        utils.build_log(
                            username=username, message="Viewed number of sentence "
                        )
                        print(
                            Fore.BLUE
                            + "[1] To see all sentences (press enter to go back)  "
                        )
                        discuss = input()
                        if discuss == "1":
                            for sentence in all_notes_list:
                                if sentence != all_notes_list[-1]:
                                    print(sentence, end=" , ")
                                else:
                                    print(sentence)
                            utils.build_log(
                                username=username, message="viewed All notes sentence"
                            )
                            input()
                    elif text_analysis_choice == 2:
                        print(
                            Fore.LIGHTYELLOW_EX
                            + "Here are the notes. You should enter the note ID to view sentences. 👇👇👇\n"
                        )
                        utils.print_all_notes()
                        try:
                            while True:
                                user_choice_note_id = int(
                                    input(Fore.YELLOW + "Please select an option: ")
                                )
                                if utils.check_id_in_notes(user_choice_note_id):
                                    break
                                else:
                                    print(Fore.RED + "invalid ID...")

                        except ValueError:
                            print(Fore.RED + "invalid choice ...")
                            input()
                            continue
                        note_result = utils.return_notes_custom(2, user_choice_note_id)
                        if not note_result:
                            print(Fore.RED + "Note not found...")
                            input()
                            continue
                        user_choice_note = note_result[0][0]
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
                        if discuss == "1":
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
                    try:
                        text_analysis_choice = int(
                            input(Fore.YELLOW + "Please select an option: ")
                        )
                    except ValueError:
                        print(Fore.RED + "invalid choice...")
                        input()
                        continue
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
                        utils.build_log(
                            username=username, message="Viewed number of words "
                        )
                        discuss = input()
                        if discuss == "1":
                            for sentence in text_words_list:
                                if sentence != text_words_list[-1]:
                                    print(sentence, end=" , ")
                                else:
                                    print(sentence)
                            utils.build_log(
                                username=username, message="viewed all noted words  "
                            )
                            print("\n")
                            input()
                    elif text_analysis_choice == 2:  # to see spacific note
                        print(
                            Fore.LIGHTYELLOW_EX
                            + "Here are the notes. You should enter the note ID to view words. 👇👇👇\n"
                        )
                        utils.print_all_notes()
                        try:
                            while True:
                                try:
                                    note_id = int(input(Fore.BLUE + "Enter note id : "))
                                except ValueError:
                                    print(Fore.RED + "invalid id ....")
                                    input()
                                    continue
                                if utils.check_id_in_notes(note_id):
                                    break
                                else:
                                    print(Fore.RED + "invalid ID...")
                                    input()
                                    continue

                        except:
                            print(Fore.RED + "invalid choice...")
                            input()
                            continue
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
                        if discuss == "1":
                            utils.build_log(
                                username=username, message="Viewed all words "
                            )
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
                    models.top_frequent_words()
                    utils.build_log(
                        username=username, message="Viewd all number of words "
                    )
                elif user_choice == 4:  # Custom Tokenizer
                    my_token = input(Fore.YELLOW + "Enter your Tokenizer: ")
                    if not my_token.strip():
                        print(Fore.RED + "Tokenizer cannot be empty...")
                        input()
                        continue
                    print(
                        Fore.BLUE
                        + "\n[1] to check your token in all notes\n[2] to check note with id "
                    )
                    try:
                        tokenize_choice = int(
                            input(Fore.YELLOW + "Please select an option: ")
                        )
                    except ValueError:
                        print(Fore.RED + "Please select a valid option (1 or 2)...")
                        input()
                        continue
                    if tokenize_choice == 1:
                        models.custom_tokenizer(my_token)
                        input()
                    elif tokenize_choice == 2:
                        utils.print_all_notes()
                        try:
                            tokenize_choice_id = int(
                                input(Fore.BLUE + "Please enter note id: ")
                            )
                            if not utils.check_id_in_notes(tokenize_choice_id):
                                print(Fore.RED + "Note not found...")
                                input()
                                continue
                            models.custom_tokenizer(my_token, tokenize_choice_id)
                        except ValueError:
                            print(Fore.RED + "Invalid note ID...")
                            input()
                            continue
                        utils.build_log(
                            username=username, message="Used customize Token "
                        )
                    else:
                        print(Fore.RED + "Please select a valid option (1 or 2)...")
                        input()
                        continue
                elif user_choice == 5:  # Back
                    print(Fore.GREEN + "Back...")
                    time.sleep(3)
                    break
                else:
                    print(Fore.RED + "invalid choice...")
                    input()
                    continue
        else:
            print(Fore.RED + "Warning : you must be an admin to access this section")
            input()
            continue
    # ======================================================= Search Engine ==========================================================
    elif choice == 4:  # Search Engine
        username, password, role = utils.login()
        while True:
            print(Fore.BLUE + pyfiglet.figlet_format("Search Engine"))
            print(
                Fore.BLUE
                + "************************************************************"
            )
            print(
                Fore.GREEN
                + "[1] Build Inverted Index \n[2] Search Keyword \n[3] Show Search Stats\n[4] Save/Load Index\n[5] Back"
            )
            user_choice = input(Fore.BLUE + "Please enter your choice: ")
            if user_choice == "1":  # inverted index
                note_inverted_index = models.build_inverted_index()
                discuss = input(
                    Fore.GREEN + "[1] To see the indexes, press Enter to continue : "
                )
                if discuss == "1":
                    tuple_index = tuple(note_inverted_index.items())
                    print(utils.two_member_tuple_to_dictionary(tuple_index))
                    input(Fore.GREEN + "\n continue...")
                inverted_index = utils.append_dictionary_to_dictionary(
                    inverted_index, note_inverted_index
                )
                utils.build_log(username=username, message="builded a inverted index")
            elif user_choice == "2":  #  Search Keyword

                while True:
                    user_search = input(Fore.GREEN + "What are you looking for? ")
                    if len(user_search) > 3:
                        searched_ids = models.search_keyword(
                            user_search=user_search, inverted_index=inverted_index
                        )
                        if searched_ids:
                            for note_id in searched_ids:
                                utils.print_note_by_id(note_id)
                            utils.append_dictionary_to_dictionary(
                                inverted_index, {user_search: searched_ids}
                            )
                            utils.append_dictionary_to_dictionary(
                                search_status, {user_search: searched_ids}
                            )
                            utils.build_log(
                                username=username, message="searched for a keyword"
                            )
                            input(
                                Fore.GREEN
                                + "Search completed. Press Enter to continue..."
                            )
                            break
                        else:
                            discuss = input(
                                Fore.RED
                                + "Nothing found, press 1 to continue or Enter to go back"
                            )
                            if discuss == "1":
                                continue
                            else:
                                break
                    else:
                        print(Fore.RED + "Please enter at least 3 characters.")
                        input()
                        continue
                utils.build_log(username=username, message="searched")
            elif user_choice == "3":  # Show Search Stats
                models.show_search_stats(search_status)
                utils.build_log(username=username, message="builded a inverted index")
                continue
            elif user_choice == "4":  # Save/Load Index
                print(Fore.GREEN + "[1] Save index\n[2] Load index \n[3] Back")
                while True:
                    sub_choice = input()
                    if sub_choice == "1":
                        if not inverted_index:
                            print(Fore.RED + "Saved an index")
                            input()
                            break
                        models.save_index(inverted_index)
                        utils.build_log(username=username, message="saved a index")
                        break
                    elif sub_choice == "2":
                        try:
                            inverted_index = models.load_index()
                            if inverted_index is None:
                                print(Fore.RED + "No saved index found.")
                                input()
                                break
                        except:
                            print(Fore.RED + "No saved index found.")
                            input()
                            break
                        print(Fore.GREEN + "Index loaded successfully.")
                        utils.build_log(username=username, message="loaded a index")
                        input()
                        break
                    elif sub_choice == "3":
                        break
                    else:
                        print(Fore.RED + "Invalid choice...")
                        input()
                        continue

            elif user_choice == "5":  # Back
                print(Fore.GREEN + "Back...")
                time.sleep(2)
                break
            else:
                print(Fore.RED + "Invalid choice...")
                input()
                continue

    # ======================================================= Backup & Archive ==========================================================

    elif choice == 5:  # Backup & Archive
        username, password, role = utils.login()
        while True:
            print(Fore.BLUE + pyfiglet.figlet_format("Backup & Archive"))
            print(
                Fore.BLUE
                + "************************************************************"
            )
            print(
                Fore.GREEN
                + "[1] Create Backup \n[2] Restore Backup \n[3] List Backups \n[4] Configure Backup Path \n[5] Back"
            )
            user_choice = input(Fore.BLUE + "Please enter your choice: ")
            if user_choice == "1":
                models.create_backup()
            elif user_choice == "2":
                models.restore_backup()
            elif user_choice == "3":
                models.list_backups()
            elif user_choice == "4":
                models.configure_backup_path()
            elif user_choice == "5":
                break
            else:
                print(Fore.RED + "Invalid choice...")
                input()
                continue
    # =========================================================  Reports  ==========================================================
    elif choice == 6:
        username, password, role = utils.login()
        if role in ["admin", "editor"]:
            while True:
                print(Fore.BLUE + pyfiglet.figlet_format("Reports"))
                print(
                    Fore.BLUE
                    + "************************************************************"
                )
                print(
                    Fore.GREEN
                    + "[1] Generate Text Report \n[2] Generate PDF Report \n[3] Show Logs \n[4] Back"
                )
                user_choice = input(Fore.BLUE + "Please enter your choice: ")
                if user_choice == "1":
                    models.generate_text_report()
                elif user_choice == "2":
                    models.generate_pdf_report()
                elif user_choice == "3":
                    models.show_logs()
                elif user_choice == "4":
                    break
                else:
                    print(Fore.RED + "Invalid choice...")
                    input()
                    continue
        else:
            print(Fore.RED + "Access denied.")
            input()
            continue
    # ======================================================= Custom Tools ==========================================================
    elif choice == 7:
        print(Fore.GREEN + "Coming soon...")
        input()
        continue
    elif choice == 0:
        print(Fore.RED + "Goodbye...")
        input()
        break
    else:
        utils.InvalidChoice()
