# Smart Notes CLI

Smart Notes CLI is a terminal-based note management application developed with Python and SQLite.

The application provides role-based user management, note CRUD operations, tagging, basic text analysis, keyword search through an inverted index, ZIP backups, text reports, and activity logging.

This project was created as a portfolio and learning project to practice Python programming, CLI development, SQLite database operations, file handling, input validation, basic text processing, and information retrieval.

> **Project status:** Active development  
> **Database:** SQLite  
> **Interface:** Command Line Interface

---

## Features

### User Management

- Create new users
- Edit existing users
- Delete users
- Display registered users
- Authenticate users before protected operations
- Assign one of three roles:
  - `Admin`
  - `Editor`
  - `Viewer`

### Notes Management

- Create notes
- Edit notes
- Delete notes
- Display stored notes
- Associate notes with their owners
- Add multiple tags to each note
- Store notes permanently in SQLite
- Restrict Viewer users to their own notes
- Allow Admin and Editor users to manage all notes

### Basic Text Analysis

- Count sentences
- Count words
- Display frequent words
- Remove punctuation and common stop words from frequency results
- Analyze all notes or a selected note
- Search for custom tokens with Regular Expressions

### Search Engine

- Build an inverted index from note titles and contents
- Map normalized words to matching note IDs
- Perform keyword-based searches
- Display matching notes
- Display search statistics
- Save the inverted index with Pickle
- Load a previously saved inverted index

### Backup and Archive

- Create ZIP backups
- Include available database, index, log, and report files
- List existing backup files
- Restore a selected backup
- Validate backup selections
- Create backup directories when necessary

### Reports and Logging

- Generate a text report
- Display:
  - Total users
  - Total notes
  - Total words
  - Top frequent words
  - Report generation time
- Record important activities and errors
- Display application logs from the CLI

### CLI

- Numbered terminal menus
- Colored output with Colorama
- ASCII headings with PyFiglet
- Input validation for common invalid values
- Back and Exit options
- Repeated menu execution through controlled loops

---

## Technologies

### External Libraries

- Python
- Colorama
- PyFiglet
- spaCy
- NLTK

### Python Standard Library

- `sqlite3`
- `hashlib`
- `re`
- `json`
- `collections.Counter`
- `collections.defaultdict`
- `pickle`
- `logging`
- `argparse`
- `zipfile`
- `shutil`
- `os`
- `datetime`
- `multiprocessing`

---

## Project Structure

```text
PYTHON_NLP/
├── backups/
│   └── .gitkeep
├── db/
│   └── .gitkeep
├── index/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
├── reports/
│   └── .gitkeep
├── main.py
├── models.py
├── utils.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Main Files

| File               | Responsibility                                                            |
| ------------------ | ------------------------------------------------------------------------- |
| `main.py`          | Application entry point, CLI menus, navigation, and access checks         |
| `models.py`        | User, note, text-analysis, search, backup, and report operations          |
| `utils.py`         | Database initialization, authentication, validation, and shared utilities |
| `requirements.txt` | External Python dependencies                                              |
| `.gitignore`       | Excludes generated, private, and development files                        |

### Runtime Directories

| Directory  | Purpose                    |
| ---------- | -------------------------- |
| `db/`      | SQLite database files      |
| `logs/`    | Application log files      |
| `backups/` | Generated ZIP backup files |
| `index/`   | Saved inverted-index files |
| `reports/` | Generated text reports     |

Generated files inside these directories are excluded from Git.

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

Replace `<repository-url>` and `<repository-directory>` with the actual repository information.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

#### Linux or macOS

```bash
source .venv/bin/activate
```

### 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 5. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Install the spaCy English pipeline

```bash
python -m spacy download en_core_web_sm
```

### 7. Install the required NLTK data

```bash
python -m nltk.downloader punkt punkt_tab
```

---

## Running the Application

Run the following command from the project root:

```bash
python main.py
```

The application creates the SQLite tables when it starts for the first time.

The runtime directories must exist:

```text
db/
logs/
backups/
index/
reports/
```

These directories are included in the repository through `.gitkeep` files.

---

## Main Menu

```text
[1] User Management
[2] Notes Management
[3] Text Analysis
[4] Search Engine
[5] Backup & Archive
[6] Reports
[7] Custom Tools
[0] Exit
```

---

## Example Usage Flow

A simple demonstration flow is:

1. Run the program.
2. Open `User Management`.
3. Create a user with an Admin role.
4. Open `Notes Management`.
5. Log in with the created account.
6. Create several notes with different tags.
7. Open `Text Analysis`.
8. Count words and sentences.
9. Display the most frequent words.
10. Open `Search Engine`.
11. Build the inverted index.
12. Search for a keyword.
13. Save the generated index.
14. Generate a text report.
15. Create a ZIP backup.

---

## User Roles and Permissions

| Operation            | Admin | Editor | Viewer |
| -------------------- | :---: | :----: | :----: |
| Create a note        |  Yes  |  Yes   |  Yes   |
| View own notes       |  Yes  |  Yes   |  Yes   |
| Edit own notes       |  Yes  |  Yes   |  Yes   |
| Delete own notes     |  Yes  |  Yes   |  Yes   |
| View all notes       |  Yes  |  Yes   |   No   |
| Edit all notes       |  Yes  |  Yes   |   No   |
| Delete all notes     |  Yes  |  Yes   |   No   |
| Edit users           |  Yes  |  Yes   |   No   |
| Delete users         |  Yes  |   No   |   No   |
| Access text analysis |  Yes  |   No   |   No   |
| Access reports       |  Yes  |  Yes   |   No   |

Some access-control rules are still being reviewed and will be standardized in future versions.

---

## Database

The project uses SQLite through Python's built-in `sqlite3` module.

The application automatically creates the following tables:

### Users Table

```text
USERS
├── username
├── password
└── role
```

### Notes Table

```text
NOTES
├── id
├── username
├── subject
├── note
└── tags
```

Parameterized SQL queries are used for the main database operations.

The generated database file is stored at:

```text
db/Notes.db
```

The database file is excluded from Git.

---

## Text Processing

The project provides introductory text-processing functionality using spaCy, NLTK, and Regular Expressions.

Current operations include:

- Sentence segmentation
- Word tokenization
- Punctuation filtering
- Stop-word filtering
- Word-frequency calculation
- Custom Regular Expression token matching
- Text processing for all notes or a selected note

This project does not implement:

- Machine Learning model training
- Large Language Models
- Retrieval-Augmented Generation
- AI agents
- Embeddings
- Semantic search
- Text generation
- Advanced NLP pipelines

The current text-processing functionality is intended for learning and basic analysis.

---

## Inverted Index and Keyword Search

The application builds an inverted index with a structure similar to:

```python
{
    "python": [1, 3, 8],
    "sqlite": [2, 3],
    "search": [1, 5]
}
```

Each word maps to the IDs of notes containing that word.

The search process includes:

1. Reading note subjects and contents
2. Tokenizing the text
3. Normalizing tokens
4. Associating tokens with note IDs
5. Searching the index for matching keywords
6. Displaying the matching notes

The generated index can be stored at:

```text
index/inverted_index.pkl
```

The search system is based on exact normalized keywords. It does not provide semantic search, ranking, fuzzy matching, or embeddings.

> Pickle files must only be loaded from trusted sources.

---

## Backup and Restore

The backup system creates ZIP archives containing available generated files such as:

```text
db/Notes.db
index/inverted_index.pkl
logs/logs.txt
reports/report.txt
```

Backups are stored in:

```text
backups/
```

The application can:

- Create backups
- List backups
- Select a backup
- Restore supported files
- Recreate destination directories when necessary

Backup ZIP files are excluded from Git.

---

## Reports

The current version supports text-report generation.

The report includes:

- Generation date and time
- Total number of users
- Total number of notes
- Total word count
- Five frequent words

The generated report is stored at:

```text
reports/report.txt
```

PDF report generation is present in the CLI but has not been implemented yet.

---

## Logging

Important application operations and selected errors are recorded in:

```text
logs/logs.txt
```

The log file can also be displayed from the Reports menu.

Generated logs are excluded from Git.

Passwords should never be written to the log file.

---

## Security Notes

User passwords are not stored as plain text. The current implementation hashes passwords with SHA-256 before storing them in SQLite.

However, SHA-256 without a unique salt is not considered suitable for production password storage.

A production-ready version should use a dedicated password-hashing approach such as:

- PBKDF2-HMAC
- Scrypt
- Argon2
- Unique random salts
- Constant-time comparisons

The current version does not provide secure encryption for sensitive note contents.

This project should therefore be treated as an educational and portfolio application, not a production security system.

---

## Current Limitations

- PDF report generation is not implemented yet.
- The Custom Tools section is not implemented yet.
- Password hashing currently uses unsalted SHA-256.
- Sensitive-note encryption is not implemented.
- Automated tests have not been added yet.
- Some access rules still need standardization.
- Some CLI and application logic are tightly coupled.
- Some broad exception handlers should be replaced with specific exceptions.
- The backup path configuration is not yet persisted globally.
- NLTK resources are downloaded from application code in the current version.
- The search engine performs exact keyword matching only.
- Pickle files must not be loaded from untrusted sources.

---

## Planned Improvements

- Replace SHA-256 with PBKDF2-HMAC and random salts
- Add automated tests with Pytest
- Complete PDF report generation
- Complete the Custom Tools section
- Add secure sensitive-note encryption
- Separate CLI, database, and business logic more clearly
- Replace broad exception handlers
- Use `pathlib` for cross-platform paths
- Improve role-based access control
- Prevent duplicate search results
- Add result ranking
- Add fuzzy search
- Add SQLite full-text search
- Add a REST API with Django REST Framework or FastAPI
- Add a graphical interface
- Add Docker support
- Add PostgreSQL support

These features are planned improvements and are not presented as completed features.

---

## Troubleshooting

### spaCy model not found

Error:

```text
OSError: [E050] Can't find model 'en_core_web_sm'
```

Install the English pipeline inside the active virtual environment:

```bash
python -m spacy download en_core_web_sm
```

Validate the installation:

```bash
python -m spacy validate
```

### spaCy is not installed

Error:

```text
ModuleNotFoundError: No module named 'spacy'
```

Run:

```bash
python -m pip install -r requirements.txt
```

Make sure the `.venv` interpreter is selected in the editor.

### NLTK resource not found

Run:

```bash
python -m nltk.downloader punkt punkt_tab
```

### Missing runtime directory

Make sure these directories exist:

```text
db/
logs/
backups/
index/
reports/
```

---

## Testing

Automated tests have not been added to the current version.

The planned test suite will cover:

- Username validation
- Password validation and hashing
- Role validation
- Note validation
- Sentence counting
- Word tokenization
- Frequent-word calculation
- Inverted-index construction
- Keyword search
- Database operations
- Access-control rules
- Backup and restore behavior

After tests are added, they will be executable with:

```bash
python -m pytest
```

---

## Screenshots

Recommended screenshots for the repository:

```text
screenshots/01-main-menu.png
screenshots/02-user-management.png
screenshots/03-notes-management.png
screenshots/04-note-list.png
screenshots/05-text-analysis.png
screenshots/06-inverted-index.png
screenshots/07-keyword-search.png
screenshots/08-backup-created.png
screenshots/09-text-report.png
```

Screenshots should use fictional users and notes. Do not display real passwords, personal information, database records, or sensitive data.

---

## Demo Data

Safe demonstration data can use:

```text
Username: demo_admin
Role: admin

Notes:
1. Python CLI Development
2. SQLite Database Practice
3. Inverted Index Search
```

Do not commit the generated database after recording the demonstration.

---

## Project Purpose

Smart Notes CLI demonstrates practical experience with:

- Python application development
- CLI design
- SQLite data persistence
- User authentication
- Role-based permissions
- CRUD operations
- Input validation
- File management
- Backup and restore
- Logging
- Basic text processing
- Inverted-index construction
- Keyword-based information retrieval

---

## License

No open-source license has been added to the repository yet.
