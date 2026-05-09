import csv
import os
import sys

from index_file import create_index_file
from btree import insert, search, get_all_pairs

def handle_create():
    if len(sys.argv) != 3:
        print("Usage: python3 project3.py create <index file>")
        return

    filename = sys.argv[2]
    create_index_file(filename)

def handle_insert():
    if len(sys.argv) != 5:
        print("Usage: python3 project3.py insert <index file> <key> <value>")
        return

    filename = sys.argv[2]

    try:
        key = int(sys.argv[3])
        value = int(sys.argv[4])
    except ValueError:
        print("Error: key and value must be integers")
        return

    insert(filename, key, value)

def handle_search():
    if len(sys.argv) != 4:
        print("Usage: python3 project3.py search <index file> <key>")
        return

    filename = sys.argv[2]

    try:
        key = int(sys.argv[3])
    except ValueError:
        print("Error: key must be an integer")
        return

    value = search(filename, key)

    if value is None:
        print("Error: key not found")
    else:
        print(f"{key},{value}")

def handle_load():
    if len(sys.argv) != 4:
        print("Usage: python3 project3.py load <index file> <csv file>")
        return

    index_filename = sys.argv[2]
    csv_filename = sys.argv[3]

    if not os.path.exists(csv_filename):
        print("Error: csv file does not exist")
        return

    with open(csv_filename, "r", newline="") as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            if len(row) != 2:
                print("Error: invalid csv row")
                return

            try:
                key = int(row[0])
                value = int(row[1])
            except ValueError:
                print("Error: csv keys and values must be integers")
                return

            insert(index_filename, key, value)

def handle_print():
    if len(sys.argv) != 3:
        print("Usage: python3 project3.py print <index file>")
        return

    filename = sys.argv[2]
    pairs = get_all_pairs(filename)

    for key, value in pairs:
        print(f"{key},{value}")

def handle_extract():
    if len(sys.argv) != 4:
        print("Usage: python3 project3.py extract <index file> <output file>")
        return

    index_filename = sys.argv[2]
    output_filename = sys.argv[3]

    if os.path.exists(output_filename):
        print("Error: output file already exists")
        return

    pairs = get_all_pairs(index_filename)

    with open(output_filename, "w", newline="") as output_file:
        writer = csv.writer(output_file)

        for key, value in pairs:
            writer.writerow([key, value])

def main():
    if len(sys.argv) < 2:
        print("Error: missing command")
        return

    command = sys.argv[1]

    if command == "create":
        handle_create()
    elif command == "insert":
        handle_insert()
    elif command == "search":
        handle_search()
    elif command == "load":
        handle_load()
    elif command == "print":
        handle_print()
    elif command == "extract":
        handle_extract()
    else:
        print("Error: unknown command")

main()
