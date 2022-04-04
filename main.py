# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 22:16:25 2022

@author: Adam Moyle
"""

from maze import Maze
from algorithms import depthFirstSearch, depthFirstSearchSolver, AStarSearch



# EXAMPLE 1: 100x100 maze generated and solved using depth-first search
#            Solve from top-left to bottom-right
#            Save image to file "dfs_maze.png"
maze = Maze([100, 100])
depthFirstSearch(maze)
solution_path = depthFirstSearchSolver(maze)
maze.saveImage(filename="./dfs_maze.png", path=solution_path)


# EXAMPLE 2: 500x100 maze generated using depth-first search
#            Solved using A* search
#            Saved image to file "dfs_astar_maze.png"
maze = Maze([500, 100])
depthFirstSearch(maze)
solution_path = AStarSearch(maze)
maze.saveImage(filename="./dfs_astar_maze.png", path=solution_path)


# EXAMPLE 3: Load "dfs_maze.png" and now solve with A* search
#            Save as "loaded_dfs_astar_maze.png"
maze = Maze(filename="./dfs_maze.png")
solution_path = AStarSearch(maze)
maze.saveImage(filename="./loaded_dfs_astar_maze.png", path=solution_path)

