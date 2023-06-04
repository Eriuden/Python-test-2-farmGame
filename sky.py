import pygame
from settings import *
from settings import LAYERS
from support import importFolder
from sprite import Generic
from random import randint

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
        Drop()
    
    def createDrops(self):
        Drop()
    def update(self):
        self.createFloor()
        self.createDrops()