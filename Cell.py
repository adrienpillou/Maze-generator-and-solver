from Vector import vector2
import pygame
from Color import colors

class cell:
    def __init__(self, position=vector2().zero(), color = (255, 255, 255),  size = 32, tag = "DEFAULT"):
        self.position = position
        self.color = color
        self.size = size
        self.tag = tag
        self.id = f"{self.position.x}:{self.position.y}"
        self.edges = []
        self.parent = None

    def set_tag(self, new_tag):
        self.tag = new_tag

    def draw(self, window):
        if(self.tag=="DEFAULT"):
            cell_color = colors().black
        elif(self.tag == "END"):
            cell_color = colors().red
        elif(self.tag == "START"):
            cell_color = colors().blue
        elif(self.tag == "CLOSED"):
            cell_color = colors().orange
        elif(self.tag == "OPENED"):
            cell_color = colors().blue_green
        elif(self.tag == "PATH"):
            cell_color =colors().green
        world_position = vector2(self.position.x*self.size, self.position.y*self.size)
        pygame.draw.rect(window, cell_color, (world_position.x, world_position.y, self.size, self.size))