# Import dependencies
import numpy as np
import os
from keras.utils import load_img, img_to_array
import matplotlib.pyplot as plt 
import tensorflow as tf

from generator_model import define_generator


# Set up path
VAL_IMAGES_DIRPATH = os.path.join("maps", "val")
CHECKPOINT_FILEPATH = "generator_checkpoint\checkpoint.ckpt"


# Utilities for Inference
def get_test_sample(dirpath, img_size=(256, 512)):
    # Get file path
    fname = np.random.choice(os.listdir(dirpath))
    fpath = os.path.join(dirpath, fname)

    # Load the image
    img = load_img(path=fpath, target_size=img_size)
    img_arr = img_to_array(img) # img_arr.dtype == 'float32'
    src, tar = img_arr[:, :256, :], img_arr[:, 256:, :] # Segment the image into source and target image
    
    # Preprocess the image
    src = (src / 127.5) - 1
    tar = (tar / 127.5) - 1
    
    return src, tar


def plot_image(src_img, gen_img, tar_img):
    images = np.array([src_img, gen_img, tar_img])
    images = (images[:] + 1) * 127.5 # Rescale the images
    images = images.astype('uint8')
    
    titles = ["Source Image", "Generated Image", "Image Expected"]
    
    # Plot the images
    plt.figure(figsize=(10, 7))
    for i in range(len(images)):
        plt.subplot(1, 3, i+1)
        plt.imshow(images[i])
        plt.title(titles[i])
        plt.axis(False)
    plt.show()


# Get the generator (without weights)
generator = define_generator()
# Load in the checkpoint
generator.load_weights(CHECKPOINT_FILEPATH)


# Get the source and target image
src, tar = get_test_sample(VAL_IMAGES_DIRPATH)

# Get the generated (fake) image
gen_img = np.squeeze(generator.predict(np.expand_dims(src, axis=0), verbose=0), axis=0)

# Plot the source, generated and target image
plot_image(src, gen_img, tar)
