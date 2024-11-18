'''
Aiden Buterbaugh
Thomas McLaughlin
CS-255-01 INTRODUCTION TO ARTIFICIAL INTELLIGENCE INTELLIGENCE

Project 1
Due October 11, 2023

Objective:
    This program implements A*: it will find the shortest path from a specified source node to
    a specified goal node. More specifically here, A* is applied to the real-world problem (RWP)
    of finding the shortest path to a user or location in a video game, where edge weight
    indicates distance between nodes/states. This program acts as a function that a game would
    call to find the shortest path to a user or location. The program will be tested on a 2D
    matrix of nodes, where each node has a weight of 1 as to better visualize the heuristic's 
    characteristics better.
'''

import time
from time import sleep
import math
import gc
import random
from queue import PriorityQueue
import sys
import pygame

# BOILER PLATE VISUALIZATION CODE
GRID_SIZE = 30
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CLOSEDSETCOLOR = (200, 200, 200)
FRONTIERCOLOR = (100, 100, 100)
PATHCOLOR = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# COLORS
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Sets the size of screen
pygame.display.set_caption("A* Visualization") # Sets the title of popout window
# BOILER PLATE VISUALIZATION CODE

WALL_PROBABILITY = 30


class Node(object):
    """
    Given: None
    Task: Create nodes to be used in a graph
    Return: None
    """
    def __init__(self, x, y, diagonal_moves):
        self.gval = 0
        self.hval = 0
        self.fval = 0
        self.xval = x
        self.yval = y
        self.neighbors = []
        self.previous = None
        self.wall = False
        self.diagonal_moves = diagonal_moves  # Added parameter for diagonal moves


        if random.randint(1, 100) < WALL_PROBABILITY:
            self.wall = True

    def add_neighbors(self, grid,width, height):
        """
        Given: grid, width, height
        Task: Append neighbors to neighbors list
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
        if self.diagonal_moves:
            if x > 0 and y > 0:
                self.neighbors.append(grid[x - 1][y - 1])
            if x < width - 1 and y > 0:
                self.neighbors.append(grid[x + 1][y - 1])
            if x > 0 and y < height - 1:
                self.neighbors.append(grid[x - 1][y + 1])
            if x < width - 1 and y < height - 1:
                self.neighbors.append(grid[x + 1][y + 1])

    def __lt__(self, other):
        """
        Given: Other node
        Task: Compare nodes
        Return: True/False
        """
        return self.fval < other.fval


def disable_diagonal_moves(space):
    """
    Given: A graph of nodes
    Task: Disable diagonal moves
    Return: None
    """
    for row in space:
        for node in row:
            node.diagonal_moves = False


def create_space(width, height, diag):
    """
    Given: width, height, and diagonal moves
    Task: Create nodes to be used in a graph
    Return: Space
    """
    space = [[Node(i, j, diag) for j in range(width)] for i in range(height)]
    gc.collect() # Clean up and deallocate memory no longer in use

    return space

def heuristic_manhattan(node_one, node_two):
    """
    Given: Two nodes
    Task: Calculate the Manhattan distance between given nodes
    Return: The Manhattan distance between node_one and node_two
    """
    distance = abs(node_one.xval-node_two.xval) + abs(node_one.yval-node_two.yval)
    return distance

def heuristic_euclidean(node_one, node_two):
    """
    Given: Two nodes
    Task: Calculate the Euclidean distance between given nodes
    Return: The Euclidean distance between node_one and node_two
    """
    dx = node_one.xval - node_two.xval
    dy = node_one.yval - node_two.yval
    return math.sqrt(dx * dx + dy * dy)


def reconstruct_path(came_from, start, goal):
    """
    Given: came_from, start, goal
    Task: Reconstruct the path
    Return: The optimal path
    """
    current = goal
    path = [current]
   
    while current != start:
        current = came_from[current]
        path.append(current)
       
    return list(reversed(path))

def astar(start_space, end_space, space, width, height, screen):
    """
    Given: start_space, end_space, space, width, height, screen
    Task: Run the A* algorithm on space
    Return: The optimal path
    """
    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}
    cost_so_far[start_space] = 0
    closed_set = set()

    node = start_space
    frontier.put((0, node))
    opened_nodes = 0  # Initialize the counter for opened nodes

    while not frontier.empty():
        _, popped_node = frontier.get()
        popped_node.add_neighbors(space, width, height)

        # Draw grid
        for row in space:
            for node in row:
                color = WHITE
                if node.wall:
                    color = BLUE
                pygame.draw.rect(screen, color, (node.xval * GRID_SIZE, node.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                pygame.draw.rect(screen, BLACK, (node.xval * GRID_SIZE, node.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        # Draw start and end nodes
        pygame.draw.rect(screen, PATHCOLOR, (start_space.xval * GRID_SIZE, start_space.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
        #pygame.draw.rect(screen, BLACK, (start_space.xval * GRID_SIZE, start_space.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
        pygame.draw.rect(screen, RED, (end_space.xval * GRID_SIZE, end_space.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
        #pygame.draw.rect(screen, BLACK, (end_space.xval * GRID_SIZE, end_space.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        # Draw closed set
        for node in closed_set:
            pygame.draw.rect(screen, CLOSEDSETCOLOR, (node.xval * GRID_SIZE, node.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            #pygame.draw.rect(screen, BLACK, (node.xval * GRID_SIZE, node.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        # Draw opened set
        for _, node in frontier.queue:
            pygame.draw.rect(screen, FRONTIERCOLOR, (node.xval * GRID_SIZE, node.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            #pygame.draw.rect(screen, BLACK, (node.xval * GRID_SIZE, node.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        # Update display
        pygame.display.flip()
        # Stagger what we see on the popup screen
        time.sleep(0.2)

        if popped_node.xval == end_space.xval and popped_node.yval == end_space.yval:
            print(f"nodes violated/insecpted\n{opened_nodes +1}")
            # Reconstruct the path
            path = reconstruct_path(came_from, start_space, end_space)

            # Highlight the best path in green
            for node in path:
                pygame.draw.rect(screen, PATHCOLOR, (node.xval * GRID_SIZE, node.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                #pygame.draw.rect(screen, BLACK, (node.xval * GRID_SIZE, node.yval * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

            # Update display
            pygame.display.flip()

            return path, opened_nodes
        closed_set.add(popped_node)

        for neighbor in popped_node.neighbors:
            if neighbor in closed_set:
                continue
            if neighbor.wall:
                continue
            new_g = cost_so_far[popped_node] + 1

            if neighbor not in cost_so_far or new_g < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_g
                priority_f = new_g + heuristic_manhattan(neighbor, end_space)
                frontier.put((priority_f, neighbor))
                came_from[neighbor] = popped_node
                opened_nodes += 1

        # Update neighbors' g, h, and f values
        for neighbor in popped_node.neighbors:
            if neighbor.wall is True:
                continue
            neighbor.gval = cost_so_far[neighbor]
            neighbor.hval = heuristic_manhattan(neighbor, end_space)
            neighbor.fval = neighbor.gval + neighbor.hval

    return False, 0


def main():
    """
    Given: None
    Task: Run the A* algorithm and display the results
    Return: None
    """

    # TRUE FOR DIAGONAL
    # FALSE FOR NODIAG
    diag = True

    widthHeight = 15

    space = create_space(widthHeight, widthHeight, diag)
    screen = pygame.display.set_mode((widthHeight * GRID_SIZE, widthHeight * GRID_SIZE))
    gc.collect() # Clean up and deallocate memory no longer in use

    start_space = space[0][0]    
    end_space = space[widthHeight-1][widthHeight-1]
    start_space.wall = False
    end_space.wall = False

    # Uncomment to disable diagonal after a run if you have multiple
    #disable_diagonal_moves(space)

    print("\nStarting search\n")
    start = time.time() # Start Timer
    path, node_count = astar(start_space, end_space, space, widthHeight, widthHeight, screen) # Run A* algo
    end =  time.time() # End Timer
    total_time= end - start
    print(total_time)
    print("\nEnding search\n")

    if path:
        print("Path:\n")
        for node in path:
            print(f"({node.xval}, {node.yval})")
        print(f"Total path length: {len(path)-1}")
        print(f"Total time taken: {total_time} seconds")
        print(f"Nodes explored from openset: {node_count +1}")
    else:
        print("No path found")

    # This will make the window stay up even after its done
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__=="__main__":
    main()
