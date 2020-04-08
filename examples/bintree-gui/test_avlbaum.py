# -*- coding: cp1252 -*-

import unittest
import random
from . import avlbaum

class TestAVLBaum(unittest.TestCase):

    def setUp(self):
        # Quellcode, der zur Testvorbereitung ausgeführt wird (vgl. "test fixture")
        pass

    def tearDown(self):
        # Quellcode, der zum Testabschluss ausgeführt wird (vgl. "test fixture")
        pass

    def testEinfuegen(self):
        tree = avlbaum.AVLBaum()
        l = [5, 3, 7, 2, 9, 4, 6, 1, 8, 10]
        done = []
        for element in l:
            tree.einfuegen(element)
            done.append(element)
            self.assertAllNodesBalanced(tree)
            self.assertNodesInOrder(tree, done)

        self.assertEqual(tree.root.holeWert(), 5)
        self.assertEqual(tree.root.holeRechts().holeRechts().holeRechts().holeWert(), 10)
    
    def testLoeschenBlatt(self):
        tree = avlbaum.AVLBaum()
        l = [2, 3, 1]
        for element in l:
            tree.einfuegen(element)

        tree.loeschen(1)
        self.assertEqual(tree.root.holeWert(), 2)
        self.assertEqual(tree.root.holeRechts().holeWert(), 3)
        self.assertNodesInOrder(tree, l[:2])
        self.assertAllNodesBalanced(tree)

    def testLoeschenWurzel(self):
        tree = avlbaum.AVLBaum()
        l = [2, 3, 1]
        for element in l:
            tree.einfuegen(element)

        tree.loeschen(2)
        self.assertEqual(tree.root.holeWert(), 1)
        self.assertEqual(tree.root.holeRechts().holeWert(), 3)
        self.assertAllNodesBalanced(tree)
        self.assertNodesInOrder(tree, l[1:])

    def testLoeschenAlles(self):
        tree = avlbaum.AVLBaum()
        l = [5, 3, 7, 2, 9, 4, 6, 1, 8, 10]
        for element in l:
            tree.einfuegen(element)

        for n in range(len(l)):
            w = tree.root.holeWert()
            tree.loeschen(w)
            l.remove(w)
            self.assertAllNodesBalanced(tree)
            self.assertNodesInOrder(tree, l)

    def testEinfachLinksRotation(self):
        tree = avlbaum.AVLBaum()
        l = [5, 3, 7, 2, 9, 4, 6, 1, 8, 10]
        for element in l:
            tree.einfuegen(element)
        tree.einfuegen(11)
        
        self.assertAllNodesBalanced(tree)
        self.assertNodesInOrder(tree, l + [11])
        
        self.assertEqual(tree.root.holeWert(), 5)
        self.assertEqual(tree.root.holeLinks().holeWert(), 3)
        self.assertEqual(tree.root.holeLinks().holeLinks().holeWert(), 2)
        self.assertEqual(tree.root.holeLinks().holeLinks().holeLinks().holeWert(), 1)
        self.assertEqual(tree.root.holeLinks().holeRechts().holeWert(), 4)
        self.assertEqual(tree.root.holeRechts().holeWert(), 9)
        self.assertEqual(tree.root.holeRechts().holeLinks().holeWert(), 7)
        self.assertEqual(tree.root.holeRechts().holeLinks().holeLinks().holeWert(), 6)
        self.assertEqual(tree.root.holeRechts().holeLinks().holeRechts().holeWert(), 8)
        self.assertEqual(tree.root.holeRechts().holeRechts().holeWert(), 10)
        self.assertEqual(tree.root.holeRechts().holeRechts().holeRechts().holeWert(), 11)

    def testEinfachRechtsRotation(self):
        tree = avlbaum.AVLBaum()
        l = [5, 3, 7, 2, 9, 4, 6, 1, 8, 10]
        for element in l:
            tree.einfuegen(element)
        tree.einfuegen(0)
        
        self.assertAllNodesBalanced(tree)
        self.assertNodesInOrder(tree, l + [0])

        self.assertEqual(tree.root.holeWert(), 5)
        self.assertEqual(tree.root.holeLinks().holeWert(), 3)
        self.assertEqual(tree.root.holeLinks().holeLinks().holeWert(), 1)
        self.assertEqual(tree.root.holeLinks().holeLinks().holeLinks().holeWert(), 0)
        self.assertEqual(tree.root.holeLinks().holeLinks().holeRechts().holeWert(), 2)
        self.assertEqual(tree.root.holeLinks().holeRechts().holeWert(), 4)
        self.assertEqual(tree.root.holeRechts().holeWert(), 7)
        self.assertEqual(tree.root.holeRechts().holeLinks().holeWert(), 6)
        self.assertEqual(tree.root.holeRechts().holeRechts().holeWert(), 9)
        self.assertEqual(tree.root.holeRechts().holeRechts().holeLinks().holeWert(), 8)
        self.assertEqual(tree.root.holeRechts().holeRechts().holeRechts().holeWert(), 10)

    def testDoppeltLinksRotation(self):
        tree = avlbaum.AVLBaum()
        l = [2, 1, 6, 7, 4]
        for element in l:
            tree.einfuegen(element)
        tree.einfuegen(5)
        
        self.assertAllNodesBalanced(tree)
        self.assertNodesInOrder(tree, l + [5])

        self.assertEqual(tree.root.holeWert(), 4)
        self.assertEqual(tree.root.holeLinks().holeWert(), 2)
        self.assertEqual(tree.root.holeLinks().holeLinks().holeWert(), 1)
        self.assertEqual(tree.root.holeRechts().holeWert(), 6)
        self.assertEqual(tree.root.holeRechts().holeLinks().holeWert(), 5)
        self.assertEqual(tree.root.holeRechts().holeRechts().holeWert(), 7)

    def testDoppeltRechtsRotation(self):
        tree = avlbaum.AVLBaum()
        l = [3, 1, 7, 2, 8, 5, 4, 6]
        for element in l:
            tree.einfuegen(element)
        tree.einfuegen(6.5)
        
        self.assertAllNodesBalanced(tree)
        self.assertNodesInOrder(tree, l + [6.5])

        self.assertEqual(tree.root.holeWert(), 3)
        self.assertEqual(tree.root.holeLinks().holeWert(), 1)
        self.assertEqual(tree.root.holeLinks().holeRechts().holeWert(), 2)
        self.assertEqual(tree.root.holeRechts().holeWert(), 6)
        self.assertEqual(tree.root.holeRechts().holeLinks().holeWert(), 5)
        self.assertEqual(tree.root.holeRechts().holeLinks().holeLinks().holeWert(), 4)
        self.assertEqual(tree.root.holeRechts().holeRechts().holeWert(), 7)
        self.assertEqual(tree.root.holeRechts().holeRechts().holeLinks().holeWert(), 6.5)
        self.assertEqual(tree.root.holeRechts().holeRechts().holeRechts().holeWert(), 8)

    def testKomplex(self):
        tree = avlbaum.AVLBaum()
        l = []
        amount = 200
        for i in range(0, amount):
            while 1:
                number = random.randint(1, amount)
                if number not in l:
                  l.append(number)
                  break
        done = []
        for element in l:
            tree.einfuegen(element)
            done.append(element)
            self.assertAllNodesBalanced(tree)
            self.assertNodesInOrder(tree, done)
        for element in l:
            tree.loeschen(element)
            done.remove(element)
            self.assertAllNodesBalanced(tree)
            self.assertNodesInOrder(tree, done)
    
    def testLeeren(self):
        tree = avlbaum.AVLBaum()
        l = [5, 3, 7, 2, 9, 4, 6, 1, 8, 10]
        for element in l:
            tree.einfuegen(element)
        tree.leeren()
        
        self.assertIsNone(tree.root)

    def testSuchen(self):
        tree = avlbaum.AVLBaum()
        l = [5, 3, 7, 2, 9, 4, 6, 1, 8, 10]
        for element in l:
            tree.einfuegen(element)

        self.assertEqual(tree.suchen(5), 5)
        self.assertIsNone(tree.suchen(11))

    def testHoleTiefe(self):
        tree = avlbaum.AVLBaum()
        l = [5, 3, 7, 2, 9, 4, 6, 1, 8, 10]
        for element in l:
            tree.einfuegen(element)

        self.assertEqual(tree.holeTiefe(avlbaum.AVLKnoten()), 0)
        self.assertEqual(tree.holeTiefe(tree.root), 1)
        self.assertEqual(tree.holeTiefe(tree.root.holeRechts().holeRechts().holeRechts()), 4)

    def testTraversieren(self):
        tree = avlbaum.AVLBaum()
        l = [5, 3, 7, 2, 9, 4, 6, 1, 8, 10]
        for element in l:
            tree.einfuegen(element)
        pre = [(5, 3), (3, 2), (2, 1), (1, 0), (4, 0), (7, 2), (6, 0), (9, 1), (8, 0), (10, 0)]
        post = [(1, 0), (2, 1), (4, 0), (3, 2), (6, 0), (8, 0), (10, 0), (9, 1), (7, 2), (5, 3)]

        self.assertEqual(pre, tree.traversieren("pre"))
        self.assertEqual(post, tree.traversieren("post"))
    
    def assertNodesInOrder(self, tree, l):
        inorder = tree.traversieren("in")
        l.sort()
        if len(l) > 0:
            self.assertEqual(len(l), len(inorder))
            for n in range(len(inorder)):
                self.assertEqual(l[n], inorder[n][0])

    def assertAllNodesBalanced(self, tree):
        self.assertTrue(self.areNodesBalanced(tree))

    def areNodesBalanced(self, tree, node = None):
        if tree.root == None:
            return True
        else:
            if node == None:
                node = tree.root
            node.bestimmeKBalance()
            balance = node.holeKBalance()
            if balance >= -1 and balance <= 1:
                if node.holeLinks() != None:
                    self.areNodesBalanced(tree, node.holeLinks())
                if node.holeRechts() != None:
                    self.areNodesBalanced(tree, node.holeRechts())
                return True
            return False

#testRotation/einfach

#testRotation/doppelt

if __name__ == "__main__":
    unittest.main()
