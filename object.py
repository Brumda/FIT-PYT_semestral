"""Objects from the game"""
import pygame as pg

from constants import TILE_SIZE


class Object(pg.sprite.Sprite):
    """
        A base class for game objects.

        This class extends Pygame's Sprite class and provides a basic structure for game objects.

        Attributes:
        - rect (pygame.Rect): A rectangular collision area for the object.
        - image (pygame.Surface): The surface representing the appearance of the object.
        - width (int): The width of the object.
        - height (int): The height of the object.

        Methods:
        - draw(win, offset): Draw the object on a Pygame surface, adjusted by the specified offset."""

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.width = width
        self.height = height

    def draw(self, win, offset):
        """
        Draw the object on a Pygame surface with an offset.

        Parameters:
        - win (pygame.Surface): The Pygame surface on which to draw the object.
        - offset (tuple): A tuple representing the offset in (x, y) coordinates for drawing."""

        win.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))


class Tile(Object):
    """Object for all the tiles. Used only for collisions"""

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.rect = self.rect = pg.Rect(x, y, width, height)
        self.mask = pg.mask.Mask((width, height), True)


class Door(Object):
    """Doors to another level. Has two states: opened and closed."""

    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.rect = self.rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.mask = pg.mask.Mask((TILE_SIZE, TILE_SIZE), True)
        self.sprite_closed = pg.image.load("assets/medieval-tileset/Objects/door1.png").convert_alpha()
        self.sprite_opened = pg.image.load("assets/medieval-tileset/Objects/door2.png").convert_alpha()
        self.image = self.sprite_closed
        self.opened = False
        self.close()

    def open(self):
        """Opens the door"""
        self.opened = True
        self.image = self.sprite_opened

    def close(self):
        """Closes the door"""
        self.opened = False
        self.image = self.sprite_closed


class Lever(Object):
    """
    Levers that the player needs to pull in order to open the doors to another level
    """

    def __init__(self, x, y):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.rect = self.rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.mask = pg.mask.Mask((TILE_SIZE, TILE_SIZE), True)
        self.sprite_closed = pg.image.load("assets/medieval-tileset/Objects/lever1.png").convert_alpha()
        self.sprite_opened = pg.image.load("assets/medieval-tileset/Objects/lever2.png").convert_alpha()
        self.image = self.sprite_closed
        self.used = False

    def use(self):
        """Switches mode upon player activation"""
        if self.used:
            self.image = self.sprite_closed
        else:
            self.image = self.sprite_opened
        self.used = not self.used
