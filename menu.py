import pygame
from settings import *

class Menu:
    def __init__(self, player, toggleMenu):
        # config générale
        self.player = player
        self.toggleMenu = toggleMenu
        self.displaySurface = pygame.display.get_surface()
        self.font = pygame.font.Font("../font/lycheeSoda.ttf", 30) # font,size

        #options
        self.width = 400
        self.space = 10
        self.padding = 8

        # entries
        self.options = list(self.player.itemsInventory.keys()) + list(self.player.seedInventory.keys())
        self.selffOrder = len(self.player.itemInventory) -1
        self.setup()

    def setup(self):
        self.textSurfaces = []
        #dernier élément au 08/06
        self.totalHeight
        for item in self.options:
            textSurfaces = self.font.render(item, False, "Black")
            self.textSurfaces.append(textSurfaces)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.toggleMenu()
    def update(self):
        self.input()
        for textIndex,textSurface in enumerate(self.textSurfaces):
            self.displaySurface.blit(textSurface,(100, textIndex * 50))
