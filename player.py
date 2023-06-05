import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collisionSprites, treeSprites, interaction, soilLayer):
        super().__init__(group)

        self.importAssets()
        self.status = 'down'
        self.frameIndex = 0

        
        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.copy().inflate((-126,-70))
        self.z = LAYERS["main"]

        #Attribut mouvements
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        #collisions

        self.collisionSprites = collisionSprites

        self.timers = {
            "tool use": Timer(350,self.useTool),
            "tool switch" : Timer(200),
            "seed use": Timer(350,self.useSeeds),
            "seed switch" : Timer(200)
        }

        #Outils
        self.tools = ["hoe", "axe", "water"]
        self.toolIndex = 0
        self.selectedTools = self.tools[self.toolIndex]

        # graines
        self.seeds = ["corn", "tomato"]
        self.seedIndex = 0
        self.selectedSeed = self.seeds[self.seedIndex]
                        

        #inventaire
        self.itemInventory = {
            "wood": 0,
            "apple": 0,
            "corn": 0,
            "tomato": 0,
        }

        self.treeSprites = treeSprites
        self.interaction = interaction
        self.sleep = False
        self.soilLayer = soilLayer

    def useTool(self):
        if self.selectedTools == "hoe":
            self.soilLayer.getHit(self.targetPos)
        elif self.selectedTools == "axe" :
            for tree in self.treeSprites.sprites():
                if tree.rect.collidepoint(self.targetPos):
                    tree.damage()
        elif self.selectedTools == "water":
            self.soilLayer.water(self.targetPos)

    def getTargetPos(self):
        self.targetPos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split("_"[0])]

    def useSeeds(self):
        self.soilLayer.plantSeed(self.targetPos, self.selectedSeed)

    def importAssets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}
       
        for animation in self.animations.keys():
            fullPath = "./graphics/character/" + animation
            self.animations[animation] = importFolder(fullPath)

    def animate(self,datatime):
        self.frameIndex += 4 * datatime
        if self.frameIndex >= len(self.animations[self.status]):
            self.frameIndex = 0

        self.image = self.animations[self.status][int(self.frameIndex)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers["tool use"].active and not self.sleep:
            if keys[pygame.K_UP]:
                self.direction.y =-1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x =-1
                self.status = "left"
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            #Outils usage
            if keys[pygame.K_SPACE]:
                self.timers["tool use"].activate()
                self.direction = pygame.math.Vector2()
                self.frameIndex = 0
            # change outils
            if keys[pygame.K_a] and not self.timers["tool switch"].active:
                self.timers["tool switch"].activate()
                self.toolIndex +=1
                self.toolIndexIndex = self.toolIndex if self.toolIndex < len(self.tools) else 0    
                self.selectedTools = self.tools[self.toolIndex]

            # graine usage
            if keys[pygame.K_LCTRL]:
                self.timers["seed use"].activate()
                self.direction = pygame.math.Vector2()
                self.frameIndex = 0
                print("use seed")
            # change graine
            if keys[pygame.K_z] and not self.timers["seed switch"].active:
                self.timers["seed switch"].activate()
                self.seedIndex +=1
                self.seedIndex = self.seedIndex if self.seedIndex < len(self.seeds) else 0    
                self.selectedSeed = self.seeds[self.seedIndex]
                print(self.selectedSeed)

            if keys[pygame.K_RETURN]:
                collidedInteractionSprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collidedInteractionSprite:
                    if collidedInteractionSprite[0].name == "Trader":
                        pass 
                    else:
                        self.status = "left_idle"
                        self.sleep = True



    def getStatus(self):
        # Si immobile
        if self.direction.magnitude() == 0 :
            self.status = self.status.split("_")[0] + "_idle"
        # Si utilise un outil
        if self.timers["tool use"].active:
            self.status = self.status.split("_")[0] + "_" + self.selectedTools
            
    def updateTimers(self):
        for timer in self.timers.values():
            timer.update

    def collision(self,direction):
        for sprite in self.collisionSprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == "horizontal":
                        if self.direction.x > 0 :
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0 :
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == "vertical":
                        if self.direction.y > 0 :
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0 :
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self,datatime):
        if self.direction.magnitude() > 0 :
            self.direction = self.direction.normalize()

        # x mouvement
        self.pos.x += self.direction.x * self.speed * datatime
        self.hitbox.centerx = round(self.pos.x) 
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")
        # y mouvement
        self.pos.y += self.direction.y * self.speed * datatime
        self.hitbox.centery = round(self.pos.y) 
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def update(self, datatime):
        self.input()
        self.getStatus()
        self.updateTimers()
        self.move(datatime)
        self.animate(datatime)
        self.getTargetPos()

