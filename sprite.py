import pygame
from settings import *
from random import randint, choice
from timer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self,pos, surf, groups, z = LAYERS["main"]):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect( topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name
class Water(Generic):
    def __init__(self, pos, frames, groups):
        
        self.frames = frames
        self.frameIndex = 0

        super().__init__(pos = pos,
            surf = self.frames[self.frameIndex], 
            groups = groups
            , z = LAYERS["water"])

    def animate(self, datatime):
         self.frameIndex += 4 * datatime
         if self.frameIndex >= len(self.frames):
            self.frameIndex = 0

            self.image = self.frames(int(self.frameIndex))

    def update(self, datatime):
        self.animate(datatime)

class WildFolwer(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbbox = self.rect.copy().inflate(-20,-self.rect.height *0.9)

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        maskSurf = pygame.mask.from_surface(self.image)
        newSurf = maskSurf.to_surface()
        newSurf.set_colorkey((0,0,0))
        self.image = newSurf


    def update(self,datatime):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.start_time > self.duration:
            self.kill()


class Tree(Generic):
    def __init__(self, pos, surf, groups, name, playerAdd):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

        #attrib arbres
        self.health = 5
        self.alive = True
        self.stumpSurf = pygame.image.load(f"./graphics/stump/{'small' if name =='small' else 'large'}.png").convert_alpha()
        self.invulFrame = Timer(200)
        
        #Pommes
        self.applesSurf = pygame.image.load("./graphics/fruit/apple.png")
        self.applesPos = APPLE_POS[name]
        self.appleSprites = pygame.sprite.Group()
        self.createFruit()

        self.playerAdd = playerAdd

    def damage(self):
        #dommages aux arbres
        self.health -=1

        if len(self.appleSprites.sprites()) > 0:
            randomApple = choice(self.appleSprites.sprites)
            Particle(pos = randomApple.rect.topleft
            , surf = randomApple.image,
            groups = self.groups()[0],
            z = LAYERS["fruit"])

            self.playerAdd("apple")
            randomApple.kill()

    def checkDeath(self):
        if self.health <=0:
            Particle(self.rect.topleft
            , self.image,
            self.groups()[0],
            LAYERS["fruit"],
            500)

            self.image = self.stumpSurf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10,-self.rect.height*0.6)
            self.alive = False
            self.playerAdd("wood")
        

    def update(self,datatime):
        if self.alive:
            self.checkDeath()

    def createFruit(self):
        for pos in self.applesPos:
            if randint(0,10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(pos = (x, y),
                surf = self.appleSurf,
                groups = [self.appleSprites, self.groups()[0]],
                z = LAYERS["fruit"])

            