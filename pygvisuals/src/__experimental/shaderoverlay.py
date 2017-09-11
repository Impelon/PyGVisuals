# -*- coding: cp1252 -*-

import pygame

class ShaderOverlay():

    """
    Manager for creating a surface with shadows/lightsources
    """

    def __init__(self, background = (0, 0, 0), positionmap = None):
        """
        Initialisation of a ShaderOverlay

        parameters:     -
        return values:  -
        """
        self._lightsources  = dict()
        self._background    = background
        try:
            positionmap.isPositionValid(0, 0)
            self._map = positionmap
        except:
            self._map = None

    def setBackground(self, color):
        """
        Set the ShaderOverlay's background-color

        parameters:     tuple a tuple of format pygame.Color representing the color to be set
        return values:  -
        """
        self._background = color

    def getBackground(self):
        """
        Return the ShaderOverlay's background-color

        parameters:     -
        return values:  tuple of format pygame.Color representing the Widget's foreground-color
        """
        return self._background

    def setPositionMap(self, positionmap):
        """
        Set the PositionMap to represent opaque positions

        parameters:     PositionMap the PositionMap to represent opaque positions
        return values:  -
        """
        try:
            positionmap.isPositionValid(0, 0)
            self._map = positionmap
        except:
            pass

    def getPositionMap(self, positionmap):
        """
        Return the PositionMap that represenst opaque positions

        parameters:     -
        return values:  PositionMap the PositionMap to represent opaque positions
        """
        return self._map

    def addLightsource(self, obj, radius, color = (255, 255, 255), intensity = 255, quality = 10):
        """
        Add a given object as a colored lightsource with specific radius

        parameters:     object the lightsource to add (must have an attribute called 'rect' that is a pygame.Rect)
                        int radius of the lightsource (in pixel)
                        tuple tuple of format pygame.Color representing the color of the lightsource (alpha will be ignored)
                        int intensity of the lightsource (min 0, max 255); corresponds to the initial alpha value
        return values:  -
        """
        try:
            self._lightsources[obj] = (abs(int(radius)), color[:3], max(min(intensity, 255), 0), abs(int(quality)))
        except:
            pass

    def removeLightsource(self, obj):
        """
        Add a given object as a colored lightsource with specific radius

        parameters:     object the lightsource to remove
        return values:  boolean if the lightsource has been removed succesfully
        """
        try:
            del self._lightsources[obj]
            return True
        except:
            return False

    def raycast(self, pos, dest, rect, steps):
        """
        Return a point that results form casting a ray between the given points to check for collisions

        parameters:     tuple tuple representing the starting-point
                        tuple tuple representing the destination-point
                        pygame.Rect Bounderies of the Check
                        int number of steps to check between the points
        return values:  tuple tuple representing the point of first collision
        """
        directionX = (pos[0] - dest[0]) / float(steps)
        directionY = (pos[1] - dest[1]) / float(steps)
        x, y = pos
        for i in xrange(steps):
            x += directionX
            y += directionY
            if x < rect.x or x > rect.w:
                break
            if y < rect.y or y > rect.h:
                break
            if self._map and not self._map.isPositionValid(int(x), int(y)):
                break
        return (int(x), int(y))

    def getOverlay(self, rect):
        """
        Draw the ShaderOverlay and return the result

        parameters:     pygame.Rect bounds of the Overlay
        return values:  pygame.Surface the result
        """
        try:
            surface = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
        except:
            return pygame.Surface((0, 0), pygame.SRCALPHA, 32)
        surface.fill(self._background)
        
        shapes          = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
        lightsources    = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
        removeAfter     = []

        for ls in self._lightsources:
            quality     = self._lightsources[ls][3]
            intensity   = self._lightsources[ls][2]
            color       = self._lightsources[ls][1]
            radius      = self._lightsources[ls][0]
            r           = ls.rect

            polygon = []
            try:
                for x in xrange(1, 2 * radius + r.w, quality):
                    polygon.append(self.raycast(r.center, (r.left - radius + x, r.top - radius), rect, radius))
                for y in xrange(1, 2 * radius + r.h, quality):
                    polygon.append(self.raycast(r.center, (r.right + radius, r.top - radius + y), rect, radius))
                for x in xrange(1, 2 * radius + r.w, quality):
                    polygon.append(self.raycast(r.center, (r.right + radius - x, r.bottom + radius), rect, radius))
                for y in xrange(1, 2 * radius + r.h, quality):
                    polygon.append(self.raycast(r.center, (r.left - radius, r.bottom + radius - y), rect, radius))
            except:
                removeAfter.append(ls)
            
            if polygon:
                pygame.draw.polygon(shapes, color, polygon)

            gradient = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
            try:
                for n in range(2 * radius, 0, -1):
                    alpha = intensity - int(intensity * (float(n) / (2 * radius)))
                    pygame.draw.ellipse(gradient, color + (alpha,), r.inflate(n, n))
            except:
                removeAfter.append(ls)

            shapes.blit(gradient, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
            lightsources.blit(shapes, (0, 0), special_flags = pygame.BLEND_RGBA_MAX)
        surface.blit(lightsources, (0, 0))

        for ls in removeAfter:
            self.removeLightsource(ls)
            
        return surface
