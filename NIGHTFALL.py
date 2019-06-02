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

state = "menuScreen" # Para indicar en que parte del juego estamos

spacePressed = False
spaceReleased = False
aPressed = False
dPressed = False
wPressed = False
huevera = [] # Para guardar todos los objetos huevo
timeForEggs = 3000 # Para almacenar el instante en el que se ha creado el último huevo
timeForTitle = GAME_TIME.get_ticks() # Para almecenar el instante del último parpadeo
timeBetweenOff = random.randint(1500, 10000) # El tiempo entre cada parpadeo
initTime = None # Para almacenar el instante de inicio del juego

# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 30
TIMEBETWEENEGGS = 3000
GAMEDURATION = 120000 # Los milisegundos que dura una partida
LIGHTCHANGES = [(0, 0), (200, 1), (500, 0), (800, 1), (850, 0), (1000, 1), (1100, 0), (1300, 1)]

# PYGAME OBJECTS

pygame.display.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('NIGHTFALL')
clock = GAME_TIME.Clock()
pygame.font.init()
textFont = pygame.font.SysFont("arialblack", 30)
huevo = egg.egg()
alien = player.player('alien', 100, 570)

# LOAD IMAGES

titleImage = [
    pygame.image.load("assets/images/background/off.png"),
    pygame.image.load("assets/images/background/on.png")
]

# LOAD SOUNDS

# FUNCTIONS

def quitGame():
    pygame.quit()
    sys.exit()

def resetPressed():
    global spacePressed, spaceReleased
    spacePressed = False
    spaceReleased = False

def drawSun(posY, color):
    global surface
    pygame.draw.circle(surface, color, (int(WINDOW_WIDTH*0.7),posY), 50)

def drawTitle():
    global titleImage, timeForTitle, timeBetweenOff
    time = GAME_TIME.get_ticks()-timeForTitle
    if time <= timeBetweenOff:
        for state in LIGHTCHANGES:
            if time > state[0]:
                imageToDraw = titleImage[state[1]]
    else:
        imageToDraw = titleImage[0]
        timeForTitle = GAME_TIME.get_ticks()
        timeBetweenOff = random.randint(1500, 10000)  # El tiempo entre cada parpadeo
    surface.blit(imageToDraw, (100, 200))

def map (x0, xf, y0, yf, x):
    m = (yf-y0)/(xf-x0)
    return int(m*(x-x0)+y0)

def drawStage():
    global surface, state
    if state == "menuScreen":
        surface.fill((0, 0, 0))
        drawTitle()
        renderedText = textFont.render('Pulsa espacio', 2, (255, 255, 255))
        surface.blit(renderedText, (350, 400))

    elif state == "playing":
        time = GAME_TIME.get_ticks() - initTime
        surface.fill((map(0,GAMEDURATION,160,70,time), map(0,GAMEDURATION,220,0,time), map(0,GAMEDURATION,185,0,time)))
        drawSun(map(0,GAMEDURATION,-50,WINDOW_HEIGHT+50, time),(255,map(0,GAMEDURATION,255,50,time),0))

        # Para dibujar los palos

        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(0, 0, 1000, 30))
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(0, 0, 30, 700))
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(0, 670, 1000, 30))
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(0, 0, 1000, 30))
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(970, 0, 30, 700))

        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(0, 475, 350, 30))
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(650, 475, 350, 30))

        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(0, 250, 200, 30))
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(800, 250, 200, 30))

        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(350, 250, 300, 30))


# STATE FUNCTIONS

def menuScreen():
    pass

def playing():
    global timeForEggs, WINDOW_WIDTH
    if (GAME_TIME.get_ticks() - TIMEBETWEENEGGS) >= timeForEggs:
        print("Nuevo huevo por favor")
        huevera.append(egg.egg())
        timeForEggs = GAME_TIME.get_ticks()
    for eachEgg in huevera:
        eachEgg.draw(surface)
    alien.draw(surface)
    if aPressed:
        alien.move(WINDOW_WIDTH, WINDOW_HEIGHT, 'left')
    if dPressed:
        alien.move(WINDOW_WIDTH, WINDOW_HEIGHT, 'right')
    if wPressed:
        alien.jump()
    alien.move(WINDOW_WIDTH, WINDOW_HEIGHT)
# MAIN LOOP

while True:
    drawStage()
    # Handle user and system events
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spacePressed = True
                spaceReleased = False
            if event.key == pygame.K_a:
                aPressed = True
            if event.key == pygame.K_d:
                dPressed = True
            if event.key == pygame.K_w:
                wPressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                spacePressed = False
                spaceReleased = True
            if event.key == pygame.K_a:
                aPressed = False
            if event.key == pygame.K_d:
                dPressed = False
            if event.key == pygame.K_w:
                wPressed = False
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()

    if state == "menuScreen":
        menuScreen()
        if spaceReleased:
            state = "playing"
            initTime = GAME_TIME.get_ticks()
            resetPressed()

    elif state == "playing":
        playing()

    clock.tick(FPS)
    pygame.display.update()