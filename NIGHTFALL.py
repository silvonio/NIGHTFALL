#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 18:21:31 2019

@author: Silvia Mena González y Antonio Muñoz Santiago

This is the main file
"""

import pygame, sys, random
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS
import pygame.time as GAME_TIME
import csv

import player, egg

# VARIABLES

state = None # Para indicar en que parte del juego estamos

# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 30

# PYGAME OBJECTS

pygame.display.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('NIGHTFALL')
clock = GAME_TIME.Clock()

# LOAD IMAGES

# LOAD SOUNDS

# FUNCTIONS

def quitGame():
    pygame.quit()
    sys.exit()

# MAIN LOOP

while True:
    # Handle user and system events
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.KEYUP:
            pass
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()

clock.tick(FPS)
pygame.display.update()