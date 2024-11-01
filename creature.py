"""Creature class"""

import pygame as pg
from pygame import mixer

from constants import FPS, GRAVITY, INVINCIBLE_DURATION
from helper_functions import load_sprites


class Creature(pg.sprite.Sprite):
    """Default class both for player and enemies. Has everything related to animations, collisions, stats and
    handles everything that the two creatures have in common"""

    def __init__(self, path, x, y, scale, max_lives, damage, width, height, hurt_sound_path, death_sound_path,
                 attack_cooldown=FPS):
        super().__init__()
        # there is no way I can reduce this to just 7 variables like pylint wants without using self.vars = {...}
        # animations & collisions
        self.SPRITES = load_sprites(path, scale)
        self.animation_count = 0
        self.sprite = None
        self.state = "Idle"
        self.can_change_state = True
        self.direction = "right"
        self.rect = pg.Rect(x, y, width, height)
        self.mask = pg.mask.Mask
        # stats
        self.lives = max_lives
        self.max_lives = max_lives
        self.damage = damage
        self.velocity = pg.Vector2(0, 0)
        self.invincible = 0
        self.attack_cooldown_timer = 0
        self.attack_cooldown = attack_cooldown
        # sounds
        self.hurt_sound = mixer.Sound(hurt_sound_path)
        self.death_sound = mixer.Sound(death_sound_path)

    def change_state(self, new_state, override=False):
        """Changes state of creature if possible. States are mainly used for animations"""
        if new_state != self.state and (self.can_change_state or override):
            self.animation_count = 0
            self.state = new_state

    def get_hit(self, amount):
        """Handles what happens when the creature is hit"""
        if not self.invincible:
            self.change_state("Hurt", True)
            self.can_change_state = False
            self.invincible = INVINCIBLE_DURATION
            self.hurt_sound.play(maxtime=int(1000))
            self.lives -= amount

        if self.lives <= 0:
            self.die()

    def die(self):
        """Makes the creature legally dead"""
        if self.state == "Hurt":
            self.hurt_sound.stop()
            self.death_sound.play(maxtime=int(1000))
        self.change_state("Die", True)
        self.can_change_state = False
        self.lives = -42

    def animation(self, delays):
        """Loops the animations based on creature state and direction. When an animation is finished
        the creature can change states again"""

        sprite_sheet_name = self.state + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // delays[self.state]) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        if sprite_index == len(sprites) - 1:
            self.can_change_state = True
        self.update()

    def update(self):
        """Updates the creature's position and collision mask"""
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(self.sprite)

    def draw(self, win, offset):
        """Draws the creature into the game"""
        win.blit(self.sprite, (self.rect.x - offset[0], self.rect.y - offset[1]))

    def landed(self):
        """When hitting the ground, resets the y velocity"""
        self.velocity.y = 0

    def loop(self):
        """Creature loop adds gravity and ticks down more timers"""
        self.velocity.y += GRAVITY * 1.5 / FPS
        self.rect.y += self.velocity.y
        if self.invincible:
            self.invincible -= 1
        if self.attack_cooldown_timer:
            self.attack_cooldown_timer -= 1
