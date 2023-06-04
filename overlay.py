import pygame
from settings import *


class Overlay:
    def __init__(self, player):
        self.displaySurface = pygame.display.get_surface()
        self.player = player 

        OverlayPath = "./graphics/overlay/"
        self.toolSurf = {tool:pygame.image.load(f"{OverlayPath}{tool}.png").convert_alpha() for tool in player.tools}
        self.seedSurf = {seed:pygame.image.load(f"{OverlayPath}{seed}.png").convert_alpha() for seed in player.seeds}
        

    def display(self):

        #tool
        toolSurface = self.toolSurf[self.player.selectedTools]
        toolRect = toolSurface.get_rect(midbottom = OVERLAY_POSITIONS["tool"])
        self.displaySurface.blit(toolSurface,toolRect)
        #seed
        seedSurface = self.seedSurf[self.player.selectedSeed]
        seedRect = seedSurface.get_rect(midbottom = OVERLAY_POSITIONS["seed"])
        self.displaySurface.blit(seedSurface,seedRect)

    