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
import logging 
# REMOVE ONCE DONE, DO NOT SHIP WITH TESTING TOOLS ;)

# Given: None
# Task: Create nodes to be used in a graph
# Return: None
class TreeNode(object):
    def __init__(self, position, parent=None):
        self.position = position # Will be used once path found to list path
        self.parent = parent # # Will be used once path found to list path
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Heuristic (estimated cost from current node to goal node)
        self.f = 0  # Total cost (f = g + h)

    def __lt__(self, other):
        return self.f < other.f


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


def AddEdges(world):
    for i in range(len(world)):
        for j in range(len(world[i])):
            if i != j:  # To avoid self-loops, you can set diagonal elements to 0
                world[i][j] = random.randint(0, 1)  # Set a random 1 or 0 as the edge value
    return world

def CreateVirtualWorld(width, height):
    print("Create graph here")
    try:
        world = [[0 for _ in range(height)] for _ in range(width)] #graph is made here
        return world
    except MemoryError:
        print("Could not allocate sufficient space you punk")
        exit
    except Exception as e:
        print("An exception occurred: ", e)
        exit

def main():
    width, height = setParameters()
    print("Width entered: ", width, "\nHeight entered: ", height)
    world = CreateVirtualWorld(width, height)
    world = AddEdges(world)
    print(world)


if __name__=="__main__":
    main()
