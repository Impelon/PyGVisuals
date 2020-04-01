# -*- coding: cp1252 -*-

from . import selectiontextwidget
from . import textwidget
import pygame
from .selectiontextwidget import *

VIEWPOINT       = 'v'

class Listbox(selectiontextwidget.SelectionTextWidget):

    """
    Listbox for displaying lists of multiple objects as strings
    """
    
    def __init__(self, x, y, width, height, editable = False, font = textwidget.defaultFont, selectioncolor = selectiontextwidget.defaultSelection):
        """
        Initialisation of an Listbox

        parameters:     int x-coordinate of the Listbox (left)
                        int y-coordinate of the Listbox (top)
                        int width of the Listbox
                        int height of the Listbox
                        boolean if the Listbox should be editable
                        pygame.font.Font font of the Listbox
                        tuple of format pygame.Color representing the Listbox's selection-color
        return values:  -
        """
        super(Listbox, self).__init__(x, y, width, height, "", font, selectioncolor = selectiontextwidget.defaultSelection)
        self._list      = []
        self._editable  = editable
        self._viewpoint = self._cursor

    def setEditable(self, editable):
        """
        Set Listbox as editable

        parameters:     boolean if the Listbox should be editable
        return values:  Listbox Listbox returned for convenience
        """
        self._editable = bool(editable)
        return self

    def isEditable(self):
        """
        Return if the Listbox should be editable

        parameters:     -
        return values:  boolean is the Listbox editable
        """
        return self._editable

    def setViewpoint(self, index):
        """
        Set the Listbox's viewpoint

        parameters:     int the index the viewpoint should be set to
        return values:  -
        """
        self._viewpoint = self.getActualIndex(index)
        self.markDirty()

    def getViewpoint(self):
        """
        Return the Listbox's viewpoint

        parameters:     -
        return values:  int the Listbox's viewpoint
        """
        return self._viewpoint

    def moveViewpoint(self, index):
        """
        Move the Listbox's cursor-position by the given amount

        parameters:     int the amount the viewpoint should be moved by
        return values:  -
        """
        self.setViewpoint(min(max(self.getActualIndex(VIEWPOINT) + int(index), 0), self.getActualIndex(END)))

    def setCursor(self, index):
        """
        Set the Listbox's cursor-position

        parameters:     int the index the cursor should be set to
        return values:  -
        """
        if self._indexToPos(index) < 0:
            self.setViewpoint(index)
        elif self._indexToPos(index) > self.rect.h:
            self.setViewpoint(index - (self.rect.h / self._font.get_linesize()))
        super(Listbox, self).setCursor(index)

    def setText(self, text):
        """
        Set the Listbox's text; any given text will be ignored; use insert or delete instead

        parameters:     string the text to be set
        return values:  Listbox Listbox returned for convenience
        """
        return self

    def getText(self):
        """
        Return the Listbox's text

        parameters:     -
        return values:  string the Listbox's text
        """
        return str(self._list)[1:-1]

    def setList(self, l):
        """
        Set the Listbox's list

        parameters:     list the list to be set
        return values:  Listbox Listbox returned for convenience
        """
        if isinstance(l, list):
            self._list = l
            self.markDirty()
        return self

    def getList(self):
        """
        Get the Listbox's list

        parameters:     -
        return values:  list the Listbox's list
        """
        return self._list

    def insert(self, index, obj):
        """
        Insert a given object into the list at the given index

        parameters:     int the index the object should be insterted at
                        object the object to be inserted
        return values:  -
        """
        index = self.getActualIndex(index)
        self._list.append(obj)
        self.markDirty()

    def delete(self, startindex, endindex):
        """
        Deletes the Listbox's objects from the list between the two given indices

        parameters:     int the index from which the objects should be deleted
                        int the index till which the objects should be deleted
        return values:  -
        """
        startindex, endindex = self._sort(startindex, endindex)
        del self._list[startindex:endindex]
        self.markDirty()

    def getActualIndex(self, index):
        """
        Return the actual index corresponding to the given index-representation

        parameters:     object object representing the index
        return values:  int the actual index of the Listbox's text
        """
        if index == END:
            return len(self._list)
        if index == VIEWPOINT:
            return self._viewpoint
        return super(Listbox, self).getActualIndex(index)

    def _indexToPos(self, index):
        """
        Return the relative y-coordinate corresponding to the given index

        private function

        parameters:     int index given
        return values:  int relative y-coordinate
        """
        return self._font.get_linesize() * (index - self._viewpoint)

    def _posToIndex(self, y):
        """
        Return the index corresponding to the given relative y-coordinate
        
        private function

        parameters:     int relative y-coordinate
        return values:  int resulting index
        """
        return (y / self._font.get_linesize()) + self._viewpoint

    def update(self, *args):
        """
        Handles the selection

        parameters: tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values: -
        """
        if len(args) > 0 and self.isActive() and self.isFocused():
            event = args[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.moveCursor(-1)
                elif event.key == pygame.K_DOWN:
                    self.moveCursor(1)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    if self.isEditable():
                        if self._selection == self._cursor:
                            self.delete(self._selection - 1, CURSOR)
                            self.moveCursor(-1)
                        else:
                            self.delete(SELECTION, CURSOR)
                            self.setCursor(self._selection)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    if self.rect.collidepoint(event.pos):
                        self.setSelection(CURSOR, self._posToIndex(event.pos[1] - self.rect.y))
                elif event.button == 4 and self.isFocused():
                    self.moveViewpoint(-1)
                elif event.button == 5 and self.isFocused():
                    self.moveViewpoint(1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    if self.rect.collidepoint(event.pos):
                        self.setCursor(self._posToIndex(event.pos[1] - self.rect.y))
        
        super(Listbox, self).update(*args)

    def _getAppearance(self, *args):
        """
        Return the underlying Widget's appearance;
        Renders the Listbox's list and selection

        private function

        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface     = super(Listbox, self)._getAppearance(*args)
        linesize    = self._font.get_linesize()
        for n in range(self._viewpoint, len(self._list)):
            surface.blit(self._font.render(str(self._list[n]), pygame.SRCALPHA, self._foreground), (0, linesize * (n - self._viewpoint)))
        if self.isFocused():
            s, e = self._sort(CURSOR, SELECTION)
            for n in range(s, e + 1):
                selection = pygame.Surface((self._bounds.width, linesize), pygame.SRCALPHA, 32)
                selection.fill(self._selectioncolor)
                surface.blit(selection, (0, linesize * (n - self._viewpoint)))
        return surface
