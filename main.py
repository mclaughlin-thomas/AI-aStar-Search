'''
Aiden Buterbaugh
Thomas McLaughlin
CS-255-01 INTRODUCTION TO ARTIFICIAL INTELLIGENCE INTELLIGENCE

Project 1
Due October 11, 2023

Objective:
    This program implements A*, to find the shortest path from a specified source node to a specified
    goal node. More specifically here, A* is applied to the real-world problem (RWP) of finding the shortest path to a user
    in a video game where edge weight indicates distance between nodes/states.
'''
import random
           
# Given: None
# Task: Create nodes to be used in a graph
# Return: None
class Node(object):
    def __init__(self, i, j):
        self.g = 0
        self.h = 0
        self.f = 0
        self.i = i
        self.j = j
        self.neighbors = []
        self.previous = None
        self.wall = False
        
        if (random.randint(1, 100) < 10):
            self.wall = True

    def __addNeighbors__(self, grid,width, height):
        i = self.i
        j = self.j
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
        

def setParameters():
    try:
        width = int(input("Enter the width of the graph: "))
        height = int(input("Enter the height of the graph: "))
        
        is_valid = True if width <= 0 or height <= 0 else False
        if is_valid is True:
            print("Number too small. Try again.\n\n")
            setParameters()
        return width, height
    except ValueError:
        print("Invalid input. Please enter valid integers.")
        return setParameters()  # calls fcn again if user inputs data wrong


def userGeneratedInput():
    dummy_tuple:int = ()
    x = int(input())
    y = int(input())
    new_tuple = dummy_tuple +(x,y,)
    return new_tuple


def createSpace(width, height):
    space = [0] * width

    for i in range(width): # entire space filled with 0's
        space[i] = [0] * height

    for i in range(width): # entire space filled with Nodes as well
        for j in range(height):
            node = Node(i,j)
            space[i][j] = node

    for i in range(width): #initializing every node's neighbors
        for j in range(height):
            space[i][j].__addNeighbors__(space, width, height)
    return space


def removeFromArray (array, element):
    for i in range(len(array) - 1, -1, -1):
        if (array[i] == element):
            array.pop(i)
 

def heuristic (a,b):
    # distance = math.dist((a.i, a.j), (b.i, b.j)) #euclidian distance, if ur feelin it ig| USE THIS IF U WANT TO ENABLE DIAGONAL
    distance = abs(a.i-b.i) + abs(a.j-b.j)
    return distance


def astar(startSpace, endSpace):
    path = []
    open_set = []
    closed_set = []


    open_set.append(startSpace)
    
    
    while open_set:  # This loop will continue as long as openSet is not empty
        winner = 0

        for i in range(len(open_set)):
            if(open_set[i].f < open_set[winner].f):
                winner = i

        current = open_set[winner]
        print("Cur node's vals")
        print(current.f," ",current.h," ",current.g," ")###
        print("\n")

        if current == endSpace:
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
        removeFromArray(open_set, current)
        closed_set.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            #g value increases one going to each square
            neighbor = neighbors[i]

            # little search inside a search
            if neighbor not in closed_set and not neighbor.wall: # IF ITS A NEIGHBOR thats not in the closed set
                tempG = current.g +1 #
                
                newPath = False
                if (neighbor in open_set):
                    if(tempG<neighbor.g):
                        neighbor.g = tempG
                        newPath = True
                else:
                    neighbor.g = tempG
                    newPath = True
                    open_set.append(neighbor)
                
                #heuristics
                if newPath:
                    neighbor.h = heuristic(neighbor, endSpace)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current

    print("No solution")
    return


def main():
    width, height = setParameters()
    space = createSpace(width, height)
    startSpace = space[0][0]
    endSpace = space[width-1][height-1]
    startSpace.wall = False
    endSpace.wall = False
    #endSpace = space[0][4]
    path = astar(startSpace, endSpace)
   
    if path:
        print("Path:")
        for node in reversed(path):
            print(f"({node.i}, {node.j})") 
    else:
        print("No path found")


if __name__=="__main__":
    main()
