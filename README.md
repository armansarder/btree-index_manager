# B Tree Indexing Manager

The project implements an interactive program that manages files using a B Tree data structure. The program creates files and stores them with pairs of data. 

# Structure

project3.py is the main file. This file sets up the contact between user and the rest of the program. 

btree.py contains the calculations for the B Tree. It handles the insertion, search, traversal, and splitting nodes. 

node.py holds the structure of the B Tree nodes. Handles the conversion of node data to and from the 512 byte format in the file.

index_file.py hanfles low level index file operations for creating indexes, and read/write operations for headers and node blocks.

# B Tree Details 

- Min degree = 10
- Max keys per node = 19
- Max child nodes per node = 20

When a node becomes full, the program performs splitting operations to promote the median key to the parent node.

Use commands like:

python3 project3.py create test.idx
python3 project3.py insert test.idx 1 10
python3 project3.py search test.idx 1
python3 project3.py print test.idx