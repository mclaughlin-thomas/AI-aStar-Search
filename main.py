'''
Aiden Buterbaugh
Thomas McLaughlin
CS-255-01 INTRODUCTION TO ARTIFICIAL INTELLIGENCE INTELLIGENCE

Project 1
Due October 11, 2023

Objective:
    This program implements A*, to find the shortest path from a specified source node to a specified goal node. More specifically here,
    A* is applied to the real-world problem (RWP) of finding the shortest path to a user in a video game where edge weight indicates distance
    between nodes/states.
'''
import random  # DO NOT DELETE
import logging  # REMOVE ONCE DONE, DO NOT SHIP WITH TESTING TOOLS ;)




            # Added: space with obstacles, runs and finds path, just boring w distance all being the same
            # To add: different values for g(n) like svc gbg example in class 












# Given: None
# Task: Create nodes to be used in a graph
# Return: None
class TreeNode(object):
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def setParameters():
    try:
        width = int(input("Enter the width of the graph: "))
        height = int(input("Enter the height of the graph: "))
        
        is_valid = True if width <= 0 or height <= 0 else False
        if is_valid is True:
            print("Number too small. Try again.\n\n")
            setParameters()

        logging.info("width height:",width," ",height)
        return width, height
    except ValueError:
        print("Invalid input. Please enter valid integers.")
        return setParameters()  # calls fcn again if user inputs data wrong


def astar(grid, start, end):
    """Returns a list of positions as a path from the given start to the given end"""

    # Create start and end nodes
    start_node = TreeNode(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = TreeNode(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get cur node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return dat reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Check if the node is within the grid
            if 0 <= node_position[0] < len(grid) and 0 <= node_position[1] < len(grid[0]):
                # Make sure the node is not blocked (you can define your own criteria here)
                if grid[node_position[0]][node_position[1]] == 0:
                    # Create new node
                    new_node = TreeNode(current_node, node_position)
                    # Append
                    children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the g, h, and f values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def printMatrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))

def addObstacles(matrix ,obstacle_percentage):
    if obstacle_percentage < 0 or obstacle_percentage > 100:
        raise ValueError("Obstacle percentage should be between 0 and 100.")
    
    rows, cols = len(matrix), len(matrix[0])
    total_cells = rows * cols
    num_obstacles = int((obstacle_percentage / 100) * total_cells)

    obstacle_positions = set()

    while len(obstacle_positions) < num_obstacles:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        obstacle_positions.add((row, col))

    for row, col in obstacle_positions:
        matrix[row][col] = 1

def userGeneratedInput():
    dummy_tuple:int = ()
    x = int(input())
    y = int(input())
    new_tuple = dummy_tuple +(x,y,)
    return new_tuple

def main():
    width, height = setParameters()
    space = [[0 for _ in range(width)] for _ in range(height)]
    addObstacles(space , obstacle_percentage=20)
    printMatrix(space)

    start = userGeneratedInput()
    print(start)
    end = userGeneratedInput()
    print(end)

    path = astar(space, start, end)
    if path:
        print("Path found:", path)
    else:
        print("No path found")

if __name__=="__main__":
    main()










# class Node():
#     """A node class for A* Pathfinding"""

#     def __init__(self, parent=None, position=None):
#         self.parent = parent
#         self.position = position

#         self.g = 0
#         self.h = 0
#         self.f = 0

#     def __eq__(self, other):
#         return self.position == other.position

# def astar(grid, start, end):
#     """Returns a list of positions as a path from the given start to the given end"""

#     # Create start and end nodes
#     start_node = Node(None, start)
#     start_node.g = start_node.h = start_node.f = 0
#     end_node = Node(None, end)
#     end_node.g = end_node.h = end_node.f = 0

#     # Initialize both open and closed list
#     open_list = []
#     closed_list = []

#     # Add the start node
#     open_list.append(start_node)

#     # Loop until you find the end
#     while len(open_list) > 0:

#         # Get the current node
#         current_node = open_list[0]
#         current_index = 0
#         for index, item in enumerate(open_list):
#             if item.f < current_node.f:
#                 current_node = item
#                 current_index = index

#         # Pop current off open list, add to closed list
#         open_list.pop(current_index)
#         closed_list.append(current_node)

#         # Found the goal
#         if current_node == end_node:
#             path = []
#             current = current_node
#             while current is not None:
#                 path.append(current.position)
#                 current = current.parent
#             return path[::-1]  # Return reversed path

#         # Generate children
#         children = []
#         for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

#             # Get node position
#             node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

#             # Check if the node is within the grid
#             if 0 <= node_position[0] < len(grid) and 0 <= node_position[1] < len(grid[0]):
#                 # Make sure the node is not blocked (you can define your own criteria here)
#                 if grid[node_position[0]][node_position[1]] == 0:
#                     # Create new node
#                     new_node = Node(current_node, node_position)
#                     # Append
#                     children.append(new_node)

#         # Loop through children
#         for child in children:

#             # Child is on the closed list
#             for closed_child in closed_list:
#                 if child == closed_child:
#                     continue

#             # Create the g, h, and f values
#             child.g = current_node.g + 1
#             child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
#             child.f = child.g + child.h

#             # Child is already in the open list
#             for open_node in open_list:
#                 if child == open_node and child.g > open_node.g:
#                     continue

#             # Add the child to the open list
#             open_list.append(child)

# def main():
#     # Create a 10x10 grid with all nodes initially set to 0
    # grid = [[0 for _ in range(20)] for _ in range(10)]

    # # Define start and end points within the grid
    # start = (0, 0)
    # end = (9, 9)

    # path = astar(grid, start, end)
    # print(path)

# if __name__ == '__main__':
#     main()
