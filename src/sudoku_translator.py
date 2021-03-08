"""Translate bounding boxes and digits into sudoku format"""

import numpy as np

# Only apply for digits occur in the 'outside' grid
# (at least one digit in the first&last row&column)
# TODO: better solution to cover every case
def sudoku_translator(bboxes, digits):

    # get the center of each bbox
    center = []
    for bbox in bboxes:
        center.append((bbox[1] + bbox[3] / 2, bbox[0] + bbox[2] / 2))

    # get the sudoku grid coorinate
    left = min([x for x, y in center])
    right = max([x for x, y in center])
    bottom = max([y for x, y in center])
    up = min([y for x, y in center])

    # computre the gap between digits
    v_gap = round((bottom - up) / 8, 2)
    h_gap = round((right - left) / 8, 2)

    h_bin = [int(left - h_gap / 2 + i * h_gap) for i in range(10)]
    v_bin = [int(up - v_gap / 2 + i * v_gap) for i in range(10)]

    sudoku = np.zeros((9, 9), dtype=int)
    for (i, j), digit in zip(center, digits):
        x, y = np.digitize(i, v_bin), np.digitize(j, h_bin)
        sudoku[x - 1, y - 1] = digit

    return sudoku
