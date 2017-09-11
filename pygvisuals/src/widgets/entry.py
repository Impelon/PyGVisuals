# -*- coding: cp1252 -*-

import selectiontextwidget
import textwidget
import pygame
from selectiontextwidget import *

class Entry(selectiontextwidget.SelectionTextWidget):

    """
    Entry that accepts keyboard-input
    """
    
    def __init__(self, x, y, width, height, text = "", font = textwidget.defaultFont, selectioncolor = selectiontextwidget.defaultSelection, validation = (lambda *x: True)):
        """
        Initialisation of an Entry

        parameters:     int x-coordinate of the Entry (left)
                        int y-coordinate of the Entry (top)
                        int width of the Entry
                        int height of the Entry
                        string text of the Entry
                        pygame.font.Font font of the Entry
                        tuple of format pygame.Color representing the Entry's selection-color
                        function function that validates input; validation(newtext, oldtext, entry) -> bool
        return values:  -
        """
        super(Entry, self).__init__(x, y, width, height, text, font, selectioncolor = selectiontextwidget.defaultSelection)
        self._validation = validation

    def setText(self, text):
        """
        Set the Entry's text; needs to be valid according to the Entry's validation-function

        parameters:     string the text to be set
        return values:  Entry Entry returned for convenience
        """
        if self._validation(text, self._text, self):
            super(Entry, self).setText(text)
        return self

    def setValidation(self, validation):
        """
        Set the Entry's validation-function

        parameters:     function function that validates input; validation(newtext, oldtext, entry) -> bool
        return values:  Entry Entry returned for convenience
        """
        if callable(validation):
            self._validation = validation
        return self

    def getValidation(self):
        """
        Return the Entry's validation-function

        parameters:     -
        return values:  function the Entry's validation-function
        """
        return self._validation

    def insert(self, index, text):
        """
        Insert a given text at the given index

        parameters:     int the index the text should be insterted at
                        string the text to be insertet
        return values:  -
        """
        index = self.getActualIndex(index)
        self.setText(self._text[:index] + text + self._text[index:])

    def delete(self, startindex, endindex):
        """
        Deletes the Entry's text between the two given indices

        parameters:     int the index from which the text should be deleted
                        int the index till which the text should be deleted
        return values:  -
        """
        startindex, endindex = self._sort(startindex, endindex)
        self.setText(self._text[:startindex] + self._text[endindex:])

    def update(self, *args):
        """
        Handles the selection and keyboard-input

        parameters: tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values: -
        """
        if len(args) > 0 and self.isActive():
            event = args[0]
            if event.type == pygame.KEYDOWN and self.isFocused():
                if event.key == pygame.K_LEFT:
                    self.moveCursor(-1)
                elif event.key == pygame.K_RIGHT:
                    self.moveCursor(1)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    if self._selection == self._cursor:
                        if event.key == pygame.K_DELETE:
                            self.delete(self._selection + 1, CURSOR)
                        else:
                            self.delete(self._selection - 1, CURSOR)
                            self.moveCursor(-1)
                    else:
                        self.delete(SELECTION, CURSOR)
                        self.setCursor(self._sort(SELECTION, CURSOR)[0])
                else:
                    char = event.unicode.encode("ascii", "ignore")
                    if (char != "" and (char == " " or not char.isspace())
                    and self._validation(self._text + char, self._text, self)):
                        self.delete(SELECTION, CURSOR)
                        s = self._sort(SELECTION, CURSOR)[0]
                        self.insert(s, char)
                        self.setCursor(s + 1)
            elif event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos) and event.buttons[0]:
                    self.setSelection(SELECTION, self._posToIndex(event.pos[0] - self.rect.x))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.setCursor(self._posToIndex(event.pos[0] - self.rect.x))
        
        super(Entry, self).update(*args)

    def _getAppearance(self, *args):
        """
        Return the underlying Widget's appearance;
        Renders the Entry's text, cursor and selection

        private function

        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface = super(Entry, self)._getAppearance(*args)
        linesize = self._font.get_linesize()
        surface.blit(self._font.render(str(self._text), pygame.SRCALPHA, self._foreground), (0, (self._bounds.height - linesize) / 2))
        if self.isFocused():
            cursor = pygame.Surface((2, linesize))
            cursor.fill(self._foreground)
            surface.blit(cursor, (self._indexToPos(CURSOR), (self._bounds.height - linesize) / 2))
            selection = pygame.Surface((abs(self._indexToPos(CURSOR) - self._indexToPos(SELECTION)), linesize), pygame.SRCALPHA, 32)
            selection.fill(self._selectioncolor)
            surface.blit(selection, (self._sort(self._indexToPos(CURSOR), self._indexToPos(SELECTION))[0] , (self._bounds.height - linesize) / 2))
        return surface
