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
import csv
import gc
import time
import math
from queue import PriorityQueue 



class Node(object):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    def __init__(self, x, y):
        self.gval = 0
        self.hval = 0
        self.fval = 0
        self.xval = x
        self.yval = y
        self.neighbors = []
        self.previous = None
        self.wall = False

        # if random.randint(1, 100) < -1:
        #     self.wall = True

    def add_neighbors(self, grid,width, height):
        """
        Given: None
        Task: Create nodes to be used in a graph
        Return: None
        """
        x = self.xval
        y = self.yval
        if x < width-1 :
            self.neighbors.append(grid[x+1][y])
        if x > 0:
            self.neighbors.append(grid[x-1][y])
        if y < height-1:
            self.neighbors.append(grid[x][y+1])
        if y>0:
            self.neighbors.append(grid[x][y-1])
        #DIAGONALS
        # if x> 0 and y>0:
        #     self.neighbors.append(grid[x-1][y-1])
        # if x < width -1 and y>0:
        #     self.neighbors.append(grid[x+1][y-1])
        # if x > 0 and y> height -1:
        #     self.neighbors.append(grid[x-1][y+1])
        # if x < width-1 and y < height-1:
        #     self.neighbors.append(grid[x+1][y+1])
    def __lt__(self, other):
        return self.fval < other.fval


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

def create_space(width, height):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    space = [[Node(i, j) for j in range(width)] for i in range(height)]
    gc.collect()


    print("Completed init neighbors's\n")
    gc.collect()

    return space


def remove_from_array (array, element):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    for i in range(len(array) - 1, -1, -1):
        if array[i] == element:
            array.pop(i)


def heuristic_manhattan(node_one, node_two):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    distance = abs(node_one.xval-node_two.xval) + abs(node_one.yval-node_two.yval) #Manhattan
    return distance
def heuristic_euclidean(node_one, node_two):
    dx = node_one.xval - node_two.xval
    dy = node_one.yval - node_two.yval
    return math.sqrt(dx * dx + dy * dy)


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    
    while current != start:
        current = came_from[current]
        path.append(current)
        
    return list(reversed(path))


def astar_manhattan(start_space, end_space, space, width, height):
    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}
    cost_so_far[start_space] = 0
    closed_set = set()

    node = start_space  
    # Update start node's g, h, and f values

    frontier.put((0, node))

    opened_nodes = 0  # Initialize the counter for opened nodes

    while not frontier.empty():
        _, popped_node = frontier.get()
        print(popped_node.xval , " ", popped_node.yval)
        popped_node.add_neighbors(space, width, height)


        if popped_node.xval == end_space.xval and popped_node.yval == end_space.yval:
            print(f"nodes opened\n{opened_nodes}")
            path  = reconstruct_path(came_from, start_space, popped_node)
            return path, opened_nodes
        closed_set.add(popped_node)

        for neighbor in popped_node.neighbors:
            print(f"Going through neighbor @ {neighbor.xval}, {neighbor.yval}")
            if neighbor in closed_set:
                print("This neighbor has already been explored! not doing that again!")
                continue
            newG = cost_so_far[popped_node] + 1

            if neighbor not in cost_so_far or newG < cost_so_far[neighbor]:
                print("Adding stuff to frontier")
                cost_so_far[neighbor] = newG
                priority_f = newG + heuristic_manhattan(neighbor, end_space)
                frontier.put((priority_f, neighbor))
                came_from[neighbor] = popped_node
                opened_nodes += 1

        # Update neighbors' g, h, and f values
        for neighbor in popped_node.neighbors:
            if neighbor is None:
                continue
            neighbor.gval = cost_so_far[neighbor]
            neighbor.hval = heuristic_manhattan(neighbor, end_space)
            neighbor.fval = neighbor.gval + neighbor.hval

    return None

def astar_euclidean(start_space, end_space, space, width, height):
    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}
    cost_so_far[start_space] = 0
    closed_set = set()

    node = start_space  
    # Update start node's g, h, and f values

    frontier.put((0, node))

    opened_nodes = 0  # Initialize the counter for opened nodes

    while not frontier.empty():
        _, popped_node = frontier.get()
        print(popped_node.xval , " ", popped_node.yval)
        popped_node.add_neighbors(space, width, height)


        if popped_node.xval == end_space.xval and popped_node.yval == end_space.yval:
            print(f"nodes opened\n{opened_nodes}")
            return reconstruct_path(came_from, start_space, popped_node), opened_nodes
        closed_set.add(popped_node)

        for neighbor in popped_node.neighbors:
            print(f"Going through neighbor @ {neighbor.xval}, {neighbor.yval}")
            if neighbor in closed_set:
                print("This neighbor has already been explored! not doing that again!")
                continue
            newG = cost_so_far[popped_node] + 1

            if neighbor not in cost_so_far or newG < cost_so_far[neighbor]:
                print("Adding stuff to frontier")
                cost_so_far[neighbor] = newG
                priority_f = newG + heuristic_euclidean(neighbor, end_space)
                frontier.put((priority_f, neighbor))
                came_from[neighbor] = popped_node
                opened_nodes += 1

        # Update neighbors' g, h, and f values
        for neighbor in popped_node.neighbors:
            if neighbor is None:
                continue
            neighbor.gval = cost_so_far[neighbor]
            neighbor.hval = heuristic_euclidean(neighbor, end_space)
            neighbor.fval = neighbor.gval + neighbor.hval

    return False

def save_data_euclidean(path, i, total_time, node_count):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: Nonep
    """
    #file_path_results = "AI-Project1\Manhattan Data\ZEROWALLTWELVETHOUSAND\data.csv"
    file_path_results = "C:\\Users\Handrail\Documents\Project 1\Euclidean\hNoWalls\hNoDiag\h2500\data.csv"
    #file_path_adjtable = "C:\\Users\Handrail\Desktop\Manhattan Data\ZEROWALLFOURTHOUSAND\Adjtable.csv"
    

    with open(file_path_results, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Use writerow to write the header (if any) and data rows
        for node in reversed(path):
            writer.writerow([node.xval, node.yval])
        writer.writerow(["total states(including start and goal)", i])
        writer.writerow(["Time for Astar", total_time])
        writer.writerow(["Nodes opened", node_count])

def save_data_manhattan(path, i, total_time, node_count):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: Nonep
    """
    #file_path_results = "AI-Project1\Manhattan Data\ZEROWALLTWELVETHOUSAND\data.csv"
    file_path_results = "C:\\Users\Handrail\Documents\Project 1\Manhattan\hNoWalls\hNoDiag\h2500\data.csv"
    #file_path_adjtable = "C:\\Users\Handrail\Desktop\Manhattan Data\ZEROWALLFOURTHOUSAND\Adjtable.csv"
    

    with open(file_path_results, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Use writerow to write the header (if any) and data rows
        for node in reversed(path):
            writer.writerow([node.xval, node.yval])
        writer.writerow(["total states(including start and goal)", i])
        writer.writerow(["Time for Astar", total_time])
        writer.writerow(["Nodes opened", node_count])




def main():
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    width, height = set_parameters()
    space = create_space(width, height)
    start_space = space[0][0]    
    end_space = space[width-1][height-1]
    # start_space.wall = False
    # end_space.wall = False


    # print("\nStarting search\n")
    # start = time.time() # Start Timer
    # path, node_count  = astar_manhattan(start_space, end_space, space, width, height)
    # end =  time.time() # End Timer
    # total_time= end - start
    # print("\nEnding search\n")


    # if path:
    #     print("Path:\n")
    #     for node in path:
    #         print(f"({node.xval}, {node.yval})")
    #     print(f"Total path length: {len(path)-1}")
    #     print(f"Total time taken: {total_time} seconds")
    #     print(f"Nodes explored from openset: {node_count }")
    #     save_data_manhattan(path, len(path)-1, total_time, node_count)
    # else:
    #     print("No path found")


    print("Starting search")
    start = time.time() # Start Timer
    path, node_count  = astar_euclidean(start_space, end_space, space, width, height)
    end =  time.time() # End Timer
    total_time= end - start
    print("Ending search")


    if path:
        print("Path:")
        for node in path:
            print(f"({node.xval}, {node.yval})")
        print(f"Total path length: {len(path)-1}")
        print(f"Total time taken: {total_time} seconds")
        print(f"Nodes explored from openset: {node_count }")
        save_data_euclidean(path, len(path)-1, total_time, node_count)
    else:
        print("No path found")

if __name__=="__main__":
    main()



# TRIED AND TRUE

# CREATE create_space
# """
#     Given: None
#     Task: Create nodes to be used in a graph
#     Return: None
#     """
#     space = [0] * width
#     adjacency = {} #NEW---------------------------


#     for i in range(width): # entire space filled with 0's (No obstacles)
#         space[i] = [0] * height
#     print("Completed 0's\n")

#     for i in range(width): # entire space filled with Nodes as well
#         for j in range(height):
#             node = Node(i,j)
#             space[i][j] = node
#             adjacency[(i, j)] = [] #NEW---------------------------
#     print("Completed filling with nodes\n")

#     for i in range(width): #initializing every node's neighbors
#         for j in range(height):
#             space[i][j].add_neighbors(space, width, height)
#     print("Completed init neighbors's\n")
    
#     for i in range(width):  # initializing every node's neighbors #NEW---------------------------
#         for j in range(height): #NEW---------------------------
#             node = space[i][j] #NEW---------------------------
#             for neighbor in node.neighbors: #NEW---------------------------
#                 adjacency[(i, j)].append(((neighbor.ival, neighbor.jval), 1)) # PUT G COST HERE #NEW
#     print("Completed adj's\n")
#     return space, adjacency


# MAIN
#         """
#     Given: None
#     Task: Create nodes to be used in a graph
#     Return: None
#     """
#     width, height = set_parameters()
#     space, adjacency = create_space(width, height)
#     start_space = space[0][0]
#     end_space = space[width-1][height-1]
#     start_space.wall = False
#     end_space.wall = False

#     print("Starting search")
#     path = astar(start_space, end_space, adjacency)
#     print("Ending search")

#     if path:
#         print("Path:")
#         i =0
#         for node in reversed(path):
#             print(f"({node.ival}, {node.jval})")
#             i=i+1
#         #save_data(path, space, adjacency, i)
#     else:
#         print("No path found")