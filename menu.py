import pygame
from settings import *
from timer import Timer

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
        self.sellBorder = len(self.player.itemInventory) -1
        self.setup()

        #Mouvement
        self.index = 0
        self.timer = Timer(200)

    def displayMoney(self):
        #l'indicateur d'argent
        textSurf = self.font.render(f'{self.player.money}G', False, "Black")
        textRect = textSurf.get_rect(topright= (SCREEN_WIDTH /2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.displaySurface, "White", textRect.inflate(10,10),0,6)
        self.displaySurface.blit(textSurf, textRect)

    def setup(self):
        self.textSurfaces = []
        self.totalHeight = 0

        for item in self.options:
            textSurfaces = self.font.render(item, False, "Black")
            self.textSurfaces.append(textSurfaces)
            self.totalHeight += textSurfaces.get_height()+ (self.padding * 2)
        
        self.totalHeight += (len(self.textSurfaces) - 1) * self.space 
        self.menu_top = SCREEN_HEIGHT / 2 - self.totalHeight / 2
        self.mainRect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2 ,self.menu_top,self.width,self.totalHeight)

        # texte achat ventes
        self.buyText = pygame.font.render("buy",False,"Black")
        self.sellText = pygame.font.render("sell",False,"Black")

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggleMenu()

        if not self.timer.activate:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                currentItem = self.options[self.index]

                #sell
                if self.index <= self.sellBorder:
                    if self.player.itemInventory[currentItem] > 0:
                        self.player.itemInventory[currentItem] -= 1
                        self.player.money += SALE_PRICES[currentItem]


                #buy
                else:
                    seedPrice = PURCHASE_PRICES[currentItem]
                    if self.player.money >= seedPrice:
                        self.player.seedInventory[currentItem] +=1
                        self.player.money -= seedPrice

            if self.index < 0:
                self.index = len(self.options) - 1
            if self.index > len(self.options):
                self.index = 0

    def showEntries(self, textSurface, amount, top, selected):
        # background
        bgRect= pygame.Rect(self.mainRect.left,top,self.width, textSurface.get_height() + (self.padding * 2))
        pygame.draw.rect(self.displaySurface, "White", bgRect, 0, 4)

        # texte
        textRect = textSurface.get_rect(midleft = (self.mainRect.left + 20, bgRect.centery))
        self.displaySurface.blit(textSurface,textRect)

        # montant
        amountSurface = self.font.render(amount, False, "Black")
        amountRect = amountSurface.get_rect(midright = (self.mainRect.right - 20, bgRect.centery))
        self.displaySurface.blit(amountSurface, amountRect)

        #selected
        if selected:
            pygame.draw.rect(self.displaySurface, "black", bgRect, 4,4)
            if self.index <= self.sellBorder: #vente
                positionRect = self.sellText.get_Rect(midleft = (self.mainRect.left + 150, bgRect.centery))
                self.displaySurface.blit(self.sellText, (self.sellText,positionRect))

            else: #achat
                positionRect = self.buyText.get_Rect(midleft = (self.mainRect.left + 150, bgRect.centery))
                self.displaySurface.blit(self.buyText, (self.buyText,positionRect))

    def update(self):
        self.input()
        self.displayMoney()
        
        for textIndex,textSurface in enumerate(self.textSurfaces):
            top = self.mainRect.top + textIndex * (textSurface.get_height() + (self.padding * 2) + self.space)
            amountList = list(self.player.itemsInventory.values()) + list(self.player.seedInventory.values())
            amount = amountList[textIndex]
            self.showEntries(textSurface, amount, top, self.index == textIndex)
            
