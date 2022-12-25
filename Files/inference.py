# Import dependencies
import numpy as np
import os
from keras.utils import load_img, img_to_array


VAL_IMAGES_DIRPATH = "/content/data/maps/val"


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
    images = np.vstack([src_img, gen_img, tar_img])
    images = (images + 1) * 127.5 # Rescale the images
    
    titles = ["Source Image", "Generated Image", "Image Expected"]
    
    # Plot the images
    for i in range(len(images)):
        plt.subplot(1, 3, i+1)
        plt.imshow(images[i])
        plt.title(titles[i])
        plt.axis(False)
    plt.show()


# Load the test image
src, tar = get_test_sample(VAL_IMAGES_DIRPATH)

# Get the generated image
gen = model.predict(np.expand_dims(src, axis=0))

# Plot
plot_image(src, gen, tar)