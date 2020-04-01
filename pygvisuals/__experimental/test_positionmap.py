# -*- coding: cp1252 -*-

from . import positionmap
import pygame, pygame.gfxdraw
import sys, random, time
from pygame.locals import *

pygame.init()

m           = positionmap.PositionMap()
screen      = pygame.display.set_mode((1000, 800), 0, 32)
rc          = False
stop        = False
mode        = "n"
testhelp    = ("Press following keys for respective actions:",
               "t: Toggle color randomness (pixel-drawingmode only)",
               "i: Print info about the status of the PositionMap",
               "b: Create the PositionMap from an image in the same folder (map.png)",
               "l: Create the PositionMap from a list hardcoded in the sourcecode",
               "+: Scale up the PositionMap by a factor of 2",
               "-: Scale down the PositionMap by a factor of 0.5",
               "F5 or F11: Scale up the PositionMap so it fits the entire screen",
               "Down-key: Create an imagefile (result.png) with the current state of the PositionMap",
               "n: Switch to normal-drawing mode; Draws the PositionMap according to mapobject.toSurface()",
               "p: Switch to pixel-drawing mode; Draws the PositionMap by drawing a row of pixels individually",
               "s: Switch to slow pixel-drawing mode; Draws the PositionMap drawing each pixel individually",
               "r: Switch to slow pixel-drawing mode; Draws the PositionMap drawing each pixel individually at a random position")

def createFromImage():
    """
    Create the PositionMap by using an imagefile (map.png)

    parameter:      -
    return values:  -
    """
    global m
    m = positionmap.createByImage()

def createFromList():
    """
    Create the PositionMap by using a list
    
    parameter:      -
    return values:  -
    """
    global m
    l = (
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                W",
    "W                                W",
    "W   WWW        WW       WWWWW    W",
    "W   W         WWWWW              W",
    "W   W   WWW       W              W",
    "W   W     W       W              W",
    "W   W     W  W       WWW        WW",
    "W   WWW   W                W W   W",
    "W     W   W   WWW                W",
    "WW   WW               WWWWW W    W",
    "W   W                            W",
    "W   W   WWWW           WWW       W",
    "W                                W",
    "W   WW    W                      W",
    "W         WWWWWW                 W",
    "W         W                      W",
    "W         W          WWWWW       W",
    "W                        W       W",
    "WWWW                      W      W",
    "W                 WWWWW          W",
    "W                  W             W",
    "W                 W              W",
    "W   WWWWW                        W",
    "W                                W",
    "W             WWWWWWWW           W",
    "W                  W             W",
    "WWWWWWW                   WWWWWWWW",
    "W                                W",
    "W                                W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    )
    m = positionmap.createByList(l)

def saveMap():
    """
    Save the PositionMap as an imagefile
    
    parameter:      -
    return values:  -
    """
    global m
    try:
        pygame.image.save(m.toSurface(), "result.png")
    except:
        pass

def mapScaleUp():
    """
    Expand the PositionMap
    
    parameter:      -
    return values:  -
    """
    global m
    m = positionmap.scale(m, 2)

def mapScaleDown():
    """
    Reduce the size of the PositionMap
    
    parameter:      -
    return values:  -
    """
    global m
    m = positionmap.scale(m, 0.5)

def mapFullscreen():
    """
    Expand the PositionMap to window-size
    
    parameter:      -
    return values:  -
    """
    global m, screen
    monitorinfo = pygame.display.Info()
    m = positionmap.scale(m, (screen.get_width() / max(m.getWidth(), 1), screen.get_height() / max(m.getHeight(), 1)))

def mapDraw():
    """
    Draw the PositionMap by drawing the objects image representation (map.toSurface())
    
    parameter:      -
    return values:  -
    """
    global m, screen
    stop = False
    color = (250, 150, 100)
    screen.blit(m.toSurface(), (0, 0))
    handleInput()
    pygame.display.update()

def mapDrawPixel():
    """
    Draw the PositionMap by drawing a row of pixels
    
    parameter:      -
    return values:  -
    """
    global m, screen, rc, stop
    stop = False
    color = (250, 150, 100)
    for x in range(m.getWidth()):
        for y in range(m.getHeight()):
            if rc:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if not m.isPositionValid(x, y):
                pygame.gfxdraw.pixel(screen, x, y, color)
        handleInput()
        pygame.display.update()
        if stop:
            return

def mapDrawPixelSlow():
    """
    Draw the PositionMap by drawing each pixels individually
    
    parameter:      -
    return values:  -
    """
    global m, screen, rc, stop
    stop = False
    color = (250, 150, 100)
    for x in range(m.getWidth()):
        for y in range(m.getHeight()):
            if rc:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if not m.isPositionValid(x, y):
                pygame.gfxdraw.pixel(screen, x, y, color)
            handleInput()
            pygame.display.update()
            if stop:
                return

def mapDrawPixelRandom():
    """
    Draw the PositionMap by drawing a random pixel
    
    parameter:      -
    return values:  -
    """
    global m, screen, rc, stop
    stop = False
    color = (250, 150, 100)
    while True:
        for n in range(m.getHeight()):
            x, y = random.randint(0, m.getWidth()), random.randint(0, m.getHeight())
            if rc:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if not m.isPositionValid(x, y):
                pygame.gfxdraw.pixel(screen, x, y, color)
        handleInput()
        pygame.display.update()
        if stop:
            screen.fill((255, 255, 255))
            return

def printHelp():
    """
    Print the help-information
    
    parameter:      -
    return values:  -
    """
    for ln in testhelp:
        print(ln)

def handleInput():
    """
    Handle User-Input
    
    parameter:      -
    return values:  -
    """
    global rc, m, stop, mode
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            key = event.str.encode("ascii", "ignore").lower()

            if key == "t":
                rc = not rc
            if key == "i":
                print("invalid Positions:", m.getLengthInvalidPositions(), "possible Positions:", m.getWidth() * m.getHeight())
            if key == "h":
                printHelp()
            if key == "b":
                createFromImage()
            if key == "l":
                createFromList()
            if key == "+":
                mapScaleUp()
            if key == "-":
                mapScaleDown()
            if event.key in (pygame.K_F5, pygame.K_F11):
                mapFullscreen()
            if event.key == pygame.K_DOWN:
                saveMap()
            
            if key in ("n", "p", "s", "r"):
                mode = key
                stop = True

if __name__ == "__main__":
    createFromImage()
    printHelp()
    while True:
        if mode == "n":
            mapDraw()
        elif mode == "p":
            mapDrawPixel()
        elif mode == "s":
            mapDrawPixelSlow()
        elif mode == "r":
            mapDrawPixelRandom()
        else:
            mapDraw()
        screen.fill((255, 255, 255))
