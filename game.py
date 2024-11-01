"""The main game class"""
from random import randint

import pygame as pg
from pygame import mixer

from constants import HEIGHT, TILE_SIZE, TUTORIAL, WIDTH
from enemy import Enemy
from helper_functions import draw_text, get_collisions, get_multiple_starting_pos, get_single_starting_pos, wait_for_key
from object import Door, Lever
from player import Player


class Game:
    """The game class. Draws everything to screen, manages all the game logic, player, enemies, some collisions,
    winning conditions etc."""

    def __init__(self, level_data, window):
        # everything the game class takes care of
        self.window = window
        self.camera_offset = [0, 0]
        self.collisions = {"floor": [], "walls": [], "roof": []}
        self.draw_order = []
        self.boundaries = []
        self.enemies = []
        self.exit = None
        self.levers = []

        # sounds
        mixer.music.load("assets/sound/background_music.wav")
        mixer.music.play(-1)
        mixer.music.set_volume(.4)
        self.lever_pull_sound = mixer.Sound("assets/sound/button_click.wav")
        self.lever_pull_sound.set_volume(.6)
        self.all_levers_down = mixer.Sound("assets/sound/next_level.wav")
        self.all_levers_down.set_volume(.6)

        # setup
        x, y = get_single_starting_pos(level_data, "player")
        self.player = Player(3, 1, x, y)
        self.level_dimension = (level_data.width, level_data.height)

        self.setup_level(level_data)
        self.draw_order = [level_data.get_layer_by_name("background"),
                           level_data.get_layer_by_name("ground"),
                           level_data.get_layer_by_name("prompts")]
        self.state = ""
        self.tutorial = True

    def setup_level(self, data):
        """Sets up the level. Basically just divides init. Create collisions, exit doors, levers and enemies"""

        for key in self.collisions:
            self.collisions[key] = get_collisions(data, key)
        boundaries = get_collisions(data, "boundaries")

        x, y = get_single_starting_pos(data, "exit")
        self.exit = Door(x, y)

        for x, y in get_multiple_starting_pos(data, "enemies"):
            self.enemies.append(Enemy(x, y, boundaries, randint(97, 99)))

        for x, y in get_multiple_starting_pos(data, "levers"):
            self.levers.append(Lever(x, y))

    def camera(self):
        """Calculates the camera position in order to have the player center"""
        pivot = 0.5
        self.camera_offset[0] += (self.player.rect.centerx - self.camera_offset[0] - WIDTH * pivot) / 10
        self.camera_offset[0] = max(0, min(self.camera_offset[0], self.level_dimension[0] * TILE_SIZE - WIDTH))
        self.camera_offset[1] += (self.player.rect.centerx - self.camera_offset[1] - HEIGHT * pivot)
        self.camera_offset[1] = max(0, min(self.camera_offset[1], self.level_dimension[1] * TILE_SIZE - HEIGHT))

    def draw_game(self):
        """Draws everything in the game except enemies.
        If the tutorial is active, displays a little text on the screen."""

        for layer in self.draw_order:
            for x, y, tile in layer.tiles():
                self.window.blit(tile, (x * TILE_SIZE - self.camera_offset[0], y * TILE_SIZE - self.camera_offset[1]))

        for lever in self.levers:
            lever.draw(self.window, self.camera_offset)

        self.exit.draw(self.window, self.camera_offset)
        self.player.draw(self.window, self.camera_offset)

        if self.tutorial:
            font = pg.font.SysFont("Comic Sans MS", 26)
            lines = TUTORIAL.split("\n")
            y = 300
            for line in lines:
                draw_text("Comic Sans MS", line, 26, (255, 255, 255), WIDTH // 2, y, self.window, font)
                y += 30

    def handle_vertical_collision(self, creature):
        """Handles vertical collision for player and enemies.
        Since enemies don't jump, the roof is only checked for the player"""

        for obj in self.collisions["floor"]:
            if pg.sprite.collide_mask(creature, obj) and creature.velocity.y > 0:
                creature.rect.bottom = obj.rect.top
                creature.landed()
        if creature == self.player:
            for obj in self.collisions["roof"]:
                if pg.sprite.collide_mask(creature, obj) and creature.velocity.y < 0:
                    creature.rect.top = obj.rect.bottom
                    creature.hit_head()

    def check_player_attack(self):
        """When player is attacking, checks if any enemies are hit"""
        for enemy in self.enemies:
            if self.player.lives > 0 and pg.sprite.collide_mask(enemy, self.player):
                enemy.get_hit(self.player.damage)

    def check_enemy_attack(self, enemy):
        """When enemy is attacking, checks if the player is hit"""
        if self.player.lives > 0 and pg.sprite.collide_mask(enemy, self.player):
            self.player.get_hit(enemy.damage)

    def check_actions(self):
        """When player is trying to use stuff, this method checks if there is anything to use"""
        new_lever_pulled = False
        for lever in self.levers:
            if pg.sprite.collide_mask(lever, self.player):
                lever.use()
                new_lever_pulled = lever.used
                self.lever_pull_sound.play()

        if all(lever.used for lever in self.levers):
            self.exit.open()
            if new_lever_pulled:
                self.all_levers_down.play()
        else:
            self.exit.close()

        if self.exit.opened and pg.sprite.collide_mask(self.exit, self.player):
            self.state = "next"

    def run(self):
        """The game loop. Here is where the game runs and calls all the other methods"""

        self.player.loop()
        self.handle_vertical_collision(self.player)
        self.draw_game()

        self.player.get_input(self.collisions["walls"])

        if self.player.using_stuff:
            self.player.using_stuff = False
            self.check_actions()

        if self.player.state == "Attack":
            self.check_player_attack()

        for enemy in self.enemies:
            if enemy.lives <= 0 and enemy.can_change_state:
                self.enemies.remove(enemy)
                continue
            enemy.loop()
            self.handle_vertical_collision(enemy)

            if self.player.rect.bottom == enemy.rect.bottom and self.player.lives > 0:
                enemy.check_for_player(self.player.rect.centerx)

            if enemy.state == "Attack":
                self.check_enemy_attack(enemy)

            enemy.draw(self.window, self.camera_offset)

        self.camera()
        pg.display.update()

        if self.player.lives == -42 and self.player.can_change_state:
            self.state = "dead"

    def start_screen(self):
        """Instead of main menu"""
        self.window.fill((69, 0, 69))
        draw_text("Comic Sans MS", "Very poorly made platformer",
                  50, "yellow", WIDTH // 2, HEIGHT // 2 - 100, self.window)
        draw_text("Comic Sans MS", "Press ESC to stop the voices",
                  25, "yellow", WIDTH // 2, HEIGHT // 2, self.window)
        draw_text("Comic Sans MS", "Press Enter to start", 25,
                  "yellow", WIDTH // 2, HEIGHT // 2 + 50, self.window)

        pg.display.update()
        self.state = wait_for_key()

    def end_screen(self, won):
        """Used when the player either dies or wins"""
        mixer.music.stop()
        if won:
            mixer.music.load("assets/sound/win.wav")
            outcome = "You Won!"
            text = "Congrats! You made it out. You are so good"
            restart = "If you want to play again, press R"
        else:
            mixer.music.load("assets/sound/lose.wav")
            outcome = "You Lost..."
            text = "I guess you can call that an effort, but maybe next time try a bit more?"
            restart = "If you want to try the level again, press R"

        mixer.music.set_volume(.4)
        mixer.music.play()
        self.window.fill((69, 0, 69))
        draw_text("Comic Sans MS", outcome, 70, "yellow",
                  WIDTH // 2, HEIGHT // 2 - 200, self.window)
        draw_text("Comic Sans MS", text, 50, "yellow",
                  WIDTH // 2, HEIGHT // 2 - 100, self.window)
        draw_text("Comic Sans MS", restart,
                  25, "yellow", WIDTH // 2, HEIGHT // 2, self.window)
        draw_text("Comic Sans MS", "Press ESC to stop this abomination",
                  25, "yellow", WIDTH // 2, HEIGHT // 2 + 50, self.window)

        pg.display.update()
        action = wait_for_key()
        return action == "restart"
