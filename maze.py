# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 22:16:50 2022

Author: Adam Moyle
"""
from PIL import Image, ImageDraw

#--- Maze class ---#
class Maze:
    def __init__(self, size=[10, 10], filename=""):
        # If filename is provided load from image
        if filename != "": self.fromImage(filename)
        else:
            self.size = size
            self.walls = [[[1, 1, 1, 1] for y in range(self.size[1])] for x in range(self.size[0])]
            self.generated = False    
    
    #--- Function to check if moving from one cell to another is valid ---#
    def isValidMove(self, pos1: list, pos2: list) -> bool:
        dx, dy = pos2[0] - pos1[0], pos2[1] - pos1[1]

        if dx == 1:
            valid = self.walls[pos1[0]][pos1[1]][1] == 0 and self.walls[pos2[0]][pos2[1]][3] == 0
        elif dx == -1:
            valid = self.walls[pos1[0]][pos1[1]][3] == 0 and self.walls[pos2[0]][pos2[1]][1] == 0
        elif dy == 1:
            valid = self.walls[pos1[0]][pos1[1]][2] == 0 and self.walls[pos2[0]][pos2[1]][0] == 0
        else:
            valid = self.walls[pos1[0]][pos1[1]][0] == 0 and self.walls[pos2[0]][pos2[1]][2] == 0
        
        return valid
    
    #--- Function to check if a given position is within the maze bounds ---#
    def isValidPos(self, pos: list) -> bool:
        if pos[0] < 0 or pos[0] >= self.size[0]: return False
        if pos[1] < 0 or pos[1] >= self.size[1]: return False
        return True
    
    #--- Function to get the neighbours of a current cell ---#
    #--- NOTE: DOES NOT CHECK IF THESE ARE VALID POSITIONS ---#
    def getNeighbours(self, pos: list) -> list:
        return [[pos[0], pos[1] + 1], [pos[0] + 1, pos[1]],
                [pos[0], pos[1] - 1], [pos[0] - 1, pos[1]]]
    
    #--- Save image to file with optional solution path ---#
    def saveImage(self, path=False, filename="./maze.png"):
        image = Image.new("RGB", (self.size[0] * 3, self.size[1] * 3))
        pixels = image.load()
        
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                pos = (1 + 3*x, 1 + 3*y)
                
                pixels[pos[0], pos[1]] = (255, 255, 255)
                
                if not self.walls[x][y][0]: pixels[pos[0], pos[1] - 1] = (255, 255, 255)
                if not self.walls[x][y][1]: pixels[pos[0] + 1, pos[1]] = (255, 255, 255)
                if not self.walls[x][y][2]: pixels[pos[0], pos[1] + 1] = (255, 255, 255)
                if not self.walls[x][y][3]: pixels[pos[0] - 1, pos[1]] = (255, 255, 255)        
        
        # Draw a solution path if provided
        if path:
            for i in range(len(path)):
                x, y = path[i]
                pos = (1 + 3*x, 1 + 3*y)
                
                pixels[pos[0], pos[1]] = (0, 255, 0)
                
                # Fill pixel between the two cells
                if i != len(path) - 1: 
                    next_x, next_y = path[i + 1]
                    dx, dy = next_x - x, next_y - y
                    
                    pixels[pos[0] + dx, pos[1] + dy] = (0, 255, 0)
                    pixels[pos[0] + 2*dx, pos[1] + 2*dy] = (0, 255, 0)
            
        # Save image as PNG
        image.save(filename, "PNG")
        
    #--- Function to initiate a maze from a image with correct format ---#
    def fromImage(self, filename:str):
        image = Image.open(filename)
        pixels = image.load()
        
        # Get width and height of image and convert to maze size
        width, height = image.size
        mWidth, mHeight = int(width/3), int(height/3)
        
        self.size = [mWidth, mHeight]
        self.walls = [[[1, 1, 1, 1] for y in range(self.size[1])] for x in range(self.size[0])]
        self.generated = True
        
        # Iterate over the image
        for x in range(mWidth):
            for y in range(mHeight):
                pos = (1 + 3*x, 1 + 3*y)
                
                # Check walls
                w1 = (pixels[pos[0], pos[1] - 1] == (255, 255, 255)
                     or pixels[pos[0], pos[1] - 1] == (0, 255, 0))
                w2 = (pixels[pos[0] + 1, pos[1]] == (255, 255, 255)
                     or pixels[pos[0] + 1, pos[1]] == (0, 255, 0))
                w3 = (pixels[pos[0], pos[1] + 1] == (255, 255, 255)
                     or pixels[pos[0], pos[1] + 1] == (0, 255, 0))
                w4 = (pixels[pos[0] - 1, pos[1]] == (255, 255, 255)
                     or pixels[pos[0] - 1, pos[1]] == (0, 255, 0))
                
                # Remove walls if applicable
                if w1: self.walls[x][y][0] = 0
                if w2: self.walls[x][y][1] = 0
                if w3: self.walls[x][y][2] = 0
                if w4: self.walls[x][y][3] = 0