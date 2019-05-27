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
        self.WIDTH = 30
        self.HEIGHT = 40
        self.platform = random.randint(1, 6)
        if self.platform >= 1 and self.platform <= 3:
            self.posY = 210 # La posición Y desde el punto de arriba a la izquierda de la imagen
            if self.platform == 1:
                self.posX = random.randint(30, 170)
            elif self.platform == 2:
                self.posX = random.randint(350, 620)
            elif self.platform == 3:
                self.posX = random.randint(800, 940)
        if self.platform >= 4 and self.platform <= 5:
            self.posY = 435
            if self.platform == 4:
                self.posX = random.randint(30, 320)
            elif self.platform == 5:
                self.posX = random.randint(650, 940)
        if self.platform == 6:
            self.posY = 630
            self.posX = random.randint(30, 940)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.posX, self.posY, self.WIDTH, self.HEIGHT))