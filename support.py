from os import walk 
import pygame


def importFolder(path):
    surfaceList = []

    for _, __, imgFile in walk(path):
        for image in imgFile:
            fullPath =  path + "/" + image
            imageSurface = pygame.image.load(fullPath).convert_alpha()
            surfaceList.append(imageSurface)

    return surfaceList

def importFolderDict(path):
    surfaceDict = {}

    for _, __, imgFile in walk(path):
        for image in imgFile:
            fullPath =  path + "/" + image
            imageSurface = pygame.image.load(fullPath).convert_alpha()
            surfaceDict[image.split("."[0])] = imageSurface
        return surfaceDict

        
