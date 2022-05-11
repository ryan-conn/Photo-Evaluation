import os
import matplotlib.pyplot as plt
import tensorflow as tf
from data_loader import (
    load_certh_training_dataset,
    load_certh_testing_dataset,
    load_exposure_dataset,
    load_realblur_dataset,
    load_sidd_dataset,
)
from model import ImageRegression, ImageBinaryClassification

EXPOSURE_TRAINING_DATASET_FOLDER = r'E:\photography\exposure\training\INPUT_IMAGES'
EXPOSURE_VALIDATION_DATASET_FOLDER = r'E:\photography\exposure\validation\INPUT_IMAGES'
EXPOSURE_TESTING_DATASET_FOLDER = r'E:\photography\exposure\testing\INPUT_IMAGES'

BLUR_TRAINING_DATASET_FILE = r'E:\photography\blur\RealBlur_J_train_list.txt'
BLUR_TESTING_DATASET_FILE = r'E:\photography\blur\RealBlur_J_test_list.txt'

NOISE_DATASET_FOLDER = r'E:\photography\noise\Data'

def run_exposure_model(train=True):
    exposure_training_dataset = load_exposure_dataset(EXPOSURE_TRAINING_DATASET_FOLDER)
    exposure_training_dataset = exposure_training_dataset.map(lambda x, y: (augmentations(x), y))
    exposure_validation_dataset = load_exposure_dataset(EXPOSURE_VALIDATION_DATASET_FOLDER)
    exposure_testing_dataset = load_exposure_dataset(EXPOSURE_TESTING_DATASET_FOLDER)

    model = ImageRegression(4)
    if train:
        model.train(exposure_training_dataset, exposure_validation_dataset, 50)
    model.test(exposure_testing_dataset)

def run_blur_model(train=True):
    augmentations = tf.keras.Sequential([
        tf.keras.layers.RandomCrop(256, 256),
        tf.keras.layers.RandomFlip('horizontal'),
    ])

    blur_training_dataset = load_realblur_dataset(BLUR_TRAINING_DATASET_FILE)
    blur_training_dataset = blur_training_dataset.map(lambda x, y: (augmentations(x), y))
    blur_testing_dataset = load_realblur_dataset(BLUR_TESTING_DATASET_FILE)
    blur_testing_dataset = blur_testing_dataset.map(lambda x, y: (tf.image.crop_to_bounding_box(x, 0, 0, 256, 256), y))

    model = ImageBinaryClassification(4)
    if train:
        model.train(blur_training_dataset, blur_testing_dataset, 100)
    model.test(blur_testing_dataset)

def run_noise_model(train=True):
    augmentations = tf.keras.Sequential([
        tf.keras.layers.RandomCrop(256, 256),
        tf.keras.layers.RandomFlip('horizontal'),
    ])

    NUM_TRAINING_IMAGES = 600
    noise_dataset = load_sidd_dataset(NOISE_DATASET_FOLDER)
    noise_training_dataset = noise_dataset.take(NUM_TRAINING_IMAGES)
    noise_testing_dataset = noise_dataset.skip(NUM_TRAINING_IMAGES)

    noise_training_dataset = noise_training_dataset.map(lambda x, y: (augmentations(x), y))
    noise_testing_dataset = noise_testing_dataset.map(lambda x, y: (tf.image.crop_to_bounding_box(x, 0, 0, 256, 256), y))

    model = ImageBinaryClassification(4)
    if train:
        model.train(noise_training_dataset, noise_testing_dataset, 100)

if __name__ == '__main__':
    # run_exposure_model()
    # TODO: need to make work with any resolution, not just 512x512 - maybe make multiple predictions per image and average?
    # run_blur_model()
    run_noise_model()
