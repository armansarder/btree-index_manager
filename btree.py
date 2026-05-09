from node import Node
from index_file import read_header, write_header, read_node, write_node

MIN_DEGREE = 10

def search(filename, key):
    header = read_header(filename)

    if header is None:
        return None

    root_id = header["root_id"]

    if root_id == 0:
        return None

    return search_node(filename, root_id, key)

def search_node(filename, block_id, key):
    node = read_node(filename, block_id)

    if node is None:
        return None

    index = 0

    while index < node.num_keys and key > node.keys[index]:
        index += 1

    if index < node.num_keys and key == node.keys[index]:
        return node.values[index]

    if node.is_leaf():
        return None

    child_id = node.children[index]

    if child_id == 0:
        return None

    return search_node(filename, child_id, key)

def insert(filename, key, value):
    header = read_header(filename)

    if header is None:
        return

    root_id = header["root_id"]
    next_block_id = header["next_block_id"]

    if root_id == 0:
        root = Node(block_id=next_block_id, parent_id=0, num_keys=1)
        root.keys[0] = key
        root.values[0] = value

        write_node(filename, root)
        write_header(filename, root.block_id, next_block_id + 1)
        return

    root = read_node(filename, root_id)

    if root is None:
        return

    if search(filename, key) is not None:
        print("Error: key already exists")
        return

    if root.is_full():
        new_root = Node(block_id=next_block_id, parent_id=0, num_keys=0)
        new_root.children[0] = root.block_id
        root.parent_id = new_root.block_id

        write_node(filename, root)
        write_node(filename, new_root)
        write_header(filename, new_root.block_id, next_block_id + 1)

        split_child(filename, new_root.block_id, 0)
        insert_non_full(filename, new_root.block_id, key, value)
    else:
        insert_non_full(filename, root.block_id, key, value)

def insert_non_full(filename, block_id, key, value):
    node = read_node(filename, block_id)

    if node is None:
        return

    index = node.num_keys - 1

    if node.is_leaf():
        while index >= 0 and key < node.keys[index]:
            node.keys[index + 1] = node.keys[index]
            node.values[index + 1] = node.values[index]
            index -= 1

        node.keys[index + 1] = key
        node.values[index + 1] = value
        node.num_keys += 1

        write_node(filename, node)
        return

    while index >= 0 and key < node.keys[index]:
        index -= 1

    index += 1
    child_id = node.children[index]
    child = read_node(filename, child_id)

    if child is None:
        return

    if child.is_full():
        split_child(filename, node.block_id, index)
        node = read_node(filename, node.block_id)

        if key > node.keys[index]:
            index += 1

    insert_non_full(filename, node.children[index], key, value)

def split_child(filename, parent_block_id, child_index):
    header = read_header(filename)

    if header is None:
        return

    parent = read_node(filename, parent_block_id)
    child = read_node(filename, parent.children[child_index])

    if parent is None or child is None:
        return

    new_child = Node(block_id=header["next_block_id"], parent_id=parent.block_id, num_keys=MIN_DEGREE - 1)

    for j in range(MIN_DEGREE - 1):
        new_child.keys[j] = child.keys[j + MIN_DEGREE]
        new_child.values[j] = child.values[j + MIN_DEGREE]

    if not child.is_leaf():
        for j in range(MIN_DEGREE):
            new_child.children[j] = child.children[j + MIN_DEGREE]

            moved_child = read_node(filename, new_child.children[j])
            if moved_child is not None:
                moved_child.parent_id = new_child.block_id
                write_node(filename, moved_child)

    child.num_keys = MIN_DEGREE - 1

    for j in range(parent.num_keys, child_index, -1):
        parent.children[j + 1] = parent.children[j]

    parent.children[child_index + 1] = new_child.block_id

    for j in range(parent.num_keys - 1, child_index - 1, -1):
        parent.keys[j + 1] = parent.keys[j]
        parent.values[j + 1] = parent.values[j]

    parent.keys[child_index] = child.keys[MIN_DEGREE - 1]
    parent.values[child_index] = child.values[MIN_DEGREE - 1]
    parent.num_keys += 1

    write_node(filename, child)
    write_node(filename, new_child)
    write_node(filename, parent)
    write_header(filename, header["root_id"], header["next_block_id"] + 1)

def get_all_pairs(filename):
    header = read_header(filename)

    if header is None:
        return []

    root_id = header["root_id"]

    if root_id == 0:
        return []

    pairs = []
    traverse_node(filename, root_id, pairs)
    return pairs

def traverse_node(filename, block_id, pairs):
    node = read_node(filename, block_id)

    if node is None:
        return

    for i in range(node.num_keys):
        if node.children[i] != 0:
            traverse_node(filename, node.children[i], pairs)

        pairs.append((node.keys[i], node.values[i]))    

    if node.children[node.num_keys] != 0:
        traverse_node(filename, node.children[node.num_keys], pairs)