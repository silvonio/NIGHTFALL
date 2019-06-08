#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 18:21:31 2019

@author: Silvia Mena González y Antonio Muñoz Santiago

This is the main file
"""

import pygame, random

class player:
    def __init__(self, type, posX, posY, PLAYERDIMENSIONS):
        self.type = type # puede ser alien o humanoid
        self.WIDTH = PLAYERDIMENSIONS[0]
        self.HEIGHT = PLAYERDIMENSIONS[1]
        self.posX = posX
        self.posY = posY
        self.VELX = 15
        self.jumping = False # Para indicar cuando está saltando
        self.acJump = 0 # La aceleración del salto, se cambia su valor desde jump()
        if self.type == "alien":
            self.color = (0, 255, 0)
        else:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def move(self, WINDOW_WIDTH, WINDOW_HEIGHT, direction = None):
        if direction == 'left' and self.posX >= 30:
            self.posX -= self.VELX
        if direction == 'right' and (self.posX + self.WIDTH) <= (WINDOW_WIDTH-30):
            self.posX += self.VELX
        if self.jumping:
            print('estoy saltando :P')
            self.posY -= self.acJump
            self.acJump -= 0.4
            if self.acJump < 0:
                if self.posY >= (WINDOW_HEIGHT - 30 - self.HEIGHT) or (self.posY >= (475 - self.HEIGHT) and (self.posX >= 30 and self.posX <= (350 - self.WIDTH)) or (self.posX >= 650 and self.posX <= (WINDOW_WIDTH - 30 - self.WIDTH))):
                    self.jumping = False
                    print('puedes volver a saltar')

    def getPos(self):
        return [self.posX, self.posY]


    def jump(self):
        if self.jumping == False:
            print('quiero saltar :V')
            self.jumping = True
            self.acJump = 15


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.posX, self.posY, self.WIDTH, self.HEIGHT))