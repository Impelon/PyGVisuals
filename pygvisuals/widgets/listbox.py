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

    def __init__(self, x, y, width, height, font=getDefaultDesign().font, editable=False, validation_function=(lambda *x: True), selection_overlay=getDefaultDesign().selection_overlay):
        """
        Initialisation of an Listbox.

        Args:
            inherit_doc:: arguments
        """
        super(Listbox, self).__init__(x, y, width, height, "", font, editable, validation_function, selection_overlay)
        self._list = []
        self.viewpoint = self.cursor

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
        self.setViewpoint(self.viewpoint + int(index))

    def setCursor(self, index):
        """
        Set the Listbox's cursor-position

        parameters:     int the index the cursor should be set to
        return values:  -
        """
        if self._indexToPos(index)[1] < 0:
            self.setViewpoint(index)
        elif self._indexToPos(index)[1] > self.rect.h:
            self.setViewpoint(index - (self.rect.h / self.font.get_linesize()))
        return super(Listbox, self).setCursor(index)

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
        return "\n".join(map(str, self.list))#str(self._list)[1:-1]

    def setList(self, l):
        """
        Set the Listbox's list

        parameters:     list the list to be set
        return values:  Listbox Listbox returned for convenience
        """
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
        return 0, self.font.get_linesize() * (index - self._viewpoint)

    def _posToIndex(self, x, y):
        return (y / self.font.get_linesize()) + self._viewpoint

    def update(self, *args):
        """
        Additionally handles keyboard-input.

        inherit_doc::
        """
        if len(args) > 0 and self.isActive() and self.isFocused():
            event = args[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.moveCursor(-1)
                elif event.key == pygame.K_DOWN:
                    self.moveCursor(1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 4:
                    self.moveViewpoint(-1)
                elif event.button == 5:
                    self.moveViewpoint(1)

        super(Listbox, self).update(*args)

    def _getAppearance(self, *args):
        """
        Additionally renders the listbox's list and selection.

        inherit_doc::
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

    list = property(getList, setList)
    viewpoint = property(getViewpoint, setViewpoint)

# inherit docs from superclass
Listbox = inherit_docstrings_from_superclass(Listbox)
