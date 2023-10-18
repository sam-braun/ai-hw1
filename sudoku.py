#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

ROW = "ABCDEFGHI"
COL = "123456789"

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def select_unassigned_variable(csp):
    min_domain_size, min_domain_tile = 10, ""

    for tile in csp:
        if len(csp[tile]) < min_domain_size:
            min_domain_size, min_domain_tile = len(csp[tile]), tile
    
    if min_domain_size == 0:
        return None
    return min_domain_tile

def board_check(board):
    print("in board_check")
   
    # iterate through columns
    for col in COL:
        seen = set()
        
        for row in ROW:
            tile_value = board[row + col]
            if tile_value in seen or tile_value == 0:
                return False
            seen.add(tile_value)

    # iterate through rows
    for row in ROW:
        seen = set()
        
        for col in COL:
            tile_value = board[row + col]
            if tile_value in seen or tile_value == 0:
                return False
            seen.add(tile_value)

    # iterate through boxes
    box_rows, box_cols = ["ABC", "DEF", "GHI"], ["123", "456", "789"]
    for rows in box_rows:
        for cols in box_cols:
            seen = set()
            for row in rows:
                for col in cols:
                    if board[row + col] in seen:
                        return False
                    seen.add(board[row + col])

    print("returns true")
    return True

def get_neighboring_tiles(tile):
    tile_row, tile_col, neighbors = tile[0], tile[1], set()

    # tile row
    for col in COL:
        neighbors.add(tile_row + col)
    
    # tile column
    for row in ROW:
        neighbors.add(row + tile_col)
    
    # tile mini box
    col_idx, row_idx = COL.index(tile_col), ROW.index(tile_row)
    box_col, box_row = col_idx // 3, row_idx // 3

    box_cols = [COL[box_col * 3], COL[(box_col * 3) + 1], COL[(box_col * 3) + 2]]
    box_rows = [ROW[box_row * 3], ROW[(box_row * 3) + 1], ROW[(box_row * 3) + 2]]

    for rows in box_cols:
        for cols in box_rows:
            neighbors.add(rows + cols)
    
    neighbors.remove(tile)
    return list(neighbors)


def forward_check(csp, tile, value):
    neighbors = get_neighboring_tiles(tile)
    for curr in neighbors:
        if value in csp[curr]:
            csp[curr].remove(value)
        if len(csp[curr]) == 0:
            return None

    return csp

def is_complete(board):
    count = 0
    for tile in board:
        count += board[tile]
    
    return count == 405

def backtracking_helper(board, csp):
    """Takes a board and returns solved board."""
    # TODO: implement this

    print("in backtracking_helper")

    if is_complete(board):
        print("is complete")
        return board
    
    print("board incomplete")


    smallest_unassigned = select_unassigned_variable(csp)
    if smallest_unassigned is None:
        print("did not find smallest_unassigned")
        return None
    
    print("found smallest_unassigned")

    for value in csp[smallest_unassigned]: # ordered domain values???
        csp_copy = csp.copy()
        new_csp = forward_check(csp_copy, smallest_unassigned, value)

        if new_csp is None:
            break

        print("new_csp made and is legit")
    
        # for tile in new_csp:
        #     if len(new_csp[tile]) == 1 and board[tile] == 0:
        #         board[tile] = new_csp[tile][0]
        
        board[smallest_unassigned] = value
        result = backtracking_helper(board, new_csp)
        if result:
            return result
        else:
            board[smallest_unassigned] = 0

    return None

    """
    function BACKTRACK(assignment, sp) returns a solution, or failure
        if assignment is complete:
            return assignment

        var = SELECT_UNASSIGNED-VARIABLE(sp)
        for each value in ORDER_DOMAIN_VALUES(var, assignment, csp):
            if value is consistent with assignment:
                add {var = value} to assignment
                result = BACKTRACK(assignment, csp)
                if result != failure:
                    return result
                remove {var = value} from assignment
        return failure
    """

def build_csp(board):
    csp = {}
    for col in COL:
        for row in ROW:
            if board[row + col] == 0:
                csp[row + col] = [1,2,3,4,5,6,7,8,9]
            else:
                csp[row + col] = [board[row + col]]
    
    for row in ROW:
        for col in COL:
            if board[row + col] == 0:
                neighbors, domain = get_neighboring_tiles(board[row + col]), csp[row + col]
                csp[row + col] = [num for num in domain if num not in neighbors]

    print(csp)
    if csp:
        return csp
    return None

def backtracking(board):
    csp = build_csp(board)
    if csp:
        final_board = backtracking_helper(board, csp)
        print("final board made")
    return final_board


if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        print("before backtracking")

        solved_board = backtracking(board)
        
        print("after backtracking")

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")
