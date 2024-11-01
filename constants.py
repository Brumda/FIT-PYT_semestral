"""All the constants that are used across the game"""
TILE_SIZE = 72
WIDTH, HEIGHT = 1920, 1080
SCREEN_SIZE = (WIDTH, HEIGHT)
FPS = 60
GRAVITY = TILE_SIZE * 0.5
PLAYER_SPEED = 5
ANIMATION_DELAYS_PLAYER = {"Hurt": 7, "Attack": 6, "Die": 7, "Double_jump": 5, "Jump": 5, "Idle": 10, "Run": 7,
                           "Fall": 10}
ANIMATION_DELAYS_ENEMY = {"Attack": 7, "Die": 8, "Hurt": 10, "Idle": 10, "Walk": 7}
NO_MOVING = ["Die", "Hurt"]
INVINCIBLE_DURATION = 1 * FPS
TUTORIAL = """
Hi! Welcome to the game. You are playing as the knight underneath.
You can run with LEFT/RIGHT, jump with UP, use levers and doors 
with DOWN and attack with SPACE. Once you jump, you can always double jump
no matter for how long have you been falling. You can use that to avoid fall damage.
There are several skele-bois, that will try to bonk you, if you get too close.
Unless, obviously, you bonk them first. Your goal is to go through the dungeon.
In each level there are several levers, that you need to pull in order to open
the door to the next level.
"""
