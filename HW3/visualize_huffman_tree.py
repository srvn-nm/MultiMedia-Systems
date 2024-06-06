from matplotlib import pyplot as plt


def visualize_huffman_tree(huffman_tree):
    def plot_node(node, x, y, dx, ax, tree_depth):
        if node:
            ax.text(x, y, str(node.value) if node.value is not None else 'N/A', ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='black'))
            if node.left:
                ax.plot([x, x - dx], [y - 1, y - 2], 'k-')
                plot_node(node.left, x - dx, y - 2, dx / 2, ax, tree_depth - 1)
            if node.right:
                ax.plot([x, x + dx], [y - 1, y - 2], 'k-')
                plot_node(node.right, x + dx, y - 2, dx / 2, ax, tree_depth - 1)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')
    depth = huffman_tree.freq.bit_length()
    plot_node(huffman_tree, 0, 0, 2 ** (depth - 1), ax, depth)
    plt.show()
