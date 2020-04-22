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
        Set the widget's viewpoint-position.

        Args:
            index: An integer (or known constant) representing the index the viewpoint should be set to.

        Returns:
            Itsself (the widget) for convenience.
        """
        self._viewpoint = self.getActualIndex(index)
        self.markDirty()
        return self

    def moveViewpoint(self, index):
        """
        Move the widget's viewpoint-position by the given amount.

        Args:
            amount: An integer representing the amount the viewpoint should be moved by.

        Returns:
            Itsself (the widget) for convenience.
        """
        return self.setViewpoint(self.viewpoint + int(index))

    def getViewpoint(self):
        """
        Return the widget's viewpoint-position.

        Returns:
            An integer representing the index the viewpoint is at.
        """
        return self._viewpoint

    def setCursor(self, index):
        if self._indexToPos(index)[1] < 0:
            self.setViewpoint(index)
        elif self._indexToPos(index)[1] > self.rect.h:
            self.setViewpoint(index - (self.rect.h / self.font.get_linesize()))
        return super(Listbox, self).setCursor(index)

    def setText(self, text):
        """
        Set the listbox's text; any given text will be ignored; use insert or delete instead.

        inherit_doc::
        """
        return self

    def getText(self):
        return "\n".join(map(str, self.list))

    def setList(self, list):
        """
        Set the widget' list-representation of its content.

        Args:
            list: A list with the content to set.

        Returns:
            Itsself (the widget) for convenience.
        """
        self._list = list
        self.markDirty()
        return self

    def getList(self):
        """
        Return the widget' list-representation of its content.

        Returns:
            A list representing the content of the widget.
        """
        return self._list

    def insert(self, index, text):
        """
        inherit_doc::

        Note: The argument 'text' can be any object, not only strings.
        """
        index = self.getActualIndex(index)
        self._list.append(text)
        self.markDirty()

    def delete(self, start, end):
        start, end = self._sort(start, end)
        del self._list[start:end]
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

    list = property(getList, setList, doc="""The widget' list-representation of its content.""")
    viewpoint = property(getViewpoint, setViewpoint, doc="""The widget's position of the viewpoint as a index. This is the first currently visible index.""")

# inherit docs from superclass
Listbox = inherit_docstrings_from_superclass(Listbox)
