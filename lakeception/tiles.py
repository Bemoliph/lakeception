# -*- coding: utf-8 -*-

from colorsys import hsv_to_rgb, rgb_to_hsv
import random

from lakeception.lakeutils import hex2rgb

# Nice Tile Graveyard (nice tiles you found but don't know what to do with)
# Tile("?", "a mysterious secret", "0", "333333")
# Tile("unknown", "something unknown", "!", "B65555")

class Tile(object):
    def __init__(self, name, description, glyphs, color, adjacentTiles=None, collidable=False):
        self.name = name
        self.description = description
        self.adjacentTiles = adjacentTiles

        self.glyph = random.choice(glyphs)
        self.allGlyphs = glyphs
        self.color = hex2rgb(color)

        self.is_collidable = collidable
        self.elevation = -1
        self.biomeID = -1

        self._hsvComponents = {"hue": 0, "saturation": 1, "brightness": 2}


    def setColor(self, hsv):
        # Apply the lambda function to every element of hsv, yielding the new
        # tuple normalizedHSV
        normalizedHSV = map(lambda hsvElement: hsvElement / 100.0, hsv)
        color = hsv_to_rgb(*normalizedHSV)
        color = tuple(map(lambda rgbElement: int(rgbElement * 255), color))
        self.color = color


    def getHSV(self):
        rgbColor = map(lambda rgbElement: rgbElement / 255.0, self.color)
        hsvColor = list(rgb_to_hsv(*rgbColor))
        # Hue
        hsvColor[0] *= 360
        # Saturation
        hsvColor[1] *= 100
        # Brightness
        hsvColor[2] *= 100
        return map(int, hsvColor)


    # Also called 'value', thus HSV; but I think brightness is easier to understand
    def setBrightness(self, brightness):
        brightness /= 100.0
        self._setHSVComponent("brightness", brightness)


    def setHue(self, hue):
        hue /=  360.0
        self._setHSVComponent("hue", hue)


    def setSaturation(self, saturation):
        saturation /= 100.0
        self._setHSVComponent("saturation", saturation)


    def _setHSVComponent(self, component, componentValue):
        index = self._hsvComponents[component]
        # Convert to HSV
        rgbColor = map(lambda rgbElement: rgbElement / 255.0, self.color)
        hsvColor = list(rgb_to_hsv(*rgbColor))
        # Set the value of the specified component
        hsvColor[index] = componentValue
        # Convert back to RGB
        rgbColor = hsv_to_rgb(*hsvColor)
        rgbColor = tuple(map(lambda rgbElement: int(rgbElement * 255), rgbColor))
        # Set the tile's color
        self.color = rgbColor


    def __unicode__(self):
        return self.glyph


    def __repr__(self):
        return self.__unicode__()


    def hasAdjacencyRequirement(self):
        return self.adjacentTiles and len(self.adjacentTiles) > 0


    def __hash__(self):
        return hash((self.glyph, self.color, self.biomeID, self.elevation))


    def __eq__(self, other):
        return (self.glyph, self.color, self.biomeID, self.elevation) == \
            (other.glyph, other.color, other.biomeID, other.elevation)
