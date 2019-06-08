#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 18:21:31 2019

@author: Silvia Mena González y Antonio Muñoz Santiago

This is the main file
"""

import pygame, random

class egg:
    def __init__(self):
        self.WIDTH = 50
        self.HEIGHT = 65
        self.platform = random.randint(1, 6)
        self.delete = False # Para saber si se debe eliminar el huevo
        self.imageList = [[
            pygame.image.load("assets/images/egg/egg1.png"),
            pygame.image.load("assets/images/egg/egg2.png"),
            pygame.image.load("assets/images/egg/egg3.png")
        ], [
            pygame.image.load("assets/images/egg/egg1bomb.png"),
            pygame.image.load("assets/images/egg/egg2bomb.png"),
            pygame.image.load("assets/images/egg/egg3bomb.png")
        ]]
        self.imageToDraw = self.imageList[0][random.randint(0, 2)]

        if self.platform >= 1 and self.platform <= 3:
            self.posY = 200 # La posición Y desde el punto de arriba a la izquierda de la imagen
            if self.platform == 1:
                self.posX = random.randint(30, 155)
            elif self.platform == 2:
                self.posX = random.randint(350, 605)
            elif self.platform == 3:
                self.posX = random.randint(800, 925)
        if self.platform >= 4 and self.platform <= 5:
            self.posY = 425
            if self.platform == 4:
                self.posX = random.randint(30, 305)
            elif self.platform == 5:
                self.posX = random.randint(650, 925)
        if self.platform == 6:
            self.posY = 620
            self.posX = random.randint(30, 940)

    def checkPosition(self, playerPos, PLAYERDIMENSIONS):
        if ((playerPos[0][0] > self.posX and playerPos[0][0] < (self.posX + self.WIDTH))\
                or ((playerPos[0][0] + PLAYERDIMENSIONS[0]) > self.posX and (playerPos[0][0] + PLAYERDIMENSIONS[0]) < (self.posX + self.WIDTH)))\
                and (self.posY > playerPos[0][1] and self.posY < (playerPos[0][1] + PLAYERDIMENSIONS[1])):
            return 'alien'
        if ((playerPos[1][0] > self.posX and playerPos[1][0] < (self.posX + self.WIDTH))\
                or ((playerPos[1][0] + PLAYERDIMENSIONS[0]) > self.posX and (playerPos[1][0] + PLAYERDIMENSIONS[0]) < (self.posX + self.WIDTH)))\
                and (self.posY > playerPos[1][1] and self.posY < (playerPos[1][1] + PLAYERDIMENSIONS[1])):
            return 'humanoid'

    def draw(self, surface):
        #pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.posX, self.posY, self.WIDTH, self.HEIGHT))
        surface.blit(self.imageToDraw, (self.posX, self.posY))