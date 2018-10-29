# -*- coding: cp1252 -*-

import textwidget
import pygame

START       = 0
END         = 'e'
CURSOR      = 'c'
INSERT      = CURSOR
CURRENT     = CURSOR
SELECTION   = 's'

defaultSelection = (45, 110, 235, 120)

class SelectionTextWidget(textwidget.TextWidget):

    """
    Underlying class for Widgets using selectable text/strings with a cursor;
    """
    
    def __init__(self, x, y, width, height, text = "", font = textwidget.defaultFont, selectioncolor = defaultSelection):
        """
        Initialisation of a SelectionTextWidget

        parameters:     int x-coordinate of the SelectionTextWidget (left)
                        int y-coordinate of the SelectionTextWidget (top)
                        int width of the SelectionTextWidget
                        int height of the SelectionTextWidget
                        string test of the SelectionTextWidget
                        pygame.font.Font font of the SelectionTextWidget
                        tuple of format pygame.Color representing the SelectionTextWidget's selection-color
        return values:  -
        """
        super(SelectionTextWidget, self).__init__(x, y, width, height, text, font)
        self._cursor            = 0
        self._selection         = 0
        self._selectioncolor    = selectioncolor

    def setSelectionColor(self, color):
        """
        Set the SelectionTextWidget's selection-color

        parameters:     tuple a tuple of format pygame.Color representing the color to be set
        return values:  Widget Widget returned for convenience
        """
        self._selectioncolor = color
        self.markDirty()
        return self

    def getSelectionColor(self):
        """
        Return the SelectionTextWidget's selection-color

        parameters:     -
        return values:  tuple of format pygame.Color representing the SelectionTextWidget's selection-color
        """
        return self._selectioncolor

    def setCursor(self, index):
        """
        Set the SelectionTextWidget's cursor-position

        parameters:     int the index the cursor should be set to
        return values:  -
        """
        self.setSelection(index, index)

    def getCursor(self):
        """
        Return the SelectionTextWidget's cursor-position

        parameters:     -
        return values:  int the SelectionTextWidget's cursor-position
        """
        return self._cursor

    def moveCursor(self, index):
        """
        Move the SelectionTextWidget's cursor-position by the given amount

        parameters:     int the amount the cursor should be moved by
        return values:  -
        """
        self.setCursor(min(max(self.getActualIndex(CURSOR) + int(index), 0), self.getActualIndex(END)))
        
    def setSelection(self, start, end):
        """
        Set the SelectionTextWidget's selection between the given bounds

        parameters:     int the index the selection should start
                        int the index the selection should end (cursor)
        return values:  -
        """
        self._selection = self.getActualIndex(start)
        self._cursor    = self.getActualIndex(end)
        self.markDirty()

    def getSelection(self):
        """
        Return the SelectionTextWidget's selection

        parameters:     -
        return values:  int the startindex of the selection
                        int the endindex of the selection
        """
        return self._sort(self._selection, self._cursor)

    def getActualIndex(self, index):
        """
        Return the actual index corresponding to the given index-representation

        parameters:     object object representing the index
        return values:  int the actual index of the SelectionTextWidget's text
        """
        if index == CURSOR:
            return self._cursor
        if index == END:
            return len(self._text)
        if index == SELECTION:
            return self._selection
        return abs(int(index))

    def _indexToPos(self, index):
        """
        Return the relative x-coordinate corresponding to the given index

        private function

        parameters:     int index given
        return values:  int relative x-coordinate
        """
        return self._font.size(self._text[:self.getActualIndex(index)])[0]

    def _posToIndex(self, x):
        """
        Return the index corresponding to the given relative x-coordinate
        
        private function

        parameters:     int relative x-coordinate
        return values:  int index given
        """
        length  = len(self._text)
        x       = min(float(x), (self._font.size(self._text[:-1])[0]
                                 + self._font.size(self._text[-1:])[0] * 1.5))
        index   = 0
        n       = 0
        if self._text:
            for n in xrange(max(min(int(x / (self._font.size(self._text)[0] / length)), length - 1), 0), 0, -1):
                if self._font.size(self._text[:n])[0] + self._font.size(self._text[n])[0] < x:
                    break
            for index in xrange(n, length):
                if self._font.size(self._text[:index])[0] + (self._font.size(self._text[index])[0] * 1.5) > x:
                    break
            else:
                index += 1
        return index

    def _sort(self, i, n):
        """
        Return the indices in ascending order
        
        private function

        parameters:     int an index
                        int another index
        return values:  int the first index
                        int the second index
        """
        i = self.getActualIndex(i)
        n = self.getActualIndex(n)
        if i > n:
            return n, i
        return i, n
