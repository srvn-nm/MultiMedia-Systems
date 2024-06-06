import matplotlib.pyplot as plt


def visualize_dct_coefficients(dct_coefficients):
    # Visualize the DCT coefficients as an image
    fig, axes = plt.subplots(1, len(dct_coefficients), figsize=(15, 5))
    for i, coef in enumerate(dct_coefficients):
        ax = axes[i]
        ax.imshow(coef, cmap='gray')
        ax.set_title(f'Channel {i}')
        ax.axis('off')
    plt.show()
