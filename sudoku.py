from z3 import Int, Solver, Distinct, sat, And
from itertools import product

grid = lambda i, j: Int("grid[%d, %d]" % (i+1, j+1))
val_range = lambda left, middle, right: And(left <= middle, middle <= right)

class SudokuSolver(Solver):
    GRID_SIZE = 9
    SUB_GRID_SIZE = 3

    def __init__(self, problem):
        super(SudokuSolver, self).__init__()
        self.problem = problem
        self._set_problem()

    def solve(self):
        self._set_restriction()
        return self.check()
    
    def _set_problem(self):
        N = SudokuSolver.GRID_SIZE
        for i, j in product(range(N), range(N)):
            if self.problem[i][j] > 0:
                self.add(grid(i, j) == self.problem[i][j])
    
    def _set_restriction(self):
        N = SudokuSolver.GRID_SIZE
        B = SudokuSolver.GRID_SIZE // SudokuSolver.SUB_GRID_SIZE
        S = SudokuSolver.SUB_GRID_SIZE

        # set initial value
        # product: 直積のこと．repeatの数だけ直積される．
        self.add(*[val_range(1, grid(i, j), 9) for i, j in product(range(N), repeat=2)])
        
        # distinct w.r.t columns
        for row in range(N):
            self.add(Distinct([grid(row, col) for col in range(N)]))
        
        # distinct w.r.t rows
        for col in range(N):
            self.add(Distinct([grid(row, col) for row in range(N)]))
        
        # distinct w.r.t blocks
        for row in range(B):
            for col in range(B):
                block = [grid(B*row+i, B*col+j) for i, j in product(range(S), repeat=2)]
                self.add(Distinct(block))
                
def solve_sudoku(problem, smt_2_filename=None):
    solver = SudokuSolver(problem)
    result = solver.solve()

    if smt_2_filename:
        with open(smt_2_filename, 'w') as f:  
            f.write(solver.to_smt2())

    if result == sat:
        model = solver.model()
        
        # print result
        N = SudokuSolver.GRID_SIZE
        for i in range(N):
            row = [model[grid(i, j)].as_long() for j in range(N)]
            print(*row)
    else:
        print(result)

    print()

def main():
    problem1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 8, 0],
                [6, 4, 0, 0, 0, 0, 7, 0, 0],
                [0, 0, 0, 0, 0, 3, 0, 0, 0],
                [0, 0, 1, 8, 0, 5, 0, 0, 0],
                [9, 0, 0, 0, 0, 0, 4, 0, 2],
                [0, 0, 0, 0, 0, 9, 3, 5, 0],
                [7, 0, 0, 0, 6, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0, 0, 0, 0]]
    solve_sudoku(problem1, 'sudoku_problem1.smt')

    problem2 = [[0, 0, 0, 0, 0, 0, 0, 3, 9],
                [0, 0, 0, 0, 0, 1, 0, 0, 5],
                [0, 0, 3, 0, 5, 0, 8, 0, 0],
                [0, 0, 8, 0, 9, 0, 0, 0, 6],
                [0, 7, 0, 0, 0, 2, 0, 0, 0],
                [1, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 9, 0, 8, 0, 0, 5, 0],
                [0, 2, 0, 0, 0, 0, 6, 0, 0],
                [4, 0, 0, 7, 0, 0, 0, 0, 0]]
    solve_sudoku(problem2, 'sudoku_problem2.smt')

if __name__ == '__main__':
    main()