# CV based Sudoku-solver


## Steps:
1. Load the image  
![1](./asset/emp_1.png)  
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

Clone this repo:
`git clone https://github.com/ZequnZ/Sudoku-generator-solver.git`  
### Dependency management
`pyenv` + `poetry`

Install [pyenv](https://github.com/pyenv/pyenv#choosing-the-python-version):  
`curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash`  

Modify env variable:  
`export PATH="<.pyenv path>/bin:$PATH"`

Install  *python3.8.2*:  
`pyenv install 3.8.2`

Intall and ctivate virtual env:  
`pyenv virtualenv 3.8.2 sudoku382`  
`pyenv activate sudoku382`

Install [poetry](https://python-poetry.org/)
`pip install poetry`

Install dependency:  
`poetry install`


TODO: docker support

## TODO
