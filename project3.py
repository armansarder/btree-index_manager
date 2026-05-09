import sys
from index_file import create_index_file, read_header

def main(): 
    if len(sys.argv) < 2:
        print("Missing command line argument")
        return

    command = sys.argv[1]
    if command == "create":
        print("Executing Create command")
    elif command == "insert":
        print("Executing Insert command")
    elif command == "search":

        if len(sys.argv) != 4:
            print("search <index file> <key>")
            return

        filename = sys.argv[2]
        header = read_header(filename)
        if header is not None:
            print(header)
    elif command == "load":
        print("Executing Load command")
    elif command == "print":
        print("Executing Print command")
    elif command == "print":
        print("Executing Print command")
    elif command == "extract":
        print("Executing Extract command")

main()
