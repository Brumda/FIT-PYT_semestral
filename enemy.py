"""Enemy class"""
from random import randint

import pygame as pg
from pygame import mixer

from constants import ANIMATION_DELAYS_ENEMY, FPS
from creature import Creature


class Enemy(Creature):
    """Class that represents the enemies. Handles all the movement, aggro state, timers when the enemy does something.
    Most of the timers, and some other features, are selected randomly from specified range"""

    def __init__(self, x, y, boundaries, move_chance):
        super().__init__("assets/SkeletonEnemy", x, y, 2.3, 2, 1, 64, 48,
                         "assets/sound/wraith_pain.wav", "assets/sound/wraith_death.wav", 1.5 * FPS)
        self.direction = "right" if randint(0, 1) else "left"
        self.speed = randint(1, 2)
        self.boundaries = boundaries
        self.move_chance = move_chance
        self.walking = 0
        self.detection_range = randint(300, 500)
        self.aggro_timer = 0
        self.aggro_state = "chilling"
        self.turn_cooldown = randint(int(.5 * FPS), 1 * FPS)
        self.turn_cooldown_timer = 0

        self.attack_sound = mixer.Sound('assets/sound/slash.mp3')

    def move(self):
        """Moves the enemy between predefined boundaries"""
        self.change_state("Walk")
        for obj in self.boundaries:
            if pg.sprite.collide_rect(self, obj):
                self.turn_around()
                break
        self.rect.x += self.speed if self.direction == "right" else -self.speed

    def turn_around(self):
        """Turns the enemy around"""
        self.turn_cooldown_timer = -42
        self.direction = "right" if self.direction == "left" else "left"

    def check_for_player(self, player_pos):
        """Checks if the player is close enough to engage. When the player is behind the enemy,
        the detection range is smaller. If the player is detected, timer for turning around is started,
        so the enemy doesn't 180 noscope the player. If the enemy is close enough, tries to bonk the player"""
        distance = self.rect.centerx - player_pos
        self.aggro_state = "chilling"
        if (self.direction == "left" and (
                0 <= distance < self.detection_range or -self.detection_range * .6 < distance <= 0) or
                (self.direction == "right" and (
                        0 <= distance < self.detection_range * .6 or -self.detection_range < distance <= 0))):

            self.aggro_state = "reeeeeeeeee"
            self.aggro_timer = randint(2 * FPS, 5 * FPS)
            if (self.direction == "left" and distance < 0) or (self.direction == "right" and distance > 0):
                if self.turn_cooldown_timer < 0:
                    self.turn_cooldown_timer = self.turn_cooldown
        if abs(distance) < 50 and self.attack_cooldown_timer == 0:
            self.change_state("Attack")
            self.attack_sound.play()
            self.attack_cooldown_timer = self.attack_cooldown
            self.can_change_state = False

    def draw(self, win, offset):
        """Draws the enemy and his life bar on the screen"""
        super().draw(win, offset)
        if self.lives > 0 and self.aggro_state == "reeeeeeeeee":
            x = self.rect.centerx - offset[0] - 50
            y = self.rect.centery - offset[1] - 50
            pg.draw.rect(win, (255, 0, 0), (x, y, self.rect.width * .7, 10))
            pg.draw.rect(win, (0, 180, 0), (x, y, (self.rect.width * .7) * (self.lives / self.max_lives), 10))

    def loop(self):
        """Enemy loop. Changes the animation, moves the enemy in random intervals for random amount of time
         and ticks down timers"""
        super().loop()
        self.animation(ANIMATION_DELAYS_ENEMY)

        if self.lives > 0 and self.can_change_state:
            if self.aggro_state == "reeeeeeeeee":
                self.aggro_timer -= 1
                if self.aggro_timer == 0:
                    self.aggro_state = "chilling"
                self.move()
                self.walking = 0
            elif self.walking > 0:
                self.walking = max(0, self.walking - 1)
                self.move()
            elif randint(0, 100) > self.move_chance:
                self.walking = randint(int(.5 * FPS), 2 * FPS)
            else:
                self.change_state("Idle")
        if self.turn_cooldown_timer > 0:
            self.turn_cooldown_timer -= 1
        elif self.turn_cooldown_timer == 0:
            self.turn_around()
