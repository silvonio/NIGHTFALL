#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 18:21:31 2019

@author: Silvia Mena González y Antonio Muñoz Santiago

This is the main file
"""

import pygame, random

class player:
    def __init__(self, type, posX, posY):
        self.type = type # puede ser alien o humanoid
        self.WIDTH = 70
        self.HEIGHT = 100
        self.posX = posX
        self.posY = posY
        self.VELX = 15
        self.jumping = False # Para indicar cuando está saltando
        self.acJump = 15 # La aceleración del salto

    def move(self, WINDOW_WIDTH, WINDOW_HEIGHT, direction = None):
        if direction == 'left' and self.posX >= 30:
            self.posX -= self.VELX
        if direction == 'right' and (self.posX + self.WIDTH) <= (WINDOW_WIDTH-30):
            self.posX += self.VELX
        if self.jumping:
            print('estoy saltando :P')
            self.posY -= self.acJump
            self.acJump -= 0.4
            if self.acJump < 0 and self.posY >= (WINDOW_HEIGHT - 30 - self.HEIGHT):
                self.jumping = False
                print('puedes volver a saltar')


    def jump(self):
        if self.jumping == False:
            print('quiero saltar :V')
            self.jumping = True
            self.acJump = 15


    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(self.posX, self.posY, self.WIDTH, self.HEIGHT))