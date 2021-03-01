import random

import numpy as np


class Sudoku:
    def __init__(self, sudoku=None):
        self.sudoku = sudoku

    def is_valid(self, r: int, c: int, v: int) -> bool:
        """Check if sudoku[r,c] can be value v"""
        if (
            v in self.sudoku[r, :]
            or v in self.sudoku[:, c]
            or v
            in self.sudoku[r // 3 * 3 : r // 3 * 3 + 3, c // 3 * 3 : c // 3 * 3 + 3]
        ):
            return False
        return True


class SudokuSolver(Sudoku):
    """Sudoku solver class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def sudoku_solver_backtrack(self, r: int, c: int) -> np.array:

        if c == 9:
            return self.sudoku_solver_backtrack(r + 1, 0)

        if r == 9:
            return self.sudoku

        if self.sudoku[r, c] != 0:
            return self.sudoku_solver_backtrack(r, c + 1)

        for i in range(1, 10):
            if self.is_valid(r, c, i):
                self.sudoku[r, c] = i
                solution = self.sudoku_solver_backtrack(r, c + 1)
                if solution is not False:
                    return solution

            self.sudoku[r, c] = 0
        return False


class SudokuGenerator(SudokuSolver):
    """Sudoku generator class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def sudoku_generator_backtrack(self, sudoku: np.array, level: int) -> np.array:
        """Use backtrack solver to generate sudoku"""

        res = sudoku.copy()

        remove_value = []

        while len(remove_value) < 81 - level:

            while True:
                r, c = random.randrange(0, 9), random.randrange(0, 9)
                if (r, c) not in remove_value:
                    break

            res[r, c] = 0

            self.sudoku = res.copy()
            if self.sudoku_solver_backtrack(0, 0) is not False:
                remove_value.append((r, c))
                res[r, c] = 0
        return res

    def sudoku_generator(self, seed, level: int) -> None:
        """sudoku generator"""

        assert level >= 17, "Level should >=17 to have unique solution!"

        while True:
            sudoku = np.zeros([9, 9], dtype=int)

            for i in range(3):
                seed = hash(str(seed))
                random.seed(seed)
                nums = [x for x in range(1, 10)]
                random.shuffle(nums)

                for j in range(3):
                    sudoku[3 * i + j, 3 * i : 3 * i + 3] = nums[3 * j : 3 * j + 3]

            self.sudoku = sudoku
            sudoku = self.sudoku_solver_backtrack(0, 0)
            if sudoku is not False:
                break
        random.seed(seed + level)
        self.sudoku = self.sudoku_generator_backtrack(sudoku, level)
