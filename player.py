"""Player class"""
import pygame as pg
from pygame import mixer

from constants import ANIMATION_DELAYS_PLAYER, FPS, GRAVITY, HEIGHT, NO_MOVING, PLAYER_SPEED, WIDTH
from creature import Creature


class Player(Creature):
    """Class that represents the player. Handles the inputs and all the movement"""

    def __init__(self, max_lives, damage, x, y):
        super().__init__("assets/Adventurer", x, y, 2, max_lives, damage, 50, 37,
                         "assets/sound/male_hurt.mp3", "assets/sound/male_hurt.mp3", 1 * FPS)
        self.jumping = 0
        self.using_stuff = False
        self.using_stuff_cooldown = 0
        # sound effects
        self.run_sound = mixer.Sound("assets/sound/footsteps.wav")
        self.leg_breaking = mixer.Sound("assets/sound/brokenleg.wav")
        self.attack_sound = mixer.Sound("assets/sound/player_attack.wav")
        # volume changes
        self.run_sound.set_volume(.6)
        self.leg_breaking.set_volume(.6)
        self.attack_sound.set_volume(.4)
        self.hurt_sound.set_volume(.4)

    def get_input(self, walls):
        """Handles teh player inputs and calls the corresponding methods"""
        self.velocity.x = 0
        keys = pg.key.get_pressed()
        collide_left = self.try_move(walls, -PLAYER_SPEED * 2)
        collide_right = self.try_move(walls, PLAYER_SPEED * 2)
        if keys[pg.K_RIGHT] and self.state not in NO_MOVING and not collide_right:
            self.direction = "right"
            self.move(PLAYER_SPEED)
        elif keys[pg.K_LEFT] and self.state not in NO_MOVING and not collide_left:
            self.direction = "left"
            self.move(-PLAYER_SPEED)
        elif keys[pg.K_SPACE] and self.state not in NO_MOVING and not self.attack_cooldown_timer:
            self.attack()
        elif keys[pg.K_DOWN] and not self.using_stuff_cooldown:
            self.using_stuff = True
            self.using_stuff_cooldown = .5 * FPS
        else:
            self.change_state("Idle")

    def move(self, vel):
        """Moves the player in the x-axis. Kinda useless, but future-proof"""
        if self.state == "Idle":
            self.run_sound.play(-1)
        self.velocity.x += vel

    def try_move(self, walls, dx):
        """Method that calculates, if the player can move in the next few frames and
        returns the objects he would collide with"""

        self.rect.x += dx
        self.update()
        collided_object = None
        for obj in walls:
            if pg.sprite.collide_mask(self, obj):
                collided_object = obj
                break
        self.rect.x -= dx
        self.update()
        return collided_object

    def landed(self):
        """Handles what happens when the player hits the ground"""
        if self.velocity.y > 1 * GRAVITY:
            self.die()
        elif self.velocity.y > .7 * GRAVITY:
            self.leg_breaking.play()
            self.get_hit(1)
        if self.velocity.y > 4:
            self.run_sound.play()
        super().landed()
        self.jumping = 0

    def hit_head(self):
        """Handles what happens when the player hits his head"""
        self.velocity.y *= -.2

    def attack(self):
        """Sets the player attack cooldown and changes the state. The collisions are resolved in the Game class"""
        self.attack_sound.play()
        self.attack_cooldown_timer = self.attack_cooldown
        self.change_state("Attack")
        self.can_change_state = False

    def jump(self):
        """Makes the player jump or double jump"""
        if self.state not in NO_MOVING:
            self.change_state("Jump")
            self.velocity.y = -GRAVITY * 24 // FPS
            self.jumping += 1
            if self.jumping == 2:
                self.change_state("Double_jump")
                self.can_change_state = False

    def draw(self, win, offset):
        """Draws the player and his life bar on the screen"""
        super().draw(win, offset)
        pg.draw.rect(win, (255, 0, 0), (10, 10, WIDTH * .3, 10))
        pg.draw.rect(win, (0, 180, 0), (10, 10, WIDTH * .3 * (self.lives / self.max_lives), 10))

    def loop(self):
        """Player loop. Adds the velocity to the player's position. Checks if player fell out of the map,
         ticks down timers, plays the animation"""
        super().loop()
        self.rect.x += self.velocity.x
        if self.rect.y > HEIGHT:
            self.die()
        if self.velocity.y > GRAVITY * .15:
            self.change_state("Fall")
            if self.jumping == 0:
                self.jumping = 42
        if self.velocity.x != 0 and self.velocity.y < 4:
            self.change_state("Run")
        if self.state != "Run":
            self.run_sound.stop()
        if self.using_stuff_cooldown:
            self.using_stuff_cooldown -= 1
        self.animation(ANIMATION_DELAYS_PLAYER)
