#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 18:21:31 2019

@author: Silvia Mena González y Antonio Muñoz Santiago

This is an object file
"""

import pygame, random

class player:
    def __init__(self, type, posX, posY, PLAYERDIMENSIONS, STAGESIZES, GAME_TIME):
        self.type = type # puede ser alien o humanoid
        self.GAME_TIME = GAME_TIME
        self.WIDTH = PLAYERDIMENSIONS[0]
        self.HEIGHT = PLAYERDIMENSIONS[1]
        self.STAGESIZES = STAGESIZES
        self.GRAVITY = 0.4 # Lo que se le resta a posY
        self.CHARGETIME = 3000 # Tiempo mínimo entre cada disparo
        self.TIMEPARALYZED = 5000 # Tiempo que el jugador permanecerá paralizado
        self.posX = posX
        self.posY = posY
        self.VELX = 15
        self.jumping = False # Para indicar cuando está saltando
        self.acJump = 0 # La aceleración del salto, se cambia su valor desde jump()
        self.overPlatform = False
        self.bullet = [] # Lista con las balas existentes
        self.shooting = False # Variable para indicar si está disparando
        self.shootTime = 0 # El instante del último disparo
        self.paralyzed = False # Si el jugador está paralizado
        self.paralysisInstant = None # Para almacenar el instante cuando el jugador queda paralizado
        self.attacking = False # Para saber cuando ha dañado al otro jugador
        if self.type == "alien":
            self.color = (0, 255, 0)
            self.direction = 'right' # La dirección a la que apunta
        else:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.direction = 'left'
        self.bulletImage = pygame.image.load("assets/images/player/bullet/bullet.png")
    def move(self, WINDOW_WIDTH, WINDOW_HEIGHT, direction = None):
        if direction == 'left' and self.posX >= 30 and not self.paralyzed:
            self.posX -= self.VELX
            self.direction = 'left'
        if direction == 'right' and (self.posX + self.WIDTH) <= (WINDOW_WIDTH-30) and not self.paralyzed:
            self.posX += self.VELX
            self.direction = 'right'
        if not self.overPlatform and not self.jumping and self.posY < (self.STAGESIZES[2][1] - self.HEIGHT):
            self.acJump -= self.GRAVITY
            self.posY -= self.acJump
        elif not self.jumping:
            self.acJump = 0
            self.posY = self.STAGESIZES[2][1] - self.HEIGHT
            self.overPlatform = True

        elif self.jumping :
            self.acJump -= self.GRAVITY
            self.posY -= self.acJump
            #self.posY -= self.acJump
            #self.acJump -= self.GRAVITY
            if self.acJump < 0:
            #    if self.posY >= (WINDOW_HEIGHT - 30 - self.HEIGHT) or (self.posY >= (475 - self.HEIGHT) and (self.posX >= 30 and self.posX <= (350 - self.WIDTH)) or (self.posX >= 650 and self.posX <= (WINDOW_WIDTH - 30 - self.WIDTH))):
                self.jumping = False
            #   print('puedes volver a saltar')

        # DISPARO
        if self.shooting:
            print(self.direction)
            self.bullet.append([self.posX + (self.WIDTH / 2), self.posY + (self.HEIGHT / 2), self.direction])
            self.shooting = False
            self.shootTime = self.GAME_TIME.get_ticks()
        # PARÁLISIS
        if self.paralyzed:
            if self.GAME_TIME.get_ticks() - self.paralysisInstant >= self.TIMEPARALYZED:
                self.paralyzed = False

    def getPos(self):
        return [self.posX, self.posY]


    def jump(self):
        if self.overPlatform and not self.paralyzed:
            self.jumping = True
            self.acJump = 15
            self.overPlatform = False

    def shoot(self):
        if self.GAME_TIME.get_ticks() - self.shootTime >= self.CHARGETIME and not self.shooting and not self.paralyzed:
            self.shooting = True

    def paralyze(self):
        if not self.paralyzed:
            self.paralyzed = True
            self.paralysisInstant = self.GAME_TIME.get_ticks()

    def harm(self):
        if self.attacking:
            self.attacking = False
            return True

    def draw(self, surface, otherPlayerPos):
        for i, bullet in enumerate(self.bullet):
            surface.blit(self.bulletImage, (bullet[0], bullet[1]))
            if bullet[2] == 'left':
                bullet[0] -= 20
            else:
                bullet[0] += 20
            if ((bullet[0] > otherPlayerPos[0] and bullet[0] < (otherPlayerPos[0] + self.WIDTH)) \
                    or ((bullet[0] + 15) > otherPlayerPos[0] and (bullet[0] + 15) < (otherPlayerPos[0] + self.WIDTH))) \
                    and ((bullet[1] > otherPlayerPos[1] and bullet[1] < (otherPlayerPos[1] + self.HEIGHT)) \
                    or ((bullet[1] + 15) > otherPlayerPos[1] and (bullet[1] + 15) < (otherPlayerPos[1] + self.HEIGHT))):
                self.attacking = True
                self.bullet.pop(i)
            if bullet[0] > self.STAGESIZES[0][2] or bullet[0] < 0:
                self.bullet.pop(i)
                print('eliminado')
        pygame.draw.rect(surface, self.color, pygame.Rect(self.posX, self.posY, self.WIDTH, self.HEIGHT))