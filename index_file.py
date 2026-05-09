import os

from node import Node, BLOCK_SIZE

MAGIC_NUMBER = b"4348PRJ3"


def create_index_file(filename):
    if os.path.exists(filename):
        print(f"File {filename} already exists.")
        return

    with open(filename, "wb") as file:
        file.write(MAGIC_NUMBER)
        file.write((0).to_bytes(8, "big"))
        file.write((1).to_bytes(8, "big"))

        remaining_bytes = BLOCK_SIZE - 24
        file.write(b"\x00" * remaining_bytes)

    print(f"Index file {filename} created successfully.")


def read_header(filename):
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return None

    with open(filename, "rb") as file:
        magic_number = file.read(8)

        if magic_number != MAGIC_NUMBER:
            print("Invalid index file.")
            return None

        root_id = int.from_bytes(file.read(8), "big")
        next_block_id = int.from_bytes(file.read(8), "big")

    header = {
        "root_id": root_id,
        "next_block_id": next_block_id
    }

    return header


def write_header(filename, root_id, next_block_id):
    with open(filename, "r+b") as file:
        file.seek(0)

        file.write(MAGIC_NUMBER)
        file.write(root_id.to_bytes(8, "big"))
        file.write(next_block_id.to_bytes(8, "big"))

        remaining_bytes = BLOCK_SIZE - 24
        file.write(b"\x00" * remaining_bytes)


def write_node(filename, node):
    with open(filename, "r+b") as file:
        file.seek(node.block_id * BLOCK_SIZE)
        file.write(node.to_bytes())


def read_node(filename, block_id):
    with open(filename, "rb") as file:
        file.seek(block_id * BLOCK_SIZE)
        data = file.read(BLOCK_SIZE)

    if len(data) != BLOCK_SIZE:
        print("Error: could not read node block")
        return None

    return Node.from_bytes(data)
