import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprite import Generic, Water, WildFolwer, Tree, Interaction
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer


class Level:
    
    def __init__(self):

        # obtenir la surface d'affichage
        self.display_surface = pygame.display.get_surface()

        #Groupes de sprites
        self.all_sprites = Camera()
        self.collisionSprites = pygame.sprite.Group()
        self.treeSprites = pygame.sprite.Group()
        self.interactionSprites = pygame.sprite.Group()
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)
        self.soilLayer = SoilLayer(self.all_sprites)
        
        
    def setup(self):

        tmxData =load_pygame("./data/map.tmx")

        # maison

        for layer in ["houseFloor", "houseFurnitureBottom"]:
            for x, y, surface in tmxData.get_layer_by_name("HouseFurnitureBottom").tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE),surface,self.all_sprites,LAYERS["house bottom"])
        
        for layer in ["houseWall", "houseFurnitureTop"]:
            for x, y, surface in tmxData.get_layer_by_name("HouseFurnitureBottom").tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE),surface,self.all_sprites)        

        # barrières
        
        for x, y ,surf in tmxData.get_layer_by_name("Fence").tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE),surf, [self.all_sprites, self.collisionSprites])

        # eau arbres et fleurs
        waterFrames = importFolder("./graphics/layer")
        for x, y ,surf in tmxData.get_layer_by_name("Water").tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE),waterFrames, self.all_sprites)

        for obj in tmxData.get_layer_by_name("Decoration"):
            WildFolwer((obj.x, obj.y), obj.image, [self.all_sprites, self.collisionSprites])

        for obj in tmxData.get_layer_by_name("Trees"):
            Tree((obj.x,obj.y),
                  obj.image,
                  [self.all_sprites ,self.collisionSprites, self.treeSprites, self.collisionSprites],
                  obj.name,
                  self.playerAdd)

        # collisions tiles
        for x, y, surf in tmxData.get_layer_by_name("Collision").tiles():
            Generic((x * TILE_SIZE,y * TILE_SIZE), pygame.Surface(TILE_SIZE,TILE_SIZE), self.collisionSprites)

        # Player
        for obj in tmxData.get_layer_by_name("Player"):
            if obj.name =="Start":
                self.player = Player(
                pos = (obj.x, obj.y),
                group = self.all_sprites,
                collisionSprites= self.collisionSprites,
                trees = self.treeSprites,
                Interaction = self.interactionSprites)
                SoilLayer = self.soilLayer
            if obj.name == "Bed" :
                Interaction((obj.x,obj.y), (obj.width, obj.height),self.interactionSprites, obj.name )


        self.player = Player((640,360), self.all_sprites, self.collisionSprites)
        Generic(
            pos = (0,0),
            surf = pygame.image.load("./graphics/world/ground.png").convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS["ground"]
        )
        
    def playerAdd(self,item):
        self.player.itemInventory[item] += 1
 
    def reset(self):

        self.soilLayer.removeWater()

        for tree in self.treeSprites.sprites():
            for apple in tree.appleSprites.sprites():
                apple.kill()    
            tree.createFruit()

    def run(self,datatime):
        self.display_surface.fill("black")
        self.all_sprites.customDraw(self.player)
        self.all_sprites.update(datatime)

        self.overlay.display()

        if self.player.sleep:
            self.transition.play(datatime)
        

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

# itération de chaque valeur dans le tableau LAYERS
    #itération de chaque sprites
        # si le sprite correspond au positionnement du layer
            # on le dessine

    def customDraw(self, player):

        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key =lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offsetRect = sprite.rect.copy()
                    offsetRect.center -= self.offset
                    self.displaySurface.blit(sprite.image, offsetRect)
