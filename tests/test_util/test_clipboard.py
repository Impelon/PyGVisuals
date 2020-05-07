# _*_ coding: UTF-8 _*_

# --- imports
# preinstalled python libraries
import unittest
import random

# pygame imports
import pygame
from pygame.locals import *

# local imports
import pygvisuals.util.clipboard as cb

class TestClipboard(unittest.TestCase):

    def disablePyperclip(self):
        try:
            import pyperclip
            pyperclip.paste = None
            pyperclip.copy = None
        except: pass

    def disableScrap(self):
        try:
            import pygame.scrap
            pygame.scrap.get = None
            pygame.scrap.put = None
        except: pass

    def setUp(self):
        try:
            self.clipboard_paste = cb.paste
            self.clipboard_copy = cb.copy
        except: pass
        try:
            import pyperclip
            self.pyperclip_paste = pyperclip.paste
            self.pyperclip_copy = pyperclip.copy
        except: pass
        try:
            import pygame.scrap
            self.scrap_get = pygame.scrap.get
            self.scrap_put = pygame.scrap.put
        except: pass

    def tearDown(self):
        try:
            pygame.display.quit()
        except: pass
        cb.paste = self.clipboard_paste
        cb.copy = self.clipboard_copy
        try:
            import pyperclip
            pyperclip.paste = self.pyperclip_paste
            pyperclip.copy = self.pyperclip_copy
        except: pass
        try:
            import pygame.scrap
            pygame.scrap.get = self.scrap_get
            pygame.scrap.put = self.scrap_put
        except: pass

    def testWithPyperclip(self):
        try:
            import pyperclip
        except:
            return
        self.disableScrap()
        test_message = "Test message " + str(random.random())
        cb.copy(test_message)
        self.assertEqual(cb.paste(), test_message)

    def testWithScrap(self):
        try:
            import pygame.scrap
        except:
            return
        self.disablePyperclip()
        pygame.init()
        pygame.display.set_mode((50, 50), DOUBLEBUF, 32)
        for i in range(10):
            if i == 8:
                test_message = "Test message " + str(random.random())
                cb.copy(test_message)
                self.assertEqual(cb.paste(), test_message)
            pygame.time.wait(50)
            pygame.display.update()
        pygame.display.quit()

    def testUnicode(self):
        pygame.init()
        pygame.display.set_mode((50, 50), DOUBLEBUF, 32)
        for i in range(10):
            if i == 8:
                test_message = u"Test message " + str(random.random()) + u"★⭐✰✪"
                cb.copy(test_message)
                self.assertEqual(cb.paste(), test_message)
            pygame.time.wait(50)
            pygame.display.update()
        pygame.display.quit()


    def testUnicodeWithScrap(self):
        self.disablePyperclip()
        pygame.init()
        pygame.display.set_mode((50, 50), DOUBLEBUF, 32)
        for i in range(10):
            if i == 8:
                test_message = u"Test message " + str(random.random()) + u"★⭐✰✪"
                cb.copy(test_message)
                self.assertEqual(cb.paste(), test_message)
            pygame.time.wait(50)
            pygame.display.update()
        pygame.display.quit()
