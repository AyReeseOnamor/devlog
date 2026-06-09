import argparse
import json
import os
from datetime import datetime
from colorama import init, Fore, Style
init(autoreset = True)

DATA_FILE = os.path.expanduser("~/.devlog.json")

def load():
    if not os.path.exists(DATA_FILE):
        return[]
    with open(DATA_FILE) as f:
        return json.load(f)
    
def save(entries):
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=2)

def cmd_add(args):
    entries = load()
    entry = {
        "id": len(entries) + 1,
        "message": args.message,
        "tag": args.tag,
        "date": datetime.now().strftime("%Y - %m - %d %H:%M")
    }
    entries.append(entry)
    save(entries)
    print(Fore.GREEN + f"✓ Logged #{entry['id']}: {entry['message']}")

def cmd_list(args):
    entries = load()
    if not entries:
        print("No entries yet. Use: python devlog.py add \"your message\"")
        return
    for entry in reversed(entries):
        tag = f" [{entry['tag']}]" if entry['tag'] else ""
        print(Fore.CYAN + f"#{entry['id']} {entry['date']}" + Fore.YELLOW + tag)
        print(Fore.WHITE + f" {entry["message"]}")
        print()

def cmd_search(args):
    entries = load()
    results = [e for e in entries if args.keyword.lower() in e["message"].lower()]
    if not results:
        print(f"No entries found for: {args.keyword}")
        return
    for entry in results:
        tag = f" [{entry['tag']}]" if entry['tag'] else ""
        print(Fore.CYAN + f"#{entry['id']} {entry['date']}" + Fore.YELLOW + tag)
        print(Fore.WHITE + f" {entry['message']}")
        print()

def cmd_delete(args):
    entries = load()
    match = [e for e in entries if e["id"] == args.id]
    if not match:
        print(f"No entry found with id #{args.id}")
        return
    entries = [e for e in entries if e["id"] != args.id]
    for i, e in enumerate(entries):
        e["id"] = i + 1
    save(entries)
    print(Fore.GREEN + f"Deleted #{args.id}: {match[0]['message']}")

def cmd_export(args):
    entries = load()
    if not entries:
        print(Fore.YELLOW + "No entries to export.")
        return
    filename = "devlog_export.md"
    with open(filename, "w") as f:
        f.write("# My Dev Log\n\n")
        for entry in entries:
            tag = f" `{entry['tag']}`" if entry['tag'] else ""
            f.write(f"### #{entry['id']} - {entry['date']}{tag}\n\n")
            f.write(f"{entry['message']}\n\n")
            f.write("---\n\n")

    print(Fore.GREEN + f"✓ Exported {len(entries)} entries to {filename}")

def cmd_stats(args):
    entries = load()
    if not entries:
        print(Fore.YELLOW + "No entries yet.")
        return
    total = len(entries)
    tags = {}
    for entry in entries:
        if entry["tag"]:
            tags[entry["tag"]] = tags.get(entry["tag"], 0) + 1

    print(Fore.CYAN + "\n── devlog stats ──────────────────")
    print(Fore.WHITE + f"  Total entries:  {total}")

    if tags:
        print(Fore.CYAN + "\n Tags:")
        for tag, count in sorted(tags.items(), key = lambda x: x[1], reverse = True):
            bar = "█" * count
            print (Fore.YELLOW + f" {tag:<15}" + Fore.GREEN + f" {bar} {count}")

    from collections import Counter
    dates = [e["date"][:10] for e in entries]
    date_counts = Counter(dates)
    print(Fore.CYAN + "\n  Entries per day:")
    for date, count in sorted(date_counts.items()):
        bar = "█" * count
        print(Fore.WHITE + f"    {date}  " + Fore.GREEN + f"{bar} {count}")

    print(Fore.CYAN + "\n──────────────────────────────────\n")


parser = argparse.ArgumentParser(prog = "devlog", description= "A devlog journal for your terminal")
subparsers = parser.add_subparsers(dest= "command")

add_parser = subparsers.add_parser("add", help = "Add a new entry")
add_parser.add_argument("message", help = "What did you work on?")
add_parser.add_argument("--tag", default = None, help = "Optional tag e.g. --tag bugfix")
add_parser.set_defaults(func = cmd_add)

list_parser = subparsers.add_parser("list", help = "Show recent entries")
list_parser.set_defaults(func = cmd_list)

search_parser = subparsers.add_parser("search", help = "Search entries by keyword")
search_parser.add_argument("keyword", help = "Word to search for")
search_parser.set_defaults(func = cmd_search)

delete_parser = subparsers.add_parser("delete", help = "Delete an entry in id")
delete_parser.add_argument("id", type = int, help = "ID of the entry to delete")
delete_parser.set_defaults(func = cmd_delete)

export_parser = subparsers.add_parser("export", help="Export all entries to a markdown file")
export_parser.set_defaults(func=cmd_export)

stats_parser = subparsers.add_parser("stats", help="Show entry statistics")
stats_parser.set_defaults(func=cmd_stats)

args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()

