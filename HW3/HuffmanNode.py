import heapq
from collections import Counter

import numpy as np


class HuffmanNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(dct_coefficients):
    # Flatten the 3D array of DCT coefficients into a 1D list
    flat_coefficients = dct_coefficients.flatten()

    # Calculate the frequency of each coefficient
    freq_counter = Counter(flat_coefficients)

    # Create a priority queue (min-heap) with nodes for each unique coefficient
    priority_queue = [HuffmanNode(value, freq) for value, freq in freq_counter.items()]
    heapq.heapify(priority_queue)

    # Build the Huffman Tree
    while len(priority_queue) > 1:
        # Extract the two nodes with the lowest frequency
        node1 = heapq.heappop(priority_queue)
        node2 = heapq.heappop(priority_queue)

        # Create a new internal node with these two nodes as children
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2

        # Add the new node back to the priority queue
        heapq.heappush(priority_queue, merged)

    # The remaining node is the root of the Huffman Tree
    return priority_queue[0]


# Function to generate Huffman codes from the Huffman Tree
def generate_huffman_codes(node, prefix='', codebook=None):
    if codebook is None:
        codebook = {}

    if node is not None:
        # If it's a leaf node, add the code to the codebook
        if node.value is not None:
            codebook[node.value] = prefix
        else:
            # Traverse the left and right children
            generate_huffman_codes(node.left, prefix + '0', codebook)
            generate_huffman_codes(node.right, prefix + '1', codebook)

    return codebook


def huffman_encode(dct_coefficients, codebook):
    # Flatten the 3D array of DCT coefficients into a 1D list
    flat_coefficients = dct_coefficients.flatten()

    # Encode the coefficients using the Huffman codebook
    encoded_str = ''.join(codebook[coeff] for coeff in flat_coefficients)

    return encoded_str


def huffman_decode(encoded_str, huffman_tree, shape):
    decoded_coefficients = []
    node = huffman_tree
    for bit in encoded_str:
        if bit == '0':
            node = node.left
        else:
            node = node.right

        if node.left is None and node.right is None:
            # It's a leaf node
            decoded_coefficients.append(node.value)
            node = huffman_tree  # Go back to the root for the next code

    # Convert the decoded coefficients into a 3D array with the given shape
    decoded_array = np.array(decoded_coefficients).reshape(shape)

    return decoded_array
