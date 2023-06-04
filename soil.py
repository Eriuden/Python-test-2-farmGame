import pygame
from pygame.sprite import _Group
from settings import *
from pytmx.util_pygame import load_pygame
from support import *
from random import choice

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super.__init__(groups)
        self.image = surface
        self.rect = self.image.getRect(topleft = position)
        self.z = LAYERS["soil"]

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS["soil water"]
class SoilLayer:
    def __init__(self, allSprites):
        
        self.allSprites = allSprites
        self.soilSprite = pygame.sprite.Group()
        self.waterSprite = pygame.sprite.Group()

        self.soilSurface = pygame.image.load("./graphics/soil/o.png")
        self.soilSurfaces =  importFolderDict("./graphics/soil")
        self.water_surfs = importFolder("../graphics/soil_water")

        self.createSoilGrid()
        self.createHitRects()

    def createSoilGrid(self):
        ground = pygame.image.load("./graphics/world/ground.png")

        #Particularité à regarder de près
        #On peux déclarer deux variables côte à côte
        #Juste séparer et leur noms, et leur valeurs par une virgule
        #Cependant c'est assez peu lisible, je pense pas refaire souvent
        hTiles, vTiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE
        self.grid = [[[] for col in range(hTiles)] for row in range(vTiles)]
        for x, y, surf in load_pygame("./data/map.tmx").get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append("F")
        
    def createHitRects(self):
        self.hitRect = []
        for indexRow,row in enumerate(self.grid):
            for indexCol,cell in enumerate(row):
                if "F" in cell:
                    x = indexCol * TILE_SIZE
                    y = indexRow * TILE_SIZE
                    rect = pygame.rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hitRect.append(rect)

    def getHit(self,point):
        for rect in self.hitRect:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if "F" in self.grid[y][x]:
                    self.grid[y][x].append("X")
                    self.createSoilTiles()

    def water(self, targetPos):
        for soilSprites in self.soilSprite.sprites():
            if soilSprites.rect.collidepoint(targetPos):
                x = soilSprites.rect.x  
                y = soilSprites.rect.y 
                self.grid[y][x].append("W")

                pos = soilSprites.rect.topleft
                surf = choice(self.water_surfs)

                WaterTile(pos, surf, [ self.allSprites, self.waterSprite])

    def removeWater(self):
        for sprite in self.waterSprite.sprites():
            sprite.kill()
        for row in self.grid:
            for cell in row:
                if "W" in cell:
                    cell.remove("W")

    def createSoilTiles(self):
        self.soilSprite.empty()
        for indexRow,row in enumerate(self.grid):
            for indexCol,cell in enumerate(row):
                if "X" in cell:

                    t = "X" in self.grid[indexRow - 1][indexCol]
                    b = "X" in self.grid[indexRow + 1][indexCol]
                    r = "X" in row [indexCol + 1 ]
                    l = "X" in row [indexCol - 1 ]

                    tyleType = "o"

                    #toutes directions
                    if all((t,r,b,l)): tyleType = "x"

                    # horizontal

                    if l and not any((t,r,b)): tyleType = "r"
                    if r and not any((t,l,b)): tyleType = "l"
                    if r and l and not any((t,b)): tyleType = "lr"

                    #vertical

                    if b and not any((t,r,l)): tyleType = "t"
                    if t and not any((l,r,b)): tyleType = "b"
                    if b and t and not any((l,r)): tyleType = "tb"

                    #coins

                    if l and b and not any((r,t)): tyleType = "tr"
                    if r and t and not any((t,l)): tyleType = "tl"
                    if l and t and not any((r,b)): tyleType = "br"
                    if r and t and not any((b,l)): tyleType = "bl"

                    # formes en T

                    if all((t,b,r)) and not l: tyleType = "tbr"
                    if all((t,b,l)) and not r: tyleType = "tbl"
                    if all((t,l,r)) and not b: tyleType = "lrb"
                    if all((l,b,r)) and not t: tyleType = "lrt"



                    SoilTile(pos=(indexCol* TILE_SIZE, indexRow* TILE_SIZE), 
                    surf =self.soilSurface[tyleType] , 
                    groups=[self.allSprites, self.soilSprite])


