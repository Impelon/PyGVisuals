#Modules#

from . import avlbaum as avltree

import sys
import random

import pygame
import pygvisuals.widgets as gui
import pygvisuals.borders as brd
import pygvisuals.designs as des
from pygame.locals import *

#Initialization#

pygame.init()

tree = None
update = False

#Functions#

def main_loop():
    """
    Draw and update the window content, handle input events

    parameters:     -
    return values:  -
    """
    global tree, update
    going = True
    while going:
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            group.update(event)
        if tree != None and tree.root != None and update:
            screen.blit(background, (0, 0))
            screen.blit(pygame.transform.scale(getDrawnTree(tree, ((50, 55, 155, 200), (100, 155, 255, 200), (100, 155, 255, 200), (255, 0, 0, 200))), (600, 600)), (0, 0))
            for widget in group:
                widget.markDirty()
                widget.update()
            update = False
        group.draw(screen, background)
        pygame.display.update()
        pygame.time.wait(100)
    pygame.quit()
    sys.exit()

def getDrawnTree(tree, colors = None, surface = None, current = None, pre = None):
    """
    Draw a tree and return the result

    parameters:     AVLBaum tree to draw
                    list with tuples of format pygame.Color for the color to draw with; colors in order for: [balance0, balance1, balance-1, wrongbalance]
                    pygame.Surface the Surface to draw on
                    AVLKnoten current node
                    tuple previous node and previous position
    return values:  pygame.Surface the Surface with the tree drawn on it
    """
    if surface == None:
        size = 0
        if tree.root != None:
            size = 0
            for n in range(tree.holeHoehe() + 1):
                size += 400 // (2 ** n)
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    if tree.root == None:
        print("Tree is empty!")
    else:
        if current == None:
            current = tree.root
        h = tree.holeTiefe(current)
        s = 2 ** (h - 1)
        n = 2 ** (h - 2)
        if pre == None:
            x = surface.get_width() // 2 - ((400 // s) // 2)
            y = 0
        else:
            if pre[0].holeLinks() == current:
                x = pre[1][0] - ((400 // s) // 2)
            else:
                x = pre[1][0] + (400 // max(n, 1)) - ((400 // s) // 2)
            y = pre[1][1] + (400 // max(n, 1))

        surface.blit(pygame.transform.smoothscale(getDrawnNode(current, colors), (400 // s, 400 // s)), (x, y))
        if current.holeLinks() != None:
            surface = getDrawnTree(tree, colors, surface, current.holeLinks(), (current, (x, y)))
        if current.holeRechts() != None:
            surface = getDrawnTree(tree, colors, surface, current.holeRechts(), (current, (x, y)))
    return surface

def getDrawnNode(node, colors = None):
    """
    Draw a node and return the result

    parameters:     AVLKnoten node to draw
                    list with tuples of format pygame.Color for the color to draw with; colors in order for: [balance0, balance1, balance-1, wrongbalance]
    return values:  pygame.Surface the Surface with the node drawn on it
    """
    surface = pygame.Surface((400, 400), pygame.SRCALPHA, 32)
    if colors == None:
        color = (0, 0, 0)
    elif isinstance(colors, (list, tuple)) and isinstance(colors[0], (list, tuple)):
        l = []
        i = 0
        while len(l) < 4:
            l.append(colors[i])
            i %= len(colors)
        balance = node.holeKBalance()
        if balance == -1:
            balance = 2
        elif abs(balance) > 1:
            balance = 3
        color = colors[balance]
    else:
        color = colors

    pygame.draw.circle(surface, color, (200, 200), 200)
    pygame.draw.circle(surface, (0, 0, 0, 0), (200, 200), 160)

    if node.holeLinks() != None:
        pygame.draw.line(surface, color, (80, 320), (0, 400), 40)
    if node.holeRechts() != None:
        pygame.draw.line(surface, color, (320, 320), (400, 400), 40)

    value   = str(node.holeInhalt())
    if float(value) == int(float(value)):
        value = str(int(float(value)))
    font    = pygame.font.Font(None, int(400 / len(value) ** 0.75))
    fsize   = font.size(value)
    surface.blit(font.render(value, False, color), (200 - fsize[0] // 2, 200 - fsize[1] // 2))

    return surface

def addToTree():
    """
    Add a node of the value from the Entry e_value to the tree

    parameters:     -
    return values:  -
    """
    global tree, update
    v = e_value.getText()
    if len(v) <= 0:
        return
    if tree == None:
        tree = avltree.AVLBaum()
    tree.einfuegen(float(v))
    update = True

def deleteFromTree():
    """
    Delete a node of the value from the Entry e_value from the tree

    parameters:     -
    return values:  -
    """
    global tree, update
    v = e_value.getText()
    if len(v) <= 0:
        return
    if tree != None:
        tree.loeschen(float(v))
    update = True

def createRandomTree():
    """
    Create a new random tree with a length and node values from the Entry e_length

    parameters:     -
    return values:  -
    """
    global tree, update
    l       = []
    length  = int(e_length.getText())
    for n in range(length):
        while True:
            number = random.randint(1, length)
            if number not in l:
              l.append(number)
              break
    tree = avltree.AVLBaum()
    for element in l:
        tree.einfuegen(element)
    update = True

def isNumber(newtext, oldtext, entry):
    """
    Validation function for an Entry; limits inputs to numbers of a length smaller than 16

    parameters:     str the text to be set
                    str the current text
                    gui.Entry the entry affected
    return values:  boolean is the operation valid
    """
    return not newtext or (newtext.replace(".", "", 1).isdigit() and len(newtext) < 16)

def isSmallNumber(newtext, oldtext, entry):
    """
    Validation function for an Entry; limits inputs to numbers smaller than 101

    parameters:     str the text to be set
                    str the current text
                    gui.Entry the entry affected
    return values:  boolean is the operation valid
    """
    return not newtext or (newtext.isdigit() and int(newtext) < 101)

#Setting Display#

w = 900
h = 600

screen = pygame.display.set_mode((w, h), 0, 32)
pygame.display.set_caption("Tree-GUI | Python Game")
pygame.mouse.set_visible(1)
pygame.key.set_repeat(50)

background = pygame.Surface((w, h))
background.fill((255, 255, 255))

#Widgets#

des.getDefaultDesign().border     = brd.CompoundBorder(brd.RoundedBorder(3, 3, (150, 190, 255, 200), 8), brd.RoundedBorder(2, 2, (30, 90, 150), 8))
des.getDefaultDesign().background = (120, 160, 200)
w_w                               = 130
w_h                               = 25

w_bg        = gui.Widget(w * 0.8571428571428571 - w_w // 2 - 20, 10, w_w // 2 + w * 0.14285714285714285, h - 20).setBackground((220, 220, 250))
l           = gui.Label(w * 0.8571428571428571 - w_w // 2, 10, w_w, w_h, "Tree-GUI").setBackground((0, 0, 0, 0)).setForeground((50, 50, 50)).setBorder(brd.Border(0, 0))
e_value     = gui.Entry(w * 0.8571428571428571 - w_w // 2, h * 0.125, w_w, w_h).setValidation(isNumber).setText("1")
b_add       = gui.Button(w * 0.8571428571428571 - w_w // 2, h * 0.25, w_w, w_h, "Add to Tree", callback = addToTree)
b_delete    = gui.Button(w * 0.8571428571428571 - w_w // 2, h * 0.375, w_w, w_h, "Delete From Tree", callback = deleteFromTree)
e_length    = gui.Entry(w * 0.8571428571428571 - w_w // 2, h * 0.5, w_w, w_h).setValidation(isSmallNumber).setText("100")
b_create    = gui.Button(w * 0.8571428571428571 - w_w // 2, h * 0.625, w_w, w_h, "Create Random Tree", callback = createRandomTree)
group = pygame.sprite.LayeredDirty([w_bg, l, e_value, b_add, b_delete, e_length, b_create])

#Automatic Start#

if __name__ == "__main__":
    main_loop()
main_loop()
