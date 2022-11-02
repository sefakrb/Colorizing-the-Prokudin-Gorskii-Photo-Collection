# library imports
import array as arr
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import sys

# normalized cross-correlation algorithm


def ncc(mainImage, searchImage):
    mainImage = mainImage-mainImage.mean(axis=0)
    searchImage = searchImage-searchImage.mean(axis=0)
    return np.sum(((mainImage/np.sqrt(np.sum(np.square(mainImage)))) * (searchImage/np.sqrt(np.sum(np.square(searchImage))))))

# align function for iterating all indexes of image and make control of matches


def align(mainImage, searchImage, t):
    min_limit = -1
    value = np.linspace(-t, t, 2*t, dtype=int)
    for i in value:
        for j in value:
            difference = ncc(mainImage, np.roll(searchImage, [i, j], axis=(0, 1)))
            if difference > min_limit:
                min_limit = difference
                output = [i, j]
    return output

# read image and save as numpy array


def readImage(filename):
    imageName = args[1] + "/" + filename
    image = Image.open(imageName)
    image = np.asarray(image)
    print(image.shape)
    plt.imshow(image)
    cleanImage(image)

# clean borders


def cleanImage(image):
    imageWidth, imageHeight = image.shape
    print(imageWidth, imageHeight)
    image = image[int(imageWidth*0.01):int(imageWidth-imageWidth*0.02),
                  int(imageHeight*0.05):int(imageHeight-imageHeight*0.05)]
    imageWidth, imageHeight = image.shape
    print(imageWidth, imageHeight)
    plt.imshow(image)
    divideImage(image)

# divide 3 equalas part and distribute to the 3 channels


def divideImage(image):
    imageWidth, imageHeight = image.shape
    height = int(imageWidth/3)

    blueChannel = image[0:height, :]
    greenChannel = image[height:2*height, :]
    redChannel = image[2*height:3*height, :]

    plt.figure()
    plt.imshow(blueChannel)

    plt.figure()
    plt.imshow(greenChannel)

    plt.figure()
    plt.imshow(redChannel)
    registerImage(blueChannel, greenChannel, redChannel)

# register greenChannel and redChannel channels to the blueChannel channel


def registerImage(blueChannel, greenChannel, redChannel):
    alignGreenToBlue = align(blueChannel, greenChannel, 20)
    alignRedtoBlue = align(blueChannel, redChannel, 20)
    print(alignGreenToBlue, alignRedtoBlue)
    rollImage(greenChannel, alignGreenToBlue, redChannel, alignRedtoBlue, blueChannel)

# roll image according to ncc algorithm's match output


def rollImage(greenChannel, alignGreenToBlue, redChannel, alignRedtoBlue, blueChannel):
    g = np.roll(greenChannel, alignGreenToBlue, axis=(0, 1))
    r = np.roll(redChannel, alignRedtoBlue, axis=(0, 1))
    stackImages(r, g, blueChannel)

# stack r and g in sequence depth wise (along blueChannel) and clear borders


def stackImages(r, g, blueChannel):
    coloured = (np.dstack((r, g, blueChannel))).astype(np.uint8)
    coloured = coloured[int(coloured.shape[0]*0.05):int(coloured.shape[0]-coloured.shape[0]*0.05),
                        int(coloured.shape[1]*0.05):int(coloured.shape[1]-coloured.shape[1]*0.05)]
    coloured = Image.fromarray(coloured)
    saveImage(coloured)

# save image


def saveImage(coloured):
    coloured.save("aligned_" + file)
    plt.figure()
    plt.imshow(coloured)

# initialize part


def main():
    global args
    args = sys.argv
    print(args[1])

    directory = args[1]
    images = []

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            images.append(f.split("\\")[1])
    print(images)

    for filename in images:
        global file
        file = filename
        readImage(filename)


if __name__ == "__main__":
    main()
