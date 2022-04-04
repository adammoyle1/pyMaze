# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 22:38:27 2022

@author: Adam Moyle
"""
from queue import PriorityQueue
from random import choice
from maze import Maze

#--- Function to generate a maze using a iterative depth first search algorithm ---#
#--- Note acts inplace upon the mazer object ---#
def depthFirstSearch(maze: Maze, bias=[0, 0], printInfo=False) -> bool:
    if maze.generated: return False
    
    print("GENERATING {}x{} MAZE USING DEPTH FIRST SEARCH".format(*maze.size))
    
    # Check if we wish to bias a certain direction
    if bias != [0, 0]: biased = True
    else: biased = False
    
    # Create arrays tracking visited cells and stack
    visited = [[0 for y in range(maze.size[1])] for x in range(maze.size[0])]
    stack = []
    
    # Set inital position and mark as visited
    pos = [0, 0]
    visited[pos[0]][pos[1]] = 1
    stack.append(pos)
    
    # Keep track of how much has been completed
    n = 0
    total_n = maze.size[0] * maze.size[1]
    
    while len(stack):
        pos = stack.pop()
        
        # Get all neighbours and remove an visited ones
        nn = maze.getNeighbours(pos)
        nn = [n for n in nn if maze.isValidPos(n)]
        unvisited_nn = [n for n in nn if not visited[n[0]][n[1]]]
        
        if len(unvisited_nn):
            
            # If we have biased, check if we can move in that direction
            if biased:
                found = False
                dd = [[n[0] - pos[0], n[1] - pos[1]] for n in unvisited_nn]
                for i in range(len(dd)):
                    if dd[i] == bias:
                        next_pos = unvisited_nn[i]
                        found = True
                        break
                
                # If we cant just choose a random next_pos
                if not found: next_pos = choice(unvisited_nn)
            else:
                # Randomly choose a cell to be the next cell
                next_pos = choice(unvisited_nn)
                
            # Find direction between next and current pos
            dx, dy = next_pos[0] - pos[0], next_pos[1] - pos[1]
            
            # Remove corresponding walls
            if dx == 1: 
                maze.walls[pos[0]][pos[1]][1] = 0
                maze.walls[next_pos[0]][next_pos[1]][3] = 0
            elif dx == -1: 
                maze.walls[pos[0]][pos[1]][3] = 0
                maze.walls[next_pos[0]][next_pos[1]][1] = 0
            elif dy == 1: 
                maze.walls[pos[0]][pos[1]][2] = 0
                maze.walls[next_pos[0]][next_pos[1]][0] = 0
            else: 
                maze.walls[pos[0]][pos[1]][0] = 0
                maze.walls[next_pos[0]][next_pos[1]][2] = 0
            
            # Push to the stack and mark next_pos as visited
            stack.append(pos)
            stack.append(next_pos)
            
            visited[next_pos[0]][next_pos[1]] = 1
            
            n += 1
            
            if printInfo and n % int(total_n/10) == 0:
                print("{:.2f}% completed".format(n/total_n*100))
    
    print("COMPLETED GENERATION")
    maze.generated = True
    return True
        
#--- Function to solve a maze using depth first search ---#
def depthFirstSearchSolver(maze: Maze, end=[0, 0]) -> list:
    if not maze.generated: return False
    
    if end == [0, 0]: end = [maze.size[0] - 1, maze.size[1] - 1]
        
    # Create arrays tracking visited cells and stack
    visited = [[0 for y in range(maze.size[1])] for x in range(maze.size[0])]
    stack = []
    
    # Set inital position and mark as visited
    pos = [0, 0]
    visited[pos[0]][pos[1]] = 1
    stack.append(pos)
    
    while pos[0] != end[0] or pos[1] != end[1]:
        pos = stack.pop()
        
        # Get neighbours and check they can be moved to/havent been visited
        nn = maze.getNeighbours(pos)
        nn = [n for n in nn if maze.isValidMove(pos, n) and visited[n[0]][n[1]] == 0]
        
        if len(nn):
            next_pos = choice(nn)
            
            visited[next_pos[0]][next_pos[1]] = 1
            
            stack.append(pos)
            stack.append(next_pos)
            
    #stack.append(end)
    
    return stack
    
#--- Function to calculate squared distance between two points ---#
#--- Used for heuristic estimate in A* search ---#
def distSquared(p1, p2):
    return pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2)

#--- Function to reconstruct the shortest path from a given hashmap ---#
def reconstructPath(cameFrom: dict, current: tuple) -> list:
    path = []
    
    while current != (0, 0):
        path.append(current)
        current = cameFrom[current]
    
    path.append(current)
    
    return path

#--- Function implementing A* search using a priority queue ---#
def AStarSearch(maze:Maze, end=(0, 0)) -> list:
    if end == (0, 0): end = (maze.size[0] - 1, maze.size[1] - 1)
    if type(end) != tuple: end = tuple(end)
    
    # Make use of priority queue
    q = PriorityQueue()
    
    # Put the current position into the queue
    current = (0, 0)
    q.put((0, current))
    
    # Hashmap of where each cell came from
    cameFrom = {}
    
    # Hashmap for scores
    gscore = {}
    gscore[current] = 0
    
    while q.qsize():
        current_fscore, current = q.get()
        
        # If we find the end position, reconstruct the best path
        if current == end:
            return reconstructPath(cameFrom, current)
        
        # Get possible neighbours and convert to tuple to allow hashing
        nn = maze.getNeighbours(current)
        nn = [n for n in nn if maze.isValidMove(current, n)]
        nn = [(n[0], n[1]) for n in nn]
        
        # For each neighbour calculate the gscore and check if we found a new minimum
        for n in nn:
            tentative_gscore = gscore[current] + distSquared(current, n)
            
            # If we havent seen it before, set to a really large number
            if n in gscore.keys(): n_gscore = gscore[n]
            else: n_gscore = float("inf")
            
            if tentative_gscore < n_gscore:
                cameFrom[n] = current
                gscore[n] = tentative_gscore
                
                q.put((tentative_gscore + distSquared(n, end), n))
                
    # If we fail return a empty list
    return []
    
    