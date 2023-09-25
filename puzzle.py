# Sam Braun
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q

#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index < self.n:
            return None
        else:
            up, switched = self.config[:], self.blank_index - self.n
            up[self.blank_index], up[switched] = up[switched], up[self.blank_index]
            return PuzzleState(up, self.n, parent=self, action="Up", cost=self.cost+1)
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index > self.n**2 - self.n:
            return None
        else:
            down, switched = self.config[:], self.blank_index + self.n
            down[self.blank_index], down[switched] = down[switched], down[self.blank_index]
            return PuzzleState(down, self.n, parent=self, action="Down", cost=self.cost+1)
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index // self.n == 0:
            return None
        else:
            left, switched = self.config[:], self.blank_index - 1
            left[self.blank_index], left[switched] = left[switched], left[self.blank_index]
            return PuzzleState(left, self.n, parent=self, action="Left", cost=self.cost+1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index // self.n == self.n - 1:
            return None
        else:
            right, switched = self.config[:], self.blank_index + 1
            right[self.blank_index], right[switched] = right[switched], right[self.blank_index]
            return PuzzleState(right, self.n, parent=self, action="Right", cost=self.cost+1)
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(state, node_cnt):
    print("path to goal: " + path_to_goal(state))
    print("cost of path: the number of moves taken to reach the goal")
    print("nodes expanded: the number of nodes that have been expanded")
    print("search depth: the depth within the search tree when the goal node is found")
    print("max search depth: the maximum depth of the search tree in the lifetime of the algorithm running time: the total running time of the search instance, reported in seconds")
    print("max ram usage: the maximum RAM usage in the lifetime of the process as measured by the ru maxrss attribute")


def path_to_goal(state):
    steps = []
    
    while state != None:
        steps.append(state.parent.action)
        state = state.parent
    
    return steps[-2::-1]


def bfs_search(initial_state):
    """BFS search"""
    """
    function BREADTH-FIRST-SEARCH(initialState, goalTest) returns SUCCESS or FAILURE:
        frontier = Queue.new (initialState)
        explored = Set.new()

        while not frontier.isEmpty ():
            state = frontier.dequeue()
            explored.add(state)
            
            if goalTest (state):
                return SUCCEss(state)

            for neighbor in state.neighbors):
                if neighbor not in frontier U explored:
                    frontier.enqueue(neighbor)
        return FAILURE
    
    """
    frontier, explored = [], set()
    frontier.append(initial_state)

    # implement priority queue?
    while frontier:
        state = frontier.pop(0)
        explored.add(state)

        if test_goal(state):
            writeOutput(state, len(explored))
    
        for child in PuzzleState.expand(state):
            if child not in (frontier or explored):
                frontier.append(child)

    return -1 # failure?


def dfs_search(initial_state):
    """DFS search"""
    """
    function DEPTH-FIRST-SEARCH(initialState, goalTest) returns SUCCESS or FAILURE:
        frontier = Stack.new (initialState)
        explored = Set.new()

        while not frontier.isEmpty ():
            state = frontier.pop()
            explored.add(state)

            if goalTest (state):
                return SUCCESS(state)

            for neighbor in state.neighbors):
                if neighbor not in frontier U explored:
                    frontier.push(neighbor)

        return FAILURE
    """
    frontier, explored = [], set()
    frontier.append(initial_state)

    while frontier:
        state = frontier.pop(-1) # poping top of stack?
        explored.add(state)

        if test_goal(state):
            return
    
        for child in PuzzleState.expand(state):
            if child not in (frontier or explored) and child != None:
                frontier.append(child)

    return -1 # failure?    

def A_star_search(initial_state):
    """A * search"""
    """
    function A-STAR-SEARCH(initialState, goalTest) returns SUCCESS or FAILURE: /* Cost f(n) = g(n) + h(n) */
        frontier = Heap.new(initialState)
        explored = Set.new ()

        while not frontier.isEmpty ():
            state = frontier.deleteMin()
            explored.add(state)

            if goalTest (state):
                return SUCCEss(state)

            for neighbor in state.neighbors:
                if neighbor not in frontier U explored:
                    frontier. insert (neighbor)

                else if neighbor in frontier:
                    frontier.decreaseKey(neighbor)

        return FAILURE
    """

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    return state.cost

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    pass

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    goal = list(range(0, puzzle_state.n))
    return True if puzzle_state.config == goal else False

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
