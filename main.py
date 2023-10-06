'''
Aiden Buterbaugh
Thomas McLaughlin
CS-255-01 INTRODUCTION TO ARTIFICIAL INTELLIGENCE INTELLIGENCE

Project 1
Due October 11, 2023

Objective:
    This program implements A*, to find the shortest path from a specified source node to
    a specified goal node. More specifically here, A* is applied to the real-world problem (RWP)
    of finding the shortest path to a user
    in a video game where edge weight indicates distance between nodes/states.
'''
import random
import csv


class Node(object):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    def __init__(self, i, j):
        self.gval = 0
        self.hval = 0
        self.fval = 0
        self.ival = i
        self.jval = j
        self.neighbors = []
        self.previous = None
        self.wall = False

        if random.randint(1, 100) < -1:
            self.wall = True

    def add_neighbors(self, grid,width, height):
        """
        Given: None
        Task: Create nodes to be used in a graph
        Return: None
        """
        i = self.ival
        j = self.jval
        if i < width-1 :
            self.neighbors.append(grid[i+1][j])
        if i > 0:
            self.neighbors.append(grid[i-1][j])
        if j < height-1:
            self.neighbors.append(grid[i][j+1])
        if j>0:
            self.neighbors.append(grid[i][j-1])
        #DIAGONALS
        if i> 0 and j>0:
            self.neighbors.append(grid[i-1][j-1])
        if i < width -1 and j>0:
            self.neighbors.append(grid[i+1][j-1])
        if i > 0 and j> height -1:
            self.neighbors.append(grid[i-1][j+1])
        if i < width-1 and j < height-1:
            self.neighbors.append(grid[i+1][j+1])


def set_parameters():
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    try:
        width = int(input("Enter the width of the graph: "))
        height = int(input("Enter the height of the graph: "))

        is_valid = True if width <= 0 or height <= 0 else False
        if is_valid is True:
            print("Number too small. Try again.\n\n")
            set_parameters()
        return width, height
    except ValueError:
        print("Invalid input. Please enter valid integers.")
        return set_parameters()  # calls fcn again if user inputs data wrong


def user_generated_input():
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    dummy_tuple:int = ()
    input_one = int(input())
    input_two = int(input())
    new_tuple = dummy_tuple +(input_one,input_two,)
    return new_tuple


def create_space(width, height):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    space = [0] * width
    adjacency = {} #NEW---------------------------


    for i in range(width): # entire space filled with 0's (No obstacles)
        space[i] = [0] * height

    for i in range(width): # entire space filled with Nodes as well
        for j in range(height):
            node = Node(i,j)
            space[i][j] = node
            adjacency[(i, j)] = [] #NEW---------------------------

    for i in range(width): #initializing every node's neighbors
        for j in range(height):
            space[i][j].add_neighbors(space, width, height)

    for i in range(width):  # initializing every node's neighbors #NEW---------------------------
        for j in range(height): #NEW---------------------------
            node = space[i][j] #NEW---------------------------
            for neighbor in node.neighbors: #NEW---------------------------
                adjacency[(i, j)].append(((neighbor.ival, neighbor.jval), 1)) # PUT G COST HERE #NEW

    return space, adjacency


def remove_from_array (array, element):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    for i in range(len(array) - 1, -1, -1):
        if array[i] == element:
            array.pop(i)


def heuristic(node_one, node_two):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    # distance = math.dist((a.i, a.j), (b.i, b.j)) #euclidian distance, if ur feelin it ig
    # USE THIS IF U WANT TO ENABLE DIAGONAL
    distance = abs(node_one.ival-node_two.ival) + abs(node_one.jval-node_two.jval) #manhattan
    return distance


def astar(start_space, end_space, adjacency):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    path = []
    open_set = []
    closed_set = []


    open_set.append(start_space)


    while open_set:  # This loop will continue as long as openSet is not empty
        winner = 0

        for i in range(len(open_set)): # Janky priority Queue | Room for improvement
            if open_set[i].fval < open_set[winner].fval:
                winner = i

        current = open_set[winner]
        print("Cur node's vals")
        print(current.fval,"<-f ",current.hval,"<-h",current.gval,"<-g")###
        print("\n")

        if current == end_space:
            # if we find it, relay path
            path = []
            temp = current
            path.append(temp)
            while temp.previous:
                path.append(temp.previous)
                temp = temp.previous
            print("\n Done")
            # Print the coordinates of the node
            return path
        remove_from_array(open_set, current)
        closed_set.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            #g value increases one going to each square
            neighbor = neighbors[i]

            # little search inside a search del me later
            # IF ITS A NEIGHBOR thats not in the closed set del me later
            if neighbor not in closed_set and not neighbor.wall:
                 #Get the cost from the adjacency list based on the current and neighbor coordinates
                cost = None
                for neighbor_coord, adjacency_cost in adjacency[(current.ival, current.jval)]:
                    if neighbor_coord == (neighbor.ival, neighbor.jval):
                        cost = adjacency_cost
                        break

                if cost is not None:
                    temp_g = current.gval + cost  # Add the cost from the adjacency list


                new_path = False
                if neighbor in open_set:
                    if temp_g<neighbor.gval:
                        neighbor.gval = temp_g
                        new_path = True
                else:
                    neighbor.gval = temp_g
                    new_path = True
                    open_set.append(neighbor)

                #heuristics
                if new_path:
                    neighbor.hval = heuristic(neighbor, end_space)
                    neighbor.fval = neighbor.gval + neighbor.hval
                    neighbor.previous = current
    print("No solution")
    return


def save_data(path, space, adjacency, i):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    # document = open("AI-Project1/algo_data.txt", "a", encoding="utf-8")
    # document.write(f"{elapsed_time}\n") # had to make it one argument
    # document.close()
    file_path_results = "AI-Project1\Manhattan Data\ZEROWALLONEHUNDRED\data.csv"
    file_path_adjtable = "AI-Project1\Manhattan Data\ZEROWALLONEHUNDRED\Adjtable.csv"
    matrix_str = repr(adjacency)

    with open(file_path_results, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Use writerow to write the header (if any) and data rows
        for node in reversed(path):
            writer.writerow([node.ival, node.jval])
        writer.writerow(["total states(including start and goal)", i])
    with open(file_path_adjtable, mode='w') as file:
        file.write(matrix_str)




def main():
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    width, height = set_parameters()
    space, adjacency = create_space(width, height)
    start_space = space[0][0]
    end_space = space[width-1][height-1]
    start_space.wall = False
    end_space.wall = False

    path = astar(start_space, end_space, adjacency)

    if path:
        print("Path:")
        i =0
        for node in reversed(path):
            print(f"({node.ival}, {node.jval})")
            i=i+1
        save_data(path, space, adjacency, i)
    else:
        print("No path found")

if __name__=="__main__":
    main()
