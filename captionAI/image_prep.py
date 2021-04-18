import requests

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# train image caption AI based off of provided dataset
# to make it easier we could train it off of a smaller dataset
#   - food
#   - nature
#   - respond to a person

# website where you can upload an image or provide a link to an image
# feed the image to the AI to get caption
# if we have extra time, we can train multiple models to give captions with different moods
# use twitter API to tweet image with caption
# get link to the post

from os import listdir
from pickle import dump
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model

# extract features from each photo in the directory


def extract_features(directory):
    # load the model
    model = VGG16()
    # re-structure the model
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
    # summarize
    print(model.summary())
    # extract features from each photo
    features = dict()
    for name in listdir(directory):
        # load an image from file
        filename = directory + '/' + name
        image = load_img(filename, target_size=(224, 224))
        # convert the image pixels to a numpy array
        image = img_to_array(image)
        # reshape data for the model
        image = image.reshape(
            (1, image.shape[0], image.shape[1], image.shape[2]))
        # prepare the image for the VGG model
        image = preprocess_input(image)
        # get features
        feature = model.predict(image, verbose=0)
        # get image id
        image_id = name.split('.')[0]
        # store feature
        features[image_id] = feature
        print('>%s' % name)
    return features


# extract features from all images
# make img_resized smaller
# directory = 
directory = 'insta_small_dataset/imgs'
features = extract_features(directory)
print('Extracted Features: %d' % len(features))
# save to file
dump(features, open('small_features.pkl', 'wb'))
# load doc into memory