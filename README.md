# CV based Sudoku-solver

## Steps:
1. Load the image  
![1](./asset/emp_png)  
2. get regional proposals from [MSER algorithm](https://en.wikipedia.org/wiki/Maximally_stable_extremal_regions)  
![2](./asset/emp_2.png)
3. Detect whether digits or not in regional proposals  
![3](./asset/emp_3.png)
4. Remove overlapped bounding boxes and classify digits  
![4](./asset/emp_4.png)
5. Translate bounding boxes and digits into 'sudoku'  
![5](./asset/emp_5.png)
6. Solve the sudoku (backtrack algorithm)  
![6](./asset/emp_6.png)
7. Draw back on the image  
![7](./asset/emp_7.png)  

## Installation

## TODO
