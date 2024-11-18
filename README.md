# AI-aStar-Search
This program creates a perfectly square search space based off the users input and performs numerous variations of A* with different heuristics displayed visually using pygame.

<img src="search.gif" alt="search" />

## INSTALLATION: 

Pygame is required for the visuals.
```
pip install pygame
```

## CAPABILITIES:
- This program can perform A* with Manhattan or Euclidean heuristics. You can alter which heuristics function is called in the "astar" functionon on lines 236 and 246 by calling whicher heuristics function you prefer.

      -"heuristic_manhattan"  for Manhattan heuristics
      -"heuristic_euclidean"  forEuclidean heuristics
      
- Diagonal movement can also be enabled/disabled. To disable diagonal movement, make Diag=False. To enable diagonal movement, make Diag=True.

- Wall/obstacles can also be enabled/disabled, as well as percent increase or decrease. To enable obstacles/walls within the search space, on line 45, make WALL_PROBABILITY be greater than 0 and to your desired liklihood of the node becoming a wall. To disable obstacles/walls within the search space, on line 45, make WALL_PROBABILITY be less than or equal to 0. When creating the search space full of nodes, each nodes then have a percentage liklihood of themselves becoming a wall, below is that funciton: this is not a traditional maze.
          
          if random.randint(1, 100) < WALL_PROBABILITY:
            self.wall = True
            

## INSTRUCTIONS:
- Install pygame and all other dependencies
- Run
- Let the search space be created. (All nodes default path cost of 1)
- View popout window and watch A* in action
