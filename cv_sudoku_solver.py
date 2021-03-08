import argparse
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from src.sudoku.sudoku import SudokuSolver
from src.sudoku_translator import sudoku_translator, SudokuTranlator
from src.regional_proposal.regional_proposal import RpMser
from src.utils.utils import draw_bboxes, draw_digits, remove_overlapped_bboxes

detector_model_path = "./model/digit_detector.h5"
classifier_model_path = "./model/digit_classifier.h5"

detector_model = tf.keras.models.load_model(detector_model_path)
classifier_model = tf.keras.models.load_model(classifier_model_path)


def parse_arguments(argv):

    parser = argparse.ArgumentParser(description="CV-based sudoku solver")
    parser.add_argument("img_path", type=str)

    return parser.parse_args()


def main(args):

    img = args.img_path

    if isinstance(img, str):
        img = cv2.imread(img)

    # Turn img into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Get regional proposal from MSER algorithm
    mser = RpMser()
    bboxes = mser.get_bboxes(gray)

    # Remove some overlapped rps
    bboxes = mser.remove_overlap_rp(bboxes, 0.2)
    rps = mser.get_cropped_rps(gray.copy(), bboxes)

    resized_rps = []
    for rp in rps:
        resized_rp = cv2.resize(rp, (32, 32))
        resized_rps.append(resized_rp)
    resized_rps = np.expand_dims(resized_rps, axis=-1)

    # Detect rps containing digits
    digits_bb = detector_model.predict(resized_rps)

    # Filter out non-digit rps
    cls_bb = np.array(bboxes)[digits_bb[:, 0] == 1, :]

    # Again, Remove overlapped rps
    cls_bb = remove_overlapped_bboxes(list(cls_bb))
    rps = mser.get_cropped_rps(gray.copy(), cls_bb)

    resized_rps = []
    for rp in rps:
        r = cv2.resize(rp, (32, 32))
        resized_rps.append(r)
    resized_rps = np.expand_dims(resized_rps, axis=-1)

    sudoku_digits = classifier_model.predict(resized_rps)

    st = SudokuTranlator()
    sudoku = st.translate_sudoku(cls_bb, np.argmax(sudoku_digits, axis=1))

    # Solve the sudoku
    s = SudokuSolver(sudoku=sudoku.copy())
    s.sudoku_solver_backtrack(0, 0)
    print(s.sudoku)

    solution_img = st.fill_sudoku(img.copy(), s.sudoku)

    fig = plt.figure(figsize=(8, 8))
    plt.axis("off")
    plt.imshow(solution_img)
    plt.show()


if __name__ == "__main__":

    main(parse_arguments(sys.argv[1:]))
