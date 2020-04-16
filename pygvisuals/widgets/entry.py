# -*- coding: cp1252 -*-

import pygame
from .selection_text_widget import *
from ..designs import getDefaultDesign, getFallbackDesign

class Entry(SelectionTextWidget):

    """
    Entry that accepts keyboard-input
    """

    def __init__(self, x, y, width, height, text = "", font = getDefaultDesign().font, selection_overlay=getDefaultDesign().selection_overlay, validation = (lambda *x: True)):
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
        super(Entry, self).__init__(x, y, width, height, text, font, selection_overlay)
        self._validation = validation

    def setText(self, text):
        """
        Set the Entry's text; needs to be valid according to the Entry's validation-function

        parameters:     string the text to be set
        return values:  Entry Entry returned for convenience
        """
        if self._validation(text, self.text, self):
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
        self.setText(self.text[:index] + text + self.text[index:])

    def delete(self, startindex, endindex):
        """
        Deletes the Entry's text between the two given indices

        parameters:     int the index from which the text should be deleted
                        int the index till which the text should be deleted
        return values:  -
        """
        startindex, endindex = self._sort(startindex, endindex)
        self.setText(self.text[:startindex] + self.text[endindex:])

    def update(self, *args):
        """
        Handles the selection and keyboard-input

        parameters: tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values: -
        """
        if len(args) > 0 and self.isActive() and self.isFocused():
            event = args[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moveCursor(-1)
                elif event.key == pygame.K_RIGHT:
                    self.moveCursor(1)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    if self.selection_index == self.cursor:
                        if event.key == pygame.K_DELETE:
                            if self._validation(self.text[:self.selection_index] + self.text[self.selection_index + 1:], self.text, self):
                                self.delete(self.selection_index + 1, CURSOR)
                        else:
                            if self._validation(self.text[:self.selection_index - 1] + self.text[self.selection_index:], self.text, self):
                                self.delete(self.selection_index - 1, CURSOR)
                                self.moveCursor(-1)
                    else:
                        s, e = self._sort(SELECTION, CURSOR)
                        if self._validation(self.text[:s] + self.text[e:], self.text, self):
                            self.delete(SELECTION, CURSOR)
                            self.setCursor(s)
                else:
                    char = event.unicode
                    if char != "" and (char == " " or not char.isspace()):
                        s, e = self._sort(SELECTION, CURSOR)
                        if self._validation(self.text[:s] + char + self.text[e:], self.text, self):
                            self.delete(SELECTION, CURSOR)
                            self.insert(s, char)
                            self.setCursor(s + 1)
            elif event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos) and event.buttons[0]:
                    self.setSelection(SELECTION, self._posToIndex(event.pos[0] - self.rect.x))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and event.button != 2:
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
        linesize = self.font.get_linesize()
        surface.blit(self._render(str(self.text)), (0, (self.bounds.height - linesize) / 2))
        if self.isFocused():
            cursor = pygame.Surface((2, linesize))
            cursor.fill(self.foreground)
            surface.blit(cursor, (self._indexToPos(CURSOR), (self.bounds.height - linesize) / 2))
            selection = pygame.Surface((abs(self._indexToPos(CURSOR) - self._indexToPos(SELECTION)), linesize), pygame.SRCALPHA, 32)
            selection.fill(self.selection_overlay)
            surface.blit(selection, (self._sort(self._indexToPos(CURSOR), self._indexToPos(SELECTION))[0] , (self.bounds.height - linesize) / 2))
        return surface
