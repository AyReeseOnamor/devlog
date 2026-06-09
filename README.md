# devlog

A command-line journal for developers. Log what you worked on, search past entries, and track your progress — all from the terminal.

![Python](https://img.shields.io/badge/Python-3.13-blue) ![License](https://img.shields.io/badge/license-MIT-green)

---

## Demo

```
$ python devlog.py add "Fixed the login bug" --tag bugfix
✓ Logged #1: Fixed the login bug

$ python devlog.py list
#1 2026-06-09 12:00  [bugfix]
   Fixed the login bug
```

---

## Installation

1. Clone the repo
   ```
   git clone https://github.com/AyReeseOnamor/devlog.git
   cd devlog
   ```

2. Install the one dependency
   ```
   pip install colorama
   ```

3. Run it
   ```
   python devlog.py --help
   ```

---

## Commands

| Command                              | Description                  |
|--------------------------------------|------------------------------|
| `python devlog.py add "message"`     | Add a new entry              |
| `python devlog.py add "msg" --tag x` | Add an entry with a tag      |
| `python devlog.py list`              | Show all entries             |
| `python devlog.py search "keyword"`  | Search entries by keyword    |
| `python devlog.py delete <id>`       | Delete an entry by id        |

---

## What I learned building this

- How CLI argument parsing works using Python's `argparse` module
- Reading and writing persistent data with JSON file storage
- List filtering patterns — finding and removing items from lists
- Terminal output formatting with `colorama`
- How to structure a Python project from scratch

---

## Built with

- Python 3 — standard library only (`argparse`, `json`, `os`, `datetime`)
- [colorama](https://pypi.org/project/colorama/) — for colored terminal output

---

## Author

Iris Romano — [github.com/AyReeseOname](https://github.com/AyReeseOnamor)