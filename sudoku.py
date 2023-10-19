#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time
import numpy as np

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

def int_to_list(int_board):
    list_board = {}
    for tile in int_board:
        list_board[tile] = [int_board[tile]]
    
    return list_board

def lists_to_ints(list_board):
    int_board = {}
    for tile in list_board:
        int_board[tile] = list_board[tile][0]
    
    return int_board


def select_unassigned_variable(csp):
    print("in select_unassigned_variable")
    min_domain_size, min_domain_tile = 10, ""

    for tile in csp:
        if len(csp[tile]) < min_domain_size:
            min_domain_size, min_domain_tile = len(csp[tile]), tile
    
    if min_domain_size == 0:
        return None
    return min_domain_tile

def get_neighboring_tiles(tile):
    print("in get_neighboring_tiles")
    tile_row, tile_col, neighbors = tile[0], tile[1], set()

    # tile row
    # print("making neigb rows")
    for col in COL:
        neighbors.add(tile_row + col)
    # print(neighbors)
    
    # tile column
    # print("making neigb columns")
    for row in ROW:
        neighbors.add(row + tile_col)
    # print(neighbors)
    
    # tile mini box
    # print("making neigb mini box")
    col_idx, row_idx = COL.index(tile_col), ROW.index(tile_row)
    box_col, box_row = col_idx // 3, row_idx // 3

    box_cols = [COL[box_col * 3], COL[(box_col * 3) + 1], COL[(box_col * 3) + 2]]
    box_rows = [ROW[box_row * 3], ROW[(box_row * 3) + 1], ROW[(box_row * 3) + 2]]

    for cols in box_cols:
        for rows in box_rows:
            neighbors.add(rows + cols)
    
    #print(neighbors)
    
    neighbors.remove(tile)
    return list(neighbors)


def forward_check(csp, tile, value):
    print("in forward_checking")
    neighbors = get_neighboring_tiles(tile)
    for curr in neighbors:
        if value in csp[curr]:
            if len(csp[curr]) == 1: # ?????
                return None
            csp[curr].remove(value)
        if len(csp[curr]) == 0:
            return None

    return csp

def is_complete(board):
    for tile in board:
        if board[tile] == 0:
            return False
        
    return True
    
    # if not domain_check(board):
    #     return False
    
    # board_copy = board.copy()
    # if isinstance(board["A1"], list):
    #     board_copy = lists_to_ints(board_copy)
    
    # count = 0
    # for tile in board_copy:
    #     count += board[tile]
    # return count == 405


def backtracking_helper(board, csp):
    """Takes a board and returns solved board."""
    # TODO: implement this

    print("in backtracking_helper, csp made")

    if is_complete(board):
        return board
    
    if not csp:
        return None
    
    smallest_unassigned = select_unassigned_variable(csp)
    if smallest_unassigned is None:
        print("did not find smallest_unassigned")
        return None
    
    print("found smallest_unassigned")

    for value in csp[smallest_unassigned]: # ordered domain values???

        new_board = board.copy()
        new_board[smallest_unassigned] = value

        print(csp)
        print('\n \n')

        csp_copy = csp.copy()
        csp_copy[smallest_unassigned] = [value]
        new_csp = forward_check(csp_copy, smallest_unassigned, value)
        print(new_csp)
        if new_csp:
            result = backtracking_helper(new_board, new_csp)
            if result:
                return result

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
    print("in build_csp")

    csp = {}
    for col in COL:
        for row in ROW:
            if board[row + col] == 0:
                csp[row + col] = [1,2,3,4,5,6,7,8,9]
            else:
                csp[row + col] = [board[row + col]]
    
    # for row in ROW:
    #     for col in COL:
    #         if board[row + col] == 0:
    #             neighbors, domain = get_neighboring_tiles(row + col), csp[row + col]
    #             print("neighbors: " + str(neighbors))
    #             csp[row + col] = [num for num in domain if num not in [board[neighbor] for neighbor in neighbors]]

    print(csp)
    if csp:
        return csp
    return None

'''

dentify in the board where the empty tiles are:
        --Where the value is 0
        --Apply forward checking to see what values can immediately go in space w/o probs
    Find minimum remaining value huristic square
        --If can't find a valid opening then return the completed board or False
    Recurse
        --Try each value and then call backtracking on the remaining board
        --If recursion returns false, set it back to 0
'''

def backtracking(board):
    return backtracking_helper(board, build_csp(board))


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

        # rme = 'README.txt'
        # readme = open(rme, "w")
        # times = []
        # counter=0
        # maxv = 0
        # minv = 0
        # std = 0
        # mean = 0


        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            start_time = time.time()

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

            # end_time = time.time()
            # timecount= end_time-start_time
        
            # counter= counter+1
            # times.append(timecount)
        
        # readme.write("Succesful puzzles : "+str(counter)+'\n')
        # readme.write("Min Time : "+str(np.min(times))+'\n')
        # readme.write("Max Time : " + str(np.max(times)) + '\n')
        # readme.write("Mean Time : " + str(np.mean(times)) + '\n')
        # readme.write("Standard Dev: " + str(np.std(times)) + '\n')

        print("Finishing all boards in file.")


"""

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
"""