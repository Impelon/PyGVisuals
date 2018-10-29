# -*- coding: cp1252 -*-
from avlbaum import AVLBaum
import random

derBaum = AVLBaum()


##liste = [15,34,13,4,7,21,14,27,56,3]
##liste = [44,17,78,32,50,88,48,62,84,92,15,35,80,36]
##liste = [47,21,91,17,44,88,96,16,20,30,45,97,4,28]
##liste = [71,56,87,44,64,100,53]

liste = []
anzahl = 100
for i in range(0, anzahl):
    while 1:
        zufall = random.randint(1, anzahl)
        if zufall not in liste:
          liste.append(zufall)
          break

###sortiert
##liste.sort()

for element in liste:
    derBaum.einfuegen(element)

print "Folgende Liste wurde in den Baum eingefügt:"
print liste, "\n"
print "Das traversieren in-order ergibt:"
print derBaum.traversieren("in"), "\n"
print "Das traversieren pre-order ergibt:"
print derBaum.traversieren("pre"), "\n"

##derBaum.loeschen(13)
##print "13 wurde entfernt!"
##print "Das traversieren in-order ergibt:"
##print derBaum.traversieren("in"), "\n"
##
##liste = [44,28,91]
##liste = [64,100]

for i in range(0, len(liste)):
    derBaum.loeschen(liste[i])
    print liste[i], "wurde entfernt!"
    print "Das traversieren in-order ergibt:"
    print derBaum.traversieren("in")
    print "Das traversieren pre-order ergibt:"
    print derBaum.traversieren("pre"), "\n"
    print "Die Balance des Baumes ergibt:"
    print derBaum.root.holeKBalance(), "\n"
    assert derBaum.root.holeKBalance() in [0, 1, -1]

print "Das traversieren in-order ergibt:"
print derBaum.traversieren("in"), "\n"
