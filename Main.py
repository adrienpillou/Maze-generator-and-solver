# Author : Adrien Pillou
# Created : 21/10/2020

# Maze Generator & A* Pathfinding

import numpy as np
import pygame
import sys
import os
from Grid import grid
from Cell import cell
import random
from Vector import vector2
from Color import colors
import math
from queue import PriorityQueue
from queue import Queue
from queue import LifoQueue

def create_board(): # Grid -> content -> cell
    for y in range(rows):
        for x in range(columns):
            board.content.append(cell(vector2(x, y), size = cell_width))


def draw_cells():
    for y in range(rows):
        for x in range(columns):
            cell = get_cell(x, y)
            cell.draw(screen)

def draw_borders():
    # Draw walls
    for y in range(rows):
        for x in range(columns):
            cell = get_cell(x, y)
            walls = [1, 1, 1, 1] # (up, down, left, right)
            for edge in cell.edges:
                # print(cell.id +" is connected to "+ edge.id)
                direction = edge.position - cell.position

                if(direction.x == 1):
                    walls[3] = 0
                elif(direction.x == -1):
                    walls[2] = 0
                if(direction.y == 1):
                    walls[1] = 0
                elif(direction.y == -1):
                    walls[0] = 0

            if(walls[0] == 1):
                # Above border
                start = (cell.position.x * cell_width, cell.position.y * cell_height)
                end = ((cell.position.x+1) * cell_width, cell.position.y * cell_height)
                pygame.draw.line(screen, colors().white, start, end, 1)
            if(walls[1] == 1):
                # Under border
                start = (cell.position.x * cell_width, (cell.position.y+1) * cell_height)
                end = ((cell.position.x+1) * cell_width, (cell.position.y+1) * cell_height)
                pygame.draw.line(screen, colors().white, start, end, 1)
            if(walls[2] == 1):
                # Left border
                start = (cell.position.x * cell_width, cell.position.y * cell_height)
                end = (cell.position.x * cell_width, (cell.position.y+1)*cell_height)
                pygame.draw.line(screen, colors().white, start, end, 1)
            if(walls[3] == 1):
                # Right border
                start = ((cell.position.x+1) * cell_width, cell.position.y * cell_height)
                end = ((cell.position.x+1) * cell_width, (cell.position.y+1) * cell_height)
                pygame.draw.line(screen, colors().white, start, end, 1)


def draw_path(path, color):
    if(len(path) == 0):
        return
    for index, location in enumerate(path):
        end = (location.x * cell_width + math.ceil(cell_width/2), location.y * cell_height + math.ceil(cell_height/2))
        pygame.draw.circle(screen, color, end, math.ceil(cell_width/8))
        if(index-1>=0):
            previous_location = path[index-1]
            start = (previous_location.x * cell_width + math.ceil(cell_width/2), previous_location.y * cell_height + math.ceil(cell_height/2))
            pygame.draw.line(screen, color, start, end, 1)
        
# Generate the maze
def generate_maze():
    number_of_cells = board.columns*board.rows
    start_position = vector2(0, 0)
    current_cell = get_cell(start_position.x, start_position.y)
    visited = set()
    stack = LifoQueue()

    while(len(visited)<number_of_cells):
        if(not current_cell in visited):
            visited.add(current_cell)
            stack.put(current_cell)
        
        neighboors = []
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                if(abs(j)!=abs(i)):
                    if(current_cell.position.x + i >= 0 and current_cell.position.x + i<board.columns):
                        if(current_cell.position.y + j >= 0 and current_cell.position.y + j < board.rows):
                            neighboor_cell = get_cell(current_cell.position.x + i, current_cell.position.y + j)
                            if(not neighboor_cell in visited):
                                neighboors.append(neighboor_cell)
        if(len(neighboors)!=0): # Pick a random neighboor
            picked_neighboor = neighboors[random.randint(0, len(neighboors)-1)]
            current_cell.edges.append(picked_neighboor)
            picked_neighboor.edges.append(current_cell)
            current_cell = picked_neighboor
        else: # Dead end
            current_cell = stack.get()
        pass

    del stack
    del visited

    get_cell(0,0).set_tag("START")
    get_cell(board.columns-1, board.rows-1).set_tag("END")

# Breadth first search
def breadth_first_search():
    opened_queue = Queue()
    start_node = get_cell_by_tag("START")
    if(start_node == None):
        return []
    opened_queue.put(start_node)
    closed_set = set()
    closed_set.add(start_node)
    
    current_node = start_node
    while(not opened_queue.empty()):
        current_node = opened_queue.get()
        if (current_node.tag == "END"):
            return build_path(current_node)
        for neighboor in current_node.edges:
            if(not neighboor in closed_set):
                neighboor.parent = current_node
                opened_queue.put(neighboor)
                closed_set.add(neighboor)
    print("No path found !")
                
def build_path(end_node):
    path = []
    while(end_node.parent!=None):
        path.append(end_node.position)
        end_node = end_node.parent
    path.append(end_node.position)
    path.reverse()
    return path

def manhattan_distance(vector_a, vector_b):
    distance = int(abs(vector_a.x - vector_b.x)+ abs(vector_a.y-vector_b.y))
    return distance

def get_cell(x, y):
    return board.content[y*board.columns + x]

def get_cell_by_tag(tag):
    for j in range(board.rows):
        for i in range(board.columns):
            current_cell = get_cell(i, j)
            if(current_cell.tag == tag):
                return current_cell
    return None

def get_grid_coords(mouse_position):
    (mouse_x, mouse_y) = mouse_position
    return (mouse_x//cell_width, mouse_y//cell_height)

def update():
    screen.fill(background_colour)
    draw_cells()
    draw_borders()
    draw_path(path, colors().green)
    pygame.display.update()

columns = 50
rows = 50
(width, height) = (1000, 1000)
cell_width = width//columns
cell_height = height//rows
os.environ['SDL_VIDEO_CENTERED'] = '1' # Centering the window on the screen (SDL flag ?)
background_colour = colors().black

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Maze Generator & Solver')
screen.fill(background_colour)

board = grid(rows, columns)
create_board()
end_cell = get_cell(board.columns-1, board.rows-1)
start_cell = get_cell(0,0)

generate_maze()

path =[]
inventory = []

running = True
while running:
    update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Mouse Inputs
        if pygame.mouse.get_pressed()[0]:
            mouse_position = pygame.mouse.get_pos()
            col, row = get_grid_coords(mouse_position)
            clicked_cell = get_cell(col, row)
            if(clicked_cell != None):
                if(clicked_cell.tag == "START"):
                    clicked_cell.set_tag("DEFAULT")
                    inventory.append("START")
                    
                elif(clicked_cell.tag == "END"):
                    clicked_cell.set_tag("DEFAULT")
                    inventory.append("END")
                    
        if pygame.mouse.get_pressed()[2]:
            mouse_position = pygame.mouse.get_pos()
            col, row = get_grid_coords(mouse_position)
            clicked_cell = get_cell(col, row)
            if(clicked_cell.tag == "DEFAULT" and len(inventory)>0):
                clicked_cell.set_tag(inventory.pop())
                
        
        # Keyboard Inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                path = []
                start_cell = get_cell_by_tag("START")
                end_cell = get_cell_by_tag("END")
                print(start_cell.id)
                if(end_cell == None or start_cell == None):
                    break
                else:
                    print("Searching the path...")
                    path = breadth_first_search()
                    print(f"Path found ! length = {len(path)}")

            if event.key == pygame.K_c:
                board = grid(rows, columns)
                create_board()
                generate_maze()
                path = []
                print("Generating a new maze !")
    
    
    
    


