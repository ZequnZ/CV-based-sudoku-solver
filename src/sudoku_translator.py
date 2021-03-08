"""Translate bounding boxes and digits into sudoku format"""

import cv2
import numpy as np


class SudokuTranlator:
    def __init__(self):
        pass

    # Only apply for digits occur in the 'outside' grid
    # (at least one digit in the first&last row&column)
    # TODO: better solution to cover every case
    def translate_sudoku(self, bboxes, digits) -> np.array:
        """Translate sudoku into a np.array"""

        self.bboxes = bboxes
        self.digits = digits

        # get the center of each bbox
        self.center = []
        for bbox in bboxes:
            self.center.append((bbox[1] + bbox[3] / 2, bbox[0] + bbox[2] / 2))

        # get the sudoku grid coorinate
        self.left = min([x for x, y in self.center])
        self.right = max([x for x, y in self.center])
        self.bottom = max([y for x, y in self.center])
        self.up = min([y for x, y in self.center])

        # compute the gap between digits
        self.v_gap = round((self.bottom - self.up) / 8, 2)
        self.h_gap = round((self.right - self.left) / 8, 2)

        self.h_bin = [
            int(self.left - self.h_gap / 2 + i * self.h_gap) for i in range(10)
        ]
        self.v_bin = [int(self.up - self.v_gap / 2 + i * self.v_gap) for i in range(10)]

        self.sudoku = np.zeros((9, 9), dtype=int)
        for (i, j), digit in zip(self.center, self.digits):
            x, y = np.digitize(i, self.v_bin), np.digitize(j, self.h_bin)
            self.sudoku[x - 1, y - 1] = digit

        return self.sudoku

    def fill_sudoku(self, image, solution: np.array, color=(0, 0, 0)):
        """fill the solution in the sudoku image"""

        for i in range(0, 9):
            for j in range(0, 9):

                if self.sudoku[j, i] != 0:
                    continue
                res = cv2.putText(
                    image,
                    str(solution[j, i]),
                    (int(self.left + i * self.h_gap), int(self.up + j * self.v_gap)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2,
                )
        return res
