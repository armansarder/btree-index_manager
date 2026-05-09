import os 

BLOCK_SIZE = 512
Magic_Number = b"4348PRJ3"

def create_index_file(filename):

    if os.path.exists(filename):
        print(f"File {filename} already exists.")
        return

    with open(filename, "wb") as f:
        f.write(Magic_Number)

        f.write((0).to_bytes(8,"big"))

        f.write((1).to_bytes(8, "big"))

        remaining_bytes = BLOCK_SIZE - 24
        f.write(b'\x00' * remaining_bytes)

    print(f"Index file {filename} created successfully.")

def read_header(filename):
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return None
    
    with open(filename, "rb") as f:

        magic_number = f.read(8)

        if magic_number != Magic_Number:
            print("Invalid index file.")
            return None
        
        root_id = int.from_bytes(f.read(8), "big")
        next_block_id = int.from_bytes(f.read(8), "big")

    header = {
        "root_id": root_id,
        "next_block_id": next_block_id
    }

    return header
