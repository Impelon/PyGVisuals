# --- imports
# pygame imports
import pygame

# local imports
from .selection_text_widget import *
from ..designs import getDefaultDesign
from ..util import inherit_docstrings_from_superclass


# constants
VIEWPOINT = 'v'


class Listbox(SelectionTextWidget):

    """
    Listbox for displaying lists of multiple objects as strings.
    """

    def __init__(self, x, y, width, height, font=getDefaultDesign().font, editable=False, selection_overlay=getDefaultDesign().selection_overlay):
        """
        Initialisation of an Listbox.

        Args:
            x: An integer specifing the x-coordinate of the widget.
                This is the horizontal distance from the left reference point.
            y: An integer specifing the y-coordinate of the widget.
                This is the vertical distance from the top reference point.
            width: An integer specifing the width of the widget.
            height: An integer specifing the height of the widget.
            text: A string specifing the content of the widget.
                The default value is an empty string.
            font: A font-like object that can be interpreted by pygame.font as a Font;
                this is used as the font for rendering text.
                The default value is the global default for fonts.
            editable: A boolean indicating whether the widget's content is editable by the user.
                The default value is False, meaning it can not be edited by user-input.
            selection_overlay: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values);
                this is used as an overlay for content that has been selected.
                The default value is the global default for the selection-color.
        """
        super(Listbox, self).__init__(x, y, width, height, "", font, editable, selection_overlay)
        self._list = []
        self._viewpoint = self.cursor

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
            self.setViewpoint(index - (self.rect.h / self.font.get_linesize()))
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
        index = self.getActualIndex(index)
        self._list.append(obj)
        self.markDirty()

    def delete(self, startindex, endindex):
        startindex, endindex = self._sort(startindex, endindex)
        del self._list[startindex:endindex]
        self.markDirty()

    def getActualIndex(self, index, constrain=True):
        if index == END:
            return len(self._list)
        if index == VIEWPOINT:
            return self._viewpoint
        return super(Listbox, self).getActualIndex(index, constrain)

    def _indexToPos(self, index):
        """
        Instead of the x-coordinate from the base implementation,
        this uses the y-coordinate.

        inherit_docstring::
        """
        return self.font.get_linesize() * (index - self._viewpoint)

    def _posToIndex(self, y):
        """
        Instead of the x-coordinate from the base implementation,
        this uses the y-coordinate.

        inherit_docstring::
        """
        return (y / self.font.get_linesize()) + self._viewpoint

    def update(self, *args):
        """
        Handles the selection of content.

        inherit_docstring::
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
                        if self.selection_index == self.cursor:
                            self.delete(self.selection_index - 1, CURSOR)
                            self.moveCursor(-1)
                        else:
                            self.delete(SELECTION, CURSOR)
                            self.setCursor(self.selection_index)
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
        Renders the listbox's list and selection.

        inherit_docstring::
        """
        surface = super(Listbox, self)._getAppearance(*args)
        linesize = self.font.get_linesize()
        for n in range(self._viewpoint, len(self._list)):
            surface.blit(self._render(str(self._list[n])), (0, linesize * (n - self._viewpoint)))
        if self.isFocused():
            s, e = self._sort(CURSOR, SELECTION)
            for n in range(s, e + 1):
                selection = pygame.Surface((self.bounds.width, linesize), pygame.SRCALPHA, 32)
                selection.fill(self.selection_overlay)
                surface.blit(selection, (0, linesize * (n - self._viewpoint)))
        return surface


# inherit docs from superclass
Listbox = inherit_docstrings_from_superclass(Listbox)
