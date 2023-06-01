import pygame
import os
import random
import csv


def draw_bg():
    """
    draw background for level and for various menu screens
    :return:
    """

def draw_text(text, font, text_col, x, y):
    """
    draw health text and draw grenade text for player while in the level
    :param text:
    :param font:
    :param text_col:
    :param x:
    :param y:
    :return:
    """

class ScreenFade():
	def __init__(self, direction, colour, speed):
        """
        intialize ScreenFade instance
        :param direction
        :param colour
        :param speed
        :return
        """


	def fade(self):
        """
        create transistion screen
        :return fade_complete
        """

class Button():
	def __init__(self,x, y, image, scale):
        """
        initialize the button variable with image,scale and
        :return Fade_complete
        """

	def draw(self, surface):
        """
        check if the button is clicked.
        :return action
        """

def reset_level():
    """
    empty all groups of instances
    set matrix of data for resetting the level
    :return: data
    """
class Player(pygame.sprite.Sprite):

    def __init__(self, char_class, x , y , scale, health, speed, grenades):
        """
        intialize Player instances
        :param char_class:
        :param x:
        :param y:
        :param scale:
        :param health:
        :param speed:
        :param grenades:
        set attributes of Player/Enemy
        """

    def move(self, moving_left, moving_right):
        """

        :param moving_left:
        :param moving_right:
        for players movement and enemy movement
        :return:    screen_scroll, level_complete
        """

    def shoot(self):
        """
        create bullet instances when player and enemy(ranged) shoot by hitting SPACE button.
        :return: 
        """

    def grenade_throw(self):
        """
        create grenade instances when player throws grenades by hitting O button.
        :return:
        """

    def update_animation(self):
        """
        cycle through the image lists to animate player and enemy when moving,idling or dying
        :return:
        """

    def update_action(self, new_action):
        #check if new action is different from the previous one
        """
        :param new_action:
        set the status variable for update_animation
        :return:
        """


    def update(self):
        """
        update animation
        check if the player/enemy still alive
        update cooldown
        :return:
        """

    def check_alive(self):
        """
        check if player/enemy has died
        set action to 3(death)
        and change other parameters to prevent interaction
        :return:
        """
    def draw(self):
        """
        draw characters on screen
        :return:
        """

class HealthBar():
	def __init__(self, x, y, health, max_health):
        """
        intialize class healthbar to display player health on the left of the screen
        starting at player max health.
        return
        """

	def draw(self, health):
        """
        draw health_bar with green rectangle
        :return
        """


class Enemy(Player):
    def __init__(self, char_class, x , y , scale, health, speed, grenades):
        """
        intialize enemey class(inherited from Player)
        using special variables beside default variables of player for ai method
        :param char_class:
        :param x:
        :param y:
        :param scale:
        :param health:
        :param speed:
        :param grenades:

        """

    def ai(self):
        """
        update instances location when characters moving left or right
        :return:
        """

class Ranged(Enemy):
    def __init__(self, char_class, x , y , scale, health, speed, grenades):
        """
        initialize ranged class(inherited from Enemy)
        vision variable for ai class
        :param char_class:
        :param x:
        :param y:
        :param scale:
        :param health:
        :param speed:
        :param grenades:
        """


    def ai(self):
        """
        making sure that the instances move around randomly and shoot the player if they see them.
        :return:
        """

class Melee(Enemy):
    def __init__(self, char_class, x, y, scale, health, speed, grenades):
        """
        intialize melee class(inherited from Enemy)
        melee_cooldown to make sure that the player won't die instantly if colliding.
        :param char_class:
        :param x:
        :param y:
        :param scale:
        :param health:
        :param speed:
        :param grenades:
        """

    def melee(self):
        """
        update melee cooldown
        if the instance hits the player
        :return:
        """

    def update(self):
        """
        update melee cooldown when not hitting the player.
        :return:
        """


    def ai(self):
        """
        moving the instance around and doing damage if the player collides with it
        :return:
        """

class Boss(Melee):
    def __init__(self, char_class, x , y , scale, health, speed, grenades):
        """same with ranged and melee classes"""

    def shoot_grenade(self):
        """
        create grenade instance when the instance is shooting
        update cooldown
        :return:
        """


    def ai(self):
        """
        damage the player if colliding and shoot the player if they are in the instance's vision
        :return
        """

class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type, x, y):
        """
        intialize the item box instances with item_type to detect the type
        :param item_type:
        :param x:
        :param y:
        """

    def update(self):
        """
        update the instances location when player is moving
        update the instances if the player collects the instance
        :return:
        """


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        """
        initialize the bullet instances with directions
        :param x:
        :param y:
        :param direction:
        :return
        """

    def update(self):
        """
        update the movement of the bullet instance
        check if the bullet hits with a tile, a Player or an Enemy.
        :return:
        """

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        """
        initialize Grenade instance
        :param x:
        :param y:
        :param direction:
        :return
        """

    def update(self):
        """
        update grenade movement
        update the timer and initialize Explosion instances
        update the player health and enemy health if in range of the grenade.
        :return:
        """

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        """
        intialize the explosion instancees
        :param x:
        :param y:
        :param scale:
        """

    def update(self):
        """
        run animation for explosion.
        :return:
        """

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        """
        intialize Decoration Instances
        :param img:
        :param x:
        :param y:
        """

    def update(self):
        """
        update the location when the player moves
        """

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        """
        intialize water instances.
        :param img:
        :param x:
        :param y:
        :return
        """
    def update(self):
        """
        update location of water instance
        :return:
        """

class Cactus(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        """
        intialize cactus instance
        :param img:
        :param x:
        :param y:
        """

    def update(self):
        """
        update the location of the instance.
        :return:
        """

class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
        """
        update exit
        :return
        """

	def update(self):
        """
        update the location of exit
        :return
        """


class World():
    def __init__(self):
        """
        intialize the list of matrix level
        """

    def process_data(self, data):
        """
        read from the data matrix
        create instances according to tiles
        add them to group.
        :param data:
        :return: player , health_bar
        """

    def draw(self)
        """
        draw the level on screen
        :return: 
        """

def world_generation():
    """
    read and create data matrix for csv.file
    """

