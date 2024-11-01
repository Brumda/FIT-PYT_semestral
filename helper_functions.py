"""Functions that are used somewhere once and therefore would only serve as a clutter in the original file"""
from os import listdir
from os.path import isdir, isfile, join

import pygame as pg
from pytmx.util_pygame import load_pygame

from object import Tile


def flip(sprites):
    """Creates new set of sprites for the opposite direction"""
    return [pg.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprites(path, scale_factor=1):
    """Load and scale sprites from a specified path.

    This function scans subdirectories within the given path, loads all images in each subdirectory,
    scales them by the specified factor, and organizes the sprites into a dictionary.

    Parameters:
    - path (str): The path to the directory containing subdirectories with sprite images.
    - scale_factor (float, optional): The factor by which to scale the loaded sprites. Default is 1.

    Returns:
    dict: A dictionary containing sprite lists, organized by direction.
          Each key represents a direction, and the corresponding value is a list of scaled sprite images.
          Directions include '_right' and '_left' for horizontal mirroring."""

    all_sprites = {}
    dirs = [f for f in listdir(path) if isdir(join(path, f))]

    for direct in dirs:
        new_path = join(path, direct)
        images = [f for f in listdir(new_path) if isfile(join(new_path, f))]
        sprites = [pg.transform.smoothscale_by(pg.image.load(join(new_path, image)).convert_alpha(), scale_factor) for
                   image in images]
        all_sprites[direct + "_right"] = sprites
        all_sprites[direct + "_left"] = flip(sprites)

    return all_sprites


def get_single_starting_pos(tmx_data, layer_name):
    """Retrieve the starting position off a first occurrence from a specified layer in TMX map data.

    This function takes TMX map data and a layer name as input, retrieves the first object's position
    from that layer, and returns the x and y coordinates as a tuple representing the starting position.

    Parameters:
    - tmx_data (TMXData): The TMX map data containing information about layers and objects.
    - layer_name (str): The name of the layer containing the starting position.

    Returns:
    tuple: A tuple containing the x and y coordinates of the starting position."""
    pos = tmx_data.get_layer_by_name(layer_name)[0]
    return pos.x, pos.y


def get_multiple_starting_pos(tmx_data, layer_name):
    """Retrieve the starting position from a specified layer in TMX map data.

        This function takes TMX map data and a layer name as input, retrieves the first object's position
        from that layer, and returns the x and y coordinates as a tuple representing the starting position.

        Parameters:
        - tmx_data (TMXData): The TMX map data containing information about layers and objects.
        - layer_name (str): The name of the layer containing the starting position.

        Returns:
        list: A list of tuples containing the x and y coordinates of the starting positions."""
    positions = []
    for pos in tmx_data.get_layer_by_name(layer_name):
        positions.append((pos.x, pos.y))
    return positions


def get_collisions(tmx_data, layer_name):
    """Extract collision data from TMX map data.

    This function takes TMX map data as input. It then iterates through the objects in each layer,
     creating Tile objects representing collision elements.

    Parameters:
    - tmx_data (TMXData): The TMX map data containing information about layers and objects.
    - layer_name (str): The name of the layer containing the collision.

    Returns:
    dict: A list containing Tile objects."""

    collisions = []
    for obj in tmx_data.get_layer_by_name(layer_name):
        collisions.append(Tile(obj.x, obj.y, obj.width, obj.height))
    return collisions


def load_levels(path):
    """Load levels from a specified directory path.

    This function takes a directory path as input, scans for files with a '.tmx' extension,
    and loads each level using the 'load_pygame' function.

    Parameters:
    - path (str): The path to the directory containing '.tmx' files representing levels.

    Returns:
    list: A list of loaded levels, each represented by the output of the 'load_pygame' function."""

    return [load_pygame(join(path, lvl)) for lvl in listdir(path) if
            isfile(join(path, lvl)) and lvl.endswith(".tmx")]


def draw_text(font_name, text, size, color, x, y, window, font=None):
    """Draws text to the screen"""
    if not font:
        font = pg.font.SysFont(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(midtop=(x, y))
    window.blit(text_surface, text_rect)


def wait_for_key():
    """Loop used in starting and end screen"""
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and (event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN):
                return "running"
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return "quit"
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                return "restart"
