#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 18:21:31 2019

@author: Silvia Mena González y Antonio Muñoz Santiago

This is a class file
"""

import pygame, random

class player:
    def __init__(self, type, posX, posY, PLAYERDIMENSIONS, STAGESIZES, GAME_TIME):
        self.type = type # puede ser alien o humanoid
        self.GAME_TIME = GAME_TIME
        self.WIDTH = PLAYERDIMENSIONS[0]
        self.HEIGHT = PLAYERDIMENSIONS[1]
        self.STAGESIZES = STAGESIZES
        self.GRAVITY = 3.8 # Lo que se le resta a posY
        self.CHARGETIME = 3000 # Tiempo mínimo entre cada disparo
        self.TIMESHOOTING = 100 # El tiempo que tendrá puesta la imágen del disparo
        self.TIMEPARALYZED = 5000 # Tiempo que el jugador permanecerá paralizado
        self.STEPTIME = 100 # Tiempo entre cada paso
        self.posX = posX
        self.posY = posY
        self.VELX = 15
        self.MAXVEL = -30 # La velocidad máxima que alcanza cayendo
        self.jumping = False # Para indicar cuando está saltando
        self.acJump = 0 # La aceleración del salto, se cambia su valor desde jump()
        self.overPlatform = False
        self.bullet = [] # Lista con las balas existentes
        self.shooting = False # Variable para indicar si está disparando
        self.shootTime = 0 # El instante del último disparo
        self.paralyzed = False # Si el jugador está paralizado
        self.paralysisInstant = None # Para almacenar el instante cuando el jugador queda paralizado
        self.lastStep = 0 # Para almacenar el instante del último paso
        self.lastWalkingImage = 1 # La última imágen de andar
        self.walking = False # Para saber si esta andando y está en una plataforma
        self.pointing = False # Para indicar si está apuntando
        self.attacking = False # Para saber cuando ha dañado al otro jugador
        if self.type == "alien":
            self.imageList = [
                (255, 0, 0), # notMoving
                (0, 255, 0), # walking1
                (0, 0, 255), # walking2
                (255, 0, 255), # jumping
                (255, 255, 255), # shooting
                (0, 0, 0) # paralyzed
            ]
            self.imageToDraw = self.imageList[0]
            self.direction = 'right' # La dirección a la que apunta
        else:
            self.imageList = [
                (255, 0, 0),  # notMoving
                (0, 255, 0),  # walking1
                (0, 0, 255),  # walking2
                (255, 0, 255),  # jumping
                (255, 255, 255),  # shooting
                (0, 0, 0)  # paralyzed
            ]
            self.imageToDraw = self.imageList[0]
            self.direction = 'left'
        self.bulletImage = pygame.image.load("assets/images/player/bullet/bullet.png")

        # LOAD SOUNDS

        self.chargeSound = pygame.mixer.Sound('assets/sounds/charge.ogg')
        self.shootSound = pygame.mixer.Sound('assets/sounds/shoot.ogg')

    # Función que devuelve True cuando el personaje está dentro de la plataforma
    def inPlat(self, plat):
        isIn = []
        point = []
        point.append((self.posX, self.posY + self.HEIGHT+1))
        point.append((self.posX+self.WIDTH, self.posY + self.HEIGHT+1))
        for p in point:
            isIn.append(p[0]>plat[0] and p[0]<plat[0]+plat[2] and p[1]>plat[1] and p[1] < plat[1]+plat[3])
        for i in isIn:
            if i:
                return True
        return False

    def whichPlat(self):
        for i, plat in enumerate(self.STAGESIZES):
            if self.inPlat(plat):
                return i
        return -1

    def move(self, WINDOW_WIDTH, WINDOW_HEIGHT, direction = None):
        if direction == 'left' and self.posX >= 30 and not self.paralyzed and self.posX > self.STAGESIZES[0][3]:
            self.posX -= self.VELX
            self.direction = 'left'
            if self.overPlatform:
                self.walking = True
        if direction == 'right' and (self.posX + self.WIDTH) <= (WINDOW_WIDTH-30) and not self.paralyzed and self.posX + self.WIDTH < self.STAGESIZES[0][2]:
            self.posX += self.VELX
            self.direction = 'right'
            if self.overPlatform:
                self.walking = True
        if direction == None:
            self.walking = False
        if self.posX < self.STAGESIZES[0][3]:
            self.posX = self.STAGESIZES[0][3]
        if self.posX + self.WIDTH > self.STAGESIZES[0][2] - 30:
            self.posX = self.STAGESIZES[0][2] - 30 - self.WIDTH
        if not self.overPlatform and not self.jumping and self.whichPlat() == -1:
            if self.acJump > self.MAXVEL:
                self.acJump -= self.GRAVITY
            self.posY -= self.acJump
            self.walking = False
        elif not self.jumping:
            self.acJump = 0
            if not self.overPlatform:
                self.posY = self.STAGESIZES[self.whichPlat()][1] - self.HEIGHT
                self.overPlatform = True
            if self.whichPlat() == -1:
                self.overPlatform = False
        elif self.jumping and self.posY >= self.STAGESIZES[1][2]:
            self.acJump -= self.GRAVITY
            self.posY -= self.acJump
            if self.acJump < 0:
                self.jumping = False
        if self.posY < self.STAGESIZES[1][2]:
            self.posY = self.STAGESIZES[1][2]
            self.acJump = 0

        # DISPARO
        if self.shooting:
            print(self.direction)
            self.bullet.append([self.posX + (self.WIDTH / 2), self.posY + (self.HEIGHT / 2), self.direction])
            self.shooting = False
            self.shootTime = self.GAME_TIME.get_ticks()
        if self.GAME_TIME.get_ticks() - self.shootTime >= self.TIMESHOOTING and self.pointing:
            self.pointing = False
            self.chargeSound.play()
        # PARÁLISIS
        if self.paralyzed:
            if self.GAME_TIME.get_ticks() - self.paralysisInstant >= self.TIMEPARALYZED:
                self.paralyzed = False

    def getPos(self):
        return [self.posX, self.posY]


    def jump(self):
        if self.overPlatform and not self.paralyzed:
            self.jumping = True
            self.acJump = 48
            self.overPlatform = False
            self.walking = False

    def shoot(self):
        if self.GAME_TIME.get_ticks() - self.shootTime >= self.CHARGETIME and not self.shooting and not self.paralyzed:
            self.shooting = True
            self.pointing = True
            self.shootSound.play()

    def paralyze(self):
        if not self.paralyzed:
            self.paralyzed = True
            self.paralysisInstant = self.GAME_TIME.get_ticks()

    def harm(self):
        if self.attacking:
            self.attacking = False
            return True

    def draw(self, surface, otherPlayerPos):
        # Para dibujar las balas
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
        # Para dibujar al jugador
        if not self.walking and not self.jumping and self.overPlatform:
            self.imageToDraw = self.imageList[0]
        elif not self.walking and not self.jumping and not self.overPlatform:
            self.imageToDraw = self.imageList[3]
        elif self.walking:
            if self.GAME_TIME.get_ticks() - self.lastStep >= self.STEPTIME:
                if self.lastWalkingImage == 1:
                    self.lastWalkingImage = 2
                else:
                    self.lastWalkingImage = 1
                self.lastStep = self.GAME_TIME.get_ticks()
            self.imageToDraw = self.imageList[self.lastWalkingImage]
        elif self.jumping:
            self.imageToDraw = self.imageList[3]
        if self.pointing:
            self.imageToDraw = self.imageList[4]
        if self.paralyzed:
            self.imageToDraw = self.imageList[5]
        pygame.draw.rect(surface, self.imageToDraw, pygame.Rect(self.posX, self.posY, self.WIDTH, self.HEIGHT))