# Smart Notes CLI

Smart Notes CLI is a Python command-line application for managing users and notes, performing basic text analysis, and searching note content through an inverted index.

The project was developed as a practical exercise in modular Python programming, SQLite data management, command-line interface design, file handling, logging, and basic information retrieval.

## Key Features

- Command-line interface with colored menus
- User management with Admin, Editor, and Viewer roles
- User creation, editing, deletion, and listing
- Note creation, editing, deletion, and listing
- SQLite database persistence
- Note tagging
- Role-based access to notes and application sections
- Sentence counting
- Word counting
- Frequent-word analysis
- Custom regular-expression token search
- Inverted index generation
- Keyword-based note search
- Search statistics
- Inverted index save and load using Pickle
- ZIP backup creation
- Backup listing and restoration
- Configurable backup directory
- Text report generation
- Application activity and error logging

## Technologies

- Python
- SQLite
- spaCy
- NLTK
- Regular Expressions
- Colorama
- PyFiglet
- Pickle
- ZIP file handling
- Python Logging

## Project Structure

```text
PYTHON_NLP/
├── backups/              # Generated ZIP backup files
├── db/                   # SQLite database files
├── index/                # Saved inverted index files
├── logs/                 # Application logs
├── reports/              # Generated text reports
├── main.py               # CLI entry point and menu handling
├── models.py             # User, note, analysis, search, backup, and report operations
├── utils.py              # Database helpers, validation, authentication, and utilities
├── requirements.txt      # External Python dependencies
└── README.md             # Project documentation
```

Files such as `.idea/`, `__pycache__/`, generated databases, logs, backups, and saved indexes should not be committed to the public repository.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd PYTHON_NLP
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the spaCy English model

```bash
python -m spacy download en_core_web_sm
```

### 5. Download the required NLTK resources

```bash
python -m nltk.downloader punkt punkt_tab
```

### 6. Check the required directories

The following directories must exist before running the current version:

```text
db/
logs/
backups/
index/
reports/
```

## Usage

Run the application from the project root directory:

```bash
python main.py
```

The main menu provides access to the following sections:

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

Enter the number of an option and follow the instructions displayed in the terminal.

## Example CLI Flow

A basic application flow can be:

1. Open `User Management`.
2. Create a user with an Admin, Editor, or Viewer role.
3. Open `Notes Management`.
4. Log in with the created account.
5. Add a note with a subject, content, and tags.
6. Open `Text Analysis` to inspect the note text.
7. Build an inverted index from the stored notes.
8. Search for a keyword.
9. Create a ZIP backup.
10. Generate a text report.

## User Roles

The project supports three user roles:

### Admin

Administrators can manage users, manage all notes, and access the text-analysis section.

### Editor

Editors can edit and delete notes and access supported management sections.

### Viewer

Viewers can create notes and manage their own notes.

> Some access-control rules still need further review and standardization before the project is considered production-ready.

## Notes Management

Each note contains:

- An automatically generated ID
- Username of the note owner
- Subject
- Note content
- Tags

Notes are stored in an SQLite database located inside the `db` directory.

## Text Processing and Search

The project provides basic text-processing and information-retrieval functionality.

Current text-processing features include:

- Sentence segmentation with spaCy
- Word tokenization with spaCy and NLTK
- Frequent-word calculation with `collections.Counter`
- Stop-word and punctuation filtering
- Custom token matching with Regular Expressions

The search engine creates an inverted index that maps normalized words to note IDs. The index is then used to locate notes containing the searched keywords.

The saved index is stored as:

```text
index/inverted_index.pkl
```

This project does not implement:

- Large Language Models
- RAG
- AI agents
- Text generation
- Semantic search
- Embeddings
- A custom-trained Machine Learning model
- An advanced NLP pipeline

Its purpose is to demonstrate basic text processing, keyword search, and information retrieval in Python.

## Backup and Archive

The application can:

- Create ZIP backups
- List available backups
- Restore a selected backup
- Accept a custom backup path

Generated backups are stored in the `backups` directory by default.

Backup files may contain:

- SQLite database
- Saved inverted index
- Log file
- Generated text report

Generated backup files should not be committed to Git.

## Reports and Logs

The application currently supports text report generation.

The text report contains information such as:

- Total number of users
- Total number of notes
- Total word count
- Most frequent words
- Report generation date

The report is stored in:

```text
reports/report.txt
```

Application activities and selected errors are written to:

```text
logs/logs.txt
```

## Security Notes

User passwords are not stored as plain text. The current version hashes passwords before saving them to SQLite.

However, the current password implementation uses SHA-256 without a unique salt. This is suitable only as a learning implementation and should not be considered production-grade password security.

A stronger future implementation should use:

- PBKDF2-HMAC
- Scrypt
- Argon2
- A unique random salt for every password
- Constant-time password comparison

The current version does not provide production-grade encryption for sensitive note content.

## Current Limitations

- The PDF report option is not implemented yet.
- The Custom Tools section is not implemented yet.
- Password hashing currently uses unsalted SHA-256.
- Sensitive-note encryption is not fully implemented.
- The application downloads some NLTK resources from inside the source code.
- The CLI logic is concentrated mainly in `main.py`.
- Database operations and application logic are not fully separated.
- Some broad exception handlers need to be replaced with specific exceptions.
- Some input validation and access-control rules need improvement.
- The application assumes that runtime directories already exist.
- Automated tests have not been added yet.
- Pickle files should only be loaded from trusted sources.
- The project has not yet been prepared for production deployment.

## Running Tests

Automated tests are not available in the current version.

Unit tests will be added for:

- Password hashing
- Input validation
- Tokenization
- Word counting
- Sentence counting
- Frequent-word analysis
- Inverted index generation
- Keyword search
- Database operations

After the test suite is added, it will be executable with:

```bash
python -m pytest
```

## Future Improvements

- Complete PDF report generation
- Complete the Custom Tools section
- Replace SHA-256 password storage with PBKDF2-HMAC and random salts
- Add secure encryption for sensitive notes
- Separate CLI, database, service, and utility layers
- Add automated tests with Pytest
- Improve exception handling
- Use `pathlib` for file paths
- Prevent duplicate keyword-search results
- Add full-text search
- Add a graphical user interface
- Build a REST API with FastAPI or Django REST Framework
- Add PostgreSQL support
- Add Docker support
- Integrate more structured NLP tools where appropriate

These items are planned improvements and are not part of the current completed feature set.

## Screenshots

Screenshots will be added after the CLI output and menu structure are finalized.

Recommended screenshots:

```text
screenshots/main-menu.png
screenshots/user-management.png
screenshots/notes-management.png
screenshots/text-analysis.png
screenshots/search-results.png
screenshots/backup-management.png
screenshots/text-report.png
```

## Project Purpose

This project was created to practice:

- Modular Python programming
- Command-line application development
- SQLite database operations
- Input validation
- User and note management
- File and backup handling
- Logging
- Basic text processing
- Inverted-index construction
- Keyword-based information retrieval

It is a portfolio and learning project, not a production note-management or security system.

## License

This project is intended to be released under the MIT License.
