from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd
import shutil
import helpers
import seaborn as sns
import os

K_PATTERNS = 20000
PATTERN_SIZE = 8
IMAGE_SIZE = 512
LEARNING_RATE = 0.01
MAX_ITER = 10000
HIDDEN_LAYER_NEURONS = [32, 20, 16, 12, 8, 6, 4, 2]

sns.set_theme(style='darkgrid')


def prepare_train_data(train):
    train_data = []
    for name in train:
        image = Image.open('images/' + name)
        normalized_image_array = np.array(image) / 255
        random_patterns = helpers.get_random_squares(
            K_PATTERNS, PATTERN_SIZE, IMAGE_SIZE, normalized_image_array)
        flatten_patterns = helpers.flatten_squares(random_patterns)
        train_data += flatten_patterns
    return train_data


def prepare_test_data(image_name):
    image = Image.open('images/' + image_name)
    normalized_image_array = np.array(image) / 255
    patterns = helpers.get_squares(
        IMAGE_SIZE, PATTERN_SIZE, normalized_image_array)
    flatten_patterns = helpers.flatten_squares(patterns)
    return flatten_patterns, np.array(image)


def patterns_to_image(array, pattern_size):
    row = np.empty((pattern_size, 0))
    rows = []

    for index, val in enumerate(array):
        row = np.concatenate((row, val), axis=1)

        if index % (IMAGE_SIZE / PATTERN_SIZE) == (IMAGE_SIZE / PATTERN_SIZE) - 1:
            rows.append(row)
            row = np.empty((pattern_size, 0))

    image_array = np.vstack(rows)
    return image_array


def normalize(arrays):
    for array in arrays:
        for i in range(len(array)):
            if array[i] > 1:
                array[i] = 1
            elif array[i] < 0:
                array[i] = 0
            array[i] = int(array[i] * 255)
    return arrays


def main():
    if os.path.exists('output'):
        shutil.rmtree('output')

    filenames = os.listdir('images')
    train, test = train_test_split(
        filenames, test_size=0.75, random_state=100)

    train_data = prepare_train_data(train)
    dict_of_df = {}
    df = pd.DataFrame(columns=['CR', 'PSNR'])
    test = filenames
    for name in test:
        dict_of_df[name] = df.copy()

    for num in HIDDEN_LAYER_NEURONS:
        clf = MLPRegressor(alpha=0., learning_rate_init=LEARNING_RATE, max_iter=MAX_ITER, activation="identity", momentum=0,
                           solver="sgd", hidden_layer_sizes=(num), random_state=100)
        clf.fit(train_data, train_data)

        for name in test:
            flatten_patterns, image_before = prepare_test_data(name)
            preds = clf.predict(flatten_patterns)

            preds = normalize(preds)
            prediction = helpers.to_squares(preds, PATTERN_SIZE)
            image_after = patterns_to_image(prediction, PATTERN_SIZE)

            dict_of_df[name] = dict_of_df[name].append(
                {'CR': (IMAGE_SIZE / PATTERN_SIZE) / num,
                 'PSNR': helpers.calculate_PSNR(IMAGE_SIZE, image_before, image_after)},
                ignore_index=True)

            image = Image.fromarray(image_after)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            if not os.path.exists('output/network'+str(num)):
                os.makedirs('output/network'+str(num))
            image.save('output/network'+str(num)+'/out_' + name.replace('.bmp', '.png'))

    for name in test:
        print(dict_of_df[name])
        sns.lineplot(data=dict_of_df[name], x="CR", y="PSNR")
        plt.title('Image ' + name.replace('.bmp', ''))
        plt.savefig('image_' + name.replace('.bmp', ''))
        plt.show()


if __name__ == "__main__":
    main()
