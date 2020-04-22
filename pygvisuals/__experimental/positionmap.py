# --- imports
# pygame imports
import pygame

def createByImage(path):
    """
    Create a PositionMap by using a imagefile
    pixels with RGB-values of 0 (black) will be interpreted as invalid positions aka. obstacles

    parameter:      string path leading to the imagefile
    return values:  PositionMap the result
    """
    try:
        mapdata = pygame.image.load(path)
    except:
        m = PositionMap()
        m.setWidth(1)
        m.setHeight(1)
        return m
    return createBySurface(mapdata)

def createBySurface(surface):
    """
    Create a PositionMap by using a Surface
    pixels with RGB-values of 0 (black) will be interpreted as invalid positions aka. obstacles

    parameter:      pygame.Surface the surface to interpret
    return values:  PositionMap the result
    """
    m       = PositionMap()
    invalid = set()
    size    = surface.get_size()
    black   = surface.map_rgb((0, 0, 0))
    surface = pygame.PixelArray(surface)
    m.setWidth(size[0])
    m.setHeight(size[1])
    for x in range(size[0]):
        for y in range(size[1]):
            try:
                if surface[x][y] == black:
                    invalid.add((x, y))
            except:
                pass
    m._invalidPositions = frozenset(invalid)
    return m

def createByList(l = []):
    """
    Create a PositionMap by using a list of strings
    the length of each list element (string) and the length of the list correspond to the width and height of the PositionMap respectively
    all characters except spaces will be interpreted as invalid positions aka. obstacles

    parameter:      list list of strings following the described format
    return values:  PositionMap the result
    """
    m       = PositionMap()
    invalid = set()
    w       = 0
    if not l:
        m.setWidth(1)
        m.setHeight(1)
        return m
    for y in range(len(l)):
        ln = str(l[y])
        for x in range(len(ln)):
            if ln[x] != " ":
                invalid.add((x, y))
        if len(ln) > w:
            w = len(ln)
    m.setWidth(w)
    m.setHeight(len(l))
    m._invalidPositions = frozenset(invalid)
    return m

def scale(m, scale = 1):
    """
    Scale a PositionMap with a scalar (out-of-place)

    parameter:      PositionMap the PositionMap, which should be scaled
                    int/tuple the scalar or a tuple containing a scalar for each dimension
    return values:  PositionMap the result
    """
    try:
        scaleX = abs(scale[0])
        scaleY = abs(scale[1])
    except:
        scaleX = abs(scale)
        scaleY = abs(scale)
    resolution = (int(m.getWidth() * scaleX), int(m.getHeight() * scaleY))
    return createBySurface(pygame.transform.scale(m.toSurface(), resolution))


class PositionMap:

    """
    Class for a map of valid and invalid positions aka. obstacles
    """

    def __init__(self):
        """
        Initialisation of a PositionMap

        parameter:      -
        return values:  -
        """
        self._width     = 0
        self._height    = 0
        self._invalidPositions = frozenset()

    def getWidth(self):
        """
        Return the width of the PositionMap

        parameter:      -
        return values:  int width of the PositionMap
        """
        return self._width

    def getHeight(self):
        """
        Return the height of the PositionMap

        parameter:      -
        return values:  int height of the PositionMap
        """
        return self._height

    def getLengthInvalidPositions(self):
        """
        Return the amount of invalid positions of the PositionMap

        parameter:      -
        return values:  int amount of invalid positions of the PositionMap
        """
        return len(self._invalidPositions)

    def setWidth(self, width):
        """
        Set the width of the PositionMap, in case it has not been set yet

        parameter:      int width of the PositionMap
        return values:  -
        """
        if not self._width:
            self._width = int(width)

    def setHeight(self, height):
        """
        Set the height of the PositionMap, in case it has not been set yet

        parameter:      int height of the PositionMap
        return values:  -
        """
        if not self._height:
            self._height = int(height)

    def isPositionValid(self, x, y):
        """
        Return if a position is valid according to the PositionMap, aka. if there are any obstacles

        parameter:      int x-coordinate of the position to check
                        int y-coordinate of the position to check
        return values:  bool whether the position is valid according to the PositionMap
        """
        if x >= self._width:
            return False
        if y >= self._height:
            return False
        if x < 0:
            return False
        if y < 0:
            return False
        return not (x, y) in self._invalidPositions

    def isRectValid(self, rect):
        """
        Return if an area/rect is completely valid according to the PositionMap, aka. if there are any obstacles inside the rect

        parameter:      pygame.Rect the area/rect to check
        return values:  bool whether the area/rect is completely valid according to the PositionMap
        """
        for x in range(rect.width):
            for y in range(rect.height):
                if not self.isPositionValid(x + rect.x, y + rect.y):
                    return False
        return True

    def toSurface(self):
        """
        Return a Surface representing the PositionMap
        invalid positions will be represented by pixels with RGB-values of 0 (black)
        valid positions ill be represented by pixels with RGB-values of 255 (white)

        parameter:      -
        return values:  pygame.Surface the result
        """
        surface = pygame.Surface((self.getWidth(), self.getHeight()), 0, 8)
        surface.fill((255, 255, 255))
        black   = surface.map_rgb((0, 0, 0))
        mapdata = pygame.PixelArray(surface)
        for pos in self._invalidPositions:
            try:
                mapdata[pos[0]][pos[1]] = black
            except:
                pass
        return surface
