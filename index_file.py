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

        
