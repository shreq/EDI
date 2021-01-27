import numpy as np
import math


def get_squares(image_size, square_size, array):
    row = 0
    squares = []
    while row < image_size:
        col = 0
        while col < image_size:
            square = array[row:row + square_size, col:col + square_size]
            squares.append(square)
            col += square_size
        row += square_size
    return squares


def get_random_squares(n_squares, square_size, image_size, array):
    squares = []
    counter = 0
    while counter < n_squares:
        rand_row = np.random.randint(0, image_size - square_size + 1)
        rand_col = np.random.randint(0, image_size - square_size + 1)
        square = array[rand_row:rand_row +
                       square_size, rand_col:rand_col + square_size]
        squares.append(square)
        counter += 1
    return squares


def flatten_squares(squares):
    flatten_s = []
    for square in squares:
        square = square.flatten()
        flatten_s.append(square)
    return flatten_s


def to_squares(flatten_squares, square_size):
    squares = []
    for array in flatten_squares:
        array = array.reshape(square_size, square_size)
        squares.append(array)
    return squares


def calculate_PSNR(image_size, image_before, image_after):
    sum = 0
    for i in range(image_size):
        for j in range(image_size):
            sum += math.pow(image_before[i][j] - image_after[i][j], 2)

    divided_sum = sum / math.pow(image_size, 2)
    return 10 * math.log10(math.pow(255, 2) / divided_sum)
