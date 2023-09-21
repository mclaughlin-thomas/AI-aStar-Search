'''
Aiden Buterbaugh
Thomas McLaughlin
CS-255-01 INTRODUCTION TO ARTIFICIAL INTELLIGENCE INTELLIGENCE

Project 1
Due October 11, 2023

Objective:
    This program implements A*, to find the shortest path from a specified source node to a specified goal node. More specifically,
    A* is applied to the real-world problem (RWP) of finding the shortest path to a user in a video game where edge weight indicates distance
    between nodes/states.
'''

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