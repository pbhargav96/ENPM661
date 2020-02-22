import numpy as np  #Numpy imported to do Numerical analysis

goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]) # The final state to be reached
movements = ["Left", "Up", "Right", "Down"] # The movement sperformed by the blank tile
# Creating Empty lists to be called upon later in the code
state = [] 
all_nodes = []
backtracking_nodes = []

# Creating a class and defining 
class solve_puzzle:
    # __init__ used to define the objects being created
    def __init__(self, node_state_i, node_index_i, parent_node_index_i, action, traverse):
        self.node_state_i = node_state_i
        self.node_index_i = node_index_i
        self.parent_node_index_i = parent_node_index_i
        self.action = action
        self.traverse = traverse

def user_input():   #code for taking in puzzle values from user
    input_values = [] #empty list created 
    values = input("Please enter values from 0-8 in succession: ")
    for i in values:
        if len(values) > 9:
            raise Exception("Only nine digits from 0-8 allowed")
        input_values.append(int(i))
    return np.reshape(input_values,(3,3))

def puzzle_solvability(input_values): #checking for inversion
    inversion_count = 0
    puzzle = np.reshape(input_values,9)
    for i in range(len(puzzle)):    # checks for the inversion whether it is odd or even
        for j in range(i+1, len(puzzle)):
            if puzzle[i] and puzzle[j] and puzzle[i] > puzzle[j]:
                inversion_count +=1
    if inversion_count % 2 == 0: # if the remainder is zero inversion is an even number thus puzzle is solvable
        print("The Puzzle is Solvable please wait a moment :")
    else:
        print("The number of inversions are odd please run the code again.")


def blank_tile_location(zero_node): #blank tile location which is represented by zero
        for i in range(0,3): # takes in index values 0,1,2
            for j in range(0,3):
                if zero_node[i,j] == 0:
                    return i,j


def swap_left(node_index_i):
    i,j = blank_tile_location(node_index_i)
    new_node = node_index_i.copy()
    if j == 0:
        return None
    else:
        new_node[i,j], new_node[i,j-1] = new_node[i,j-1], new_node[i,j]
        return new_node

def swap_up(node_index_i):
    i,j = blank_tile_location(node_index_i)
    new_node = node_index_i.copy()
    if i == 0:
        return None
    else:
        new_node[i,j], new_node[i-1,j] = new_node[i-1,j], new_node[i,j]
        return new_node

def swap_right(node_index_i):
    i,j = blank_tile_location(node_index_i)
    new_node = node_index_i.copy()
    if j == 2:
        return None
    else:
        new_node[i,j], new_node[i,j+1] = new_node[i,j+1], new_node[i,j]
        return new_node

def swap_down(node_index_i):
    i,j = blank_tile_location(node_index_i)
    new_node = node_index_i.copy()
    if i == 2:
        return None
    else:
        new_node[i,j], new_node[i+1,j] = new_node[i+1,j], new_node[i,j]
        return new_node


def swap_tile(swap, node_index_i):
    if swap == 'Left':
        return swap_left(node_index_i)
    elif swap == 'Up':
        return swap_up(node_index_i)
    elif swap == 'Right':
        return swap_right(node_index_i)
    elif swap == 'Down':
        return swap_down(node_index_i)
    else:
        return None


def generate_path(nodes) :  # backtracking path from goal state to input state
    state.append(nodes)
    main_node = nodes.parent_node_index_i
    while main_node is not None:
        state.append(main_node)
        main_node = main_node.parent_node_index_i
    return list(reversed(state))

def node_path(path):  # Exporting the states taken to reach the path
    f = open("nodePath.txt", "w")
    for nodes in path:
        if nodes.parent_node_index_i is not None:
            f.write(str(nodes.parent_node_index_i) + "\t" + "\n")
    f.close()


def nodes_info(info): # Exporting node index and parent node index

    f = open("NodesInfo.txt", "w")
    for n in info:
        if n.parent_node_index_i is not None:
            f.write(str(n.node_state_i) + "\t" +str(n.parent_node_index_i.node_state_i) + "\n")
    f.close()

def all_nodes_visited(visited):  # Exporting all the states created to a text file

    f = open("Nodes.txt", "w")
    for element in visited:
        for i in range(len(element)):
            for j in range(len(element)):
                f.write(str(element[j][i]) + " ")
        f.write("\n")
    f.close()

# code to find the nodes 
def finding_nodes(nodes):     
    a = [nodes]
    all_nodes.append(a[0].node_index_i.tolist())  
    count_nodes = 0  

    while a:
        current_state = a.pop(0)  # from the list created 0 is popped
        if current_state.node_index_i.tolist() == goal_state.tolist():
            print("Goal reached")
            return current_state, all_nodes, backtracking_nodes

        for tile in movements:
            temp_node = swap_tile(tile, current_state.node_index_i)
            if temp_node is not None:
                count_nodes += 1
                sub_node = solve_puzzle(count_nodes, np.array(temp_node), current_state, tile,0) 

                if sub_node.node_index_i.tolist() not in all_nodes:  
                    a.append(sub_node)
                    all_nodes.append(sub_node.node_index_i.tolist())
                    backtracking_nodes.append(sub_node)
                    if sub_node.node_index_i.tolist() == goal_state.tolist():                        
                        return sub_node, all_nodes, backtracking_nodes
    return None, None, None  



# Printing the path taken to reach the goal state
def print_states(get):  
    for g in get:
        print("\n" + str(g.node_index_i))
    print("\n" + "Goal State Reached")

run = user_input()  # call and run the data entered by the user
puzzle_solvability(run) # call and check for the solvability of the puzzle
base = solve_puzzle(0,run, None, None, 0)

# BFS implementation call to print the outputs and export text files
reach_goal, v, i = finding_nodes(base)
print_states(generate_path(reach_goal))
node_path(generate_path(reach_goal))
all_nodes_visited(v)
nodes_info(i)
