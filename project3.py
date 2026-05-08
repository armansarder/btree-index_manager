import sys

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
        print("Executing Search command")
    elif command == "load":
        print("Executing Load command")
    elif command == "print":
        print("Executing Print command")
    elif command == "print":
        print("Executing Print command")
    elif command == "extract":
        print("Executing Extract command")

main()
