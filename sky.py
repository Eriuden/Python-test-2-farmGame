import pygame
from settings import *
from settings import LAYERS
from support import importFolder
from sprite import Generic
from random import randint
from random import choice

class Sky:
    def __init__(self):
        self.displaySurface = pygame.display.get_surface()
        self.fullSurf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.startColor = [255,255,255]
        self.endColor = (38,101,189)

    def display(self,dt):
        for index,value in enumerate(self.endColor):
            # si l'index de la couleur est sup à la value
            # on la réduit au fil du temps pour simuler la course du soleil
            if self.startColor[index] > value:
                self.startColor[index] -= 2 * dt 

        self.fullSurf.fill(self.startColor)
        self.displaySurface.blit(self.fullSurf, (0,0), special_flags= pygame.BLEND_RGBA_MULT)

class Drop(Generic):
    def __init__(self, pos, surf, groups, z, moving):
        super().__init__(pos, surf, groups, z, moving)
        self.lifetime = randint(400,500)
        self.startTime = pygame.time.get_ticks()

        self.moving = moving
        # si self moving est vrai, alors on crée une position
        # puis on lui donne une direction x et y et une vitesse
        # dans update, on mouvoie en ajoutant la self direction
        # elle même influencée par la vitesse et le temps
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2,4)
            self.speed = randint(200,250)
    def update(self,dt):
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # Si le chiffre de get ticks auquel on soutrait startime
        # est supérieur à la durée de vie qu'on a donné, ca disparait
        if pygame.time.get_ticks() - self.startTime >= self.lifetime:
            self.kill() 
        

class Rain:
    def __init__(self, allSprites):
        self.allSprites = allSprites
        self.raindDrops = importFolder("../graphics/rain/drops")
        self.rainFloor = importFolder("../graphics/rain/floor")
        self.floor_w, self.floor_h = pygame.image.load("..graphics/wolrd/ground.png").get_size()
    
    def createFloor(self):
        Drop(surf=choice (self.rainFloor),
            pos= (randint(0,self.floor_w), randint(0, self.floor_h)),
            moving= False, 
            groups = self.allSprites, 
            z= LAYERS['rain floor'])
    
    def createDrops(self):
        Drop(surf=choice (self.raindDrops),
            pos= (randint(0,self.floor_w), randint(0, self.floor_h)),
            moving= False, 
            groups = self.allSprites, 
            z= LAYERS['rain drops'])
        
    def update(self):
        self.createFloor()
        self.createDrops()