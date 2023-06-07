import pygame
import os
import random
import csv

pygame.init()
#load music/sound
pygame.mixer.music.load('Shooter-main/audio/music2.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()
jump_fx = pygame.mixer.Sound('Shooter-main/audio/jump.wav')
jump_fx.set_volume(0.5)
shoot_fx = pygame.mixer.Sound('Shooter-main/audio/shot.wav')
shoot_fx.set_volume(0.5)
grenade_fx = pygame.mixer.Sound('Shooter-main/audio/grenade.wav')
grenade_fx.set_volume(0.5)


#screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
start_game = False
start_intro = False
#menu setup
sound = True
options_menu = False
lv_menu = False
start_menu = True
level = 1
pause_menu = False
#set up for tile
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 23
#char variable
moving_left = False
moving_right = False
shoot = False
grenade_throw = False
screen_scroll = 0
bg_scroll = 0
GRAVITY = 0.75
MAX_LEVEL = 3
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter.exe')

#load image
#button
start_img = pygame.image.load('Shooter-main/img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('Shooter-main/img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('Shooter-main/img/restart_btn.png').convert_alpha()
options_img = pygame.image.load('Shooter-main/img/options_btn.png').convert_alpha()
audio_img = pygame.image.load('Shooter-main/img/options_menu/audio_btn.png').convert_alpha()
back_img = pygame.image.load('Shooter-main/img/options_menu/back_btn.png').convert_alpha()
resume_img = pygame.image.load('Shooter-main/img/resume_btn.png').convert_alpha()
lv_img = pygame.image.load('Shooter-main/img/lv_btn.png').convert_alpha()
lv1_img = pygame.image.load('Shooter-main/img/lv_menu/1_btn.png').convert_alpha()
lv2_img = pygame.image.load('Shooter-main/img/lv_menu/2_btn.png').convert_alpha()
lv3_img = pygame.image.load('Shooter-main/img/lv_menu/3_btn.png').convert_alpha()
#assets for level
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Shooter-main/img/Tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
#projectiles
bullet_img = pygame.image.load('Shooter-main/img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('Shooter-main/img/icons/grenade.png').convert_alpha()
#items
health_box_img = pygame.image.load('Shooter-main/img/icons/health_box.png').convert_alpha()
grenade_box_img = pygame.image.load('Shooter-main/img/icons/grenade_box.png').convert_alpha()
item_boxes = {
    'Health' : health_box_img ,
    'Grenade' : grenade_box_img
}
#background img
pine1_img = pygame.image.load('Shooter-main/img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('Shooter-main/img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('Shooter-main/img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('Shooter-main/img/Background/sky.png').convert_alpha()
clock = pygame.time.Clock()
FPS = 60

BG = (144, 201, 200)

RED = (255, 0, 0)

BLACK = (0, 0, 0)

PINK = (255, 192, 203)

GREEN = (0, 255, 0)
def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

#define font
font = pygame.font.SysFont('Futara', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class ScreenFade():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed
		self.fade_counter = 0


	def fade(self):
		fade_complete = False
		self.fade_counter += self.speed
		if self.direction == 1:#whole screen fade
            #left and right
			pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            #up and down
			pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
			pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
		if self.direction == 2:#vertical screen fade down
			pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
		if self.fade_counter >= SCREEN_WIDTH:
			fade_complete = True

		return fade_complete

intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

class Button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:

			self.clicked = False
		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
def reset_level():
    ranged_group.empty()
    boss_group.empty()
    melee_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    cactus_group.empty()
    exit_group.empty()

    #create empty tile list
    data = []
    for row in range(ROWS):
	    r = [-1] * COLS
	    data.append(r)

    return data

class Player(pygame.sprite.Sprite):

    def __init__(self, char_class, x , y , scale, health, speed, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.jump = False
        self.in_air = False
        self.health = health
        self.max_health = self.health
        self.vel_y = 0
        self.shoot_cooldown = 0
        self.grenade_cooldown = 0
        self.char_class = char_class
        self.flip = False
        self.speed = speed
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = 0
        self.grenade_count = grenades
        #Ai specific counter
        temp_list = []
        animation_type = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_type:
            temp_list = []
            num_of_frames = len(os.listdir(f'Shooter-main/img/{self.char_class}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'Shooter-main/img/{self.char_class}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * scale,img.get_height() * scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.direction = 1
        self.rect = img.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        #Reset movement variable to stop moving
        dx = 0
        dy = 0
        #Assign movement variable for movement
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump == True:
            self.vel_y = -14
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        for tile in world.obstacle_list:
            #check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_class == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            #check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, ie falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom


        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        level_complete = False

        if pygame.sprite.spritecollide(self, exit_group, False) and self.char_class == 'player':
            level_complete = True

            # check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        if pygame.sprite.spritecollide(self, cactus_group, False):
            if self.char_class == 'player':
                self.health = 0

        if self.char_class == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy
        #update scroll based on player movement
        if self.char_class == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE - SCREEN_WIDTH))\
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * 0.6 * self.direction), self.rect.centery,
                        self.direction)
            bullet_group.add(bullet)
            if sound == True:
                shoot_fx.play()

    def grenade_throw(self):
        if self.grenade_cooldown == 0 and self.grenade_count > 0:
            self.grenade_cooldown = 40
            self.grenade_count -= 1
            grenade = Grenade(player.rect.centerx + (player.rect.size[0] * 0.5 * player.direction),
                              player.rect.top,player.direction)
            grenade_group.add(grenade)

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #check for enough times since last update
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #Check if this is a final frame
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
                self.kill()
            else:
                self.frame_index = 0


    def update_action(self, new_action):
        #check if new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.grenade_cooldown > 0:
            self.grenade_cooldown -= 1

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False) , self.rect)

class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class Enemy(Player):
    def __init__(self, char_class, x , y , scale, health, speed, grenades):
        super().__init__(char_class, x ,y , scale, health, speed, grenades)
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        temp_list = []

    def ai(self):
        self.rect.x += screen_scroll
class Ranged(Enemy):
    def __init__(self, char_class, x , y , scale, health, speed, grenades):
        super().__init__(char_class, x ,y , scale, health, speed, grenades)
        self.vision = pygame.Rect(0, 0, TILE_SIZE * 4, 20)
        temp_list = []


    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 20
            if self.vision.colliderect(player.rect):
                    # running and face the player
                    self.update_action(0)
                    self.shoot()
                    self.shoot_cooldown = 40
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1

                    if self.idling_counter < 0:
                        self.idling = False
                        self.idling_counter = 0
        super().ai()

class Melee(Enemy):
    def __init__(self, char_class, x, y, scale, health, speed, grenades):
        super().__init__(char_class, x, y, scale, health, speed, grenades)
        self.melee_cooldown = 0

    def melee(self):
        if self.melee_cooldown == 0:
            self.melee_cooldown = 40
            player.health -= 20

    def update(self):
        super().update()
        if self.melee_cooldown > 0:
            self.melee_cooldown -= 1

    def ai(self):
            # if ((player.rect.x - self.rect.x) < TILE_SIZE * 4) and  ((player.rect.y - self.rect.y) < TILE_SIZE * 4):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 20
            if pygame.sprite.collide_rect(self, player):
                    # running and face the player
                    self.update_action(0)
                    self.melee()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1

                    if self.idling_counter < 0:
                        self.idling = False
                        self.idling_counter = 0
        super().ai()
class Boss(Melee):
    def __init__(self, char_class, x , y , scale, health, speed, grenades):
        super().__init__(char_class, x ,y , scale, health, speed, grenades)
        self.vision = pygame.Rect(0, 0, TILE_SIZE * 4, 20)
        temp_list = []

    def shoot_grenade(self):
        if self.grenade_cooldown == 0:
            self.grenade_cooldown = 100
            grenade = Grenade(self.rect.centerx + (self.rect.size[0] * 0.5 * self.direction),
                              self.rect.top, self.direction)
            grenade_group.add(grenade)


    def ai(self):
            # if ((player.rect.x - self.rect.x) < TILE_SIZE * 4) and  ((player.rect.y - self.rect.y) < TILE_SIZE * 4):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 20
            if self.vision.colliderect(player.rect):
                    # running and face the player
                self.update_action(0)
                self.shoot_grenade()
                if pygame.sprite.collide_rect(self, player):
                    self.melee()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1

                    if self.idling_counter < 0:
                        self.idling = False
                        self.idling_counter = 0

        super().ai()
class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        #check if the player has picked up the boxes
        if pygame.sprite.collide_rect(self, player):
            #check what kind of boxes
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Grenade':
                player.grenade_count += 1
            #delete item
            self.kill()
        self.rect.x += screen_scroll

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #bullet movement
        self.rect.x += (self.direction * self.speed) + screen_scroll

        #check if bullet has gone offscreen
        #check collision with tiles:
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        #check collision with character
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 10
                self.kill()
        for ranged in ranged_group:
            if pygame.sprite.spritecollide(ranged, bullet_group, False):
                if ranged.alive:
                    ranged.health -= 10
                    self.kill()
        for melee in melee_group:
            if pygame.sprite.spritecollide(melee, bullet_group, False):
                if melee.alive:
                    melee.health -= 10
                    self.kill()
        for boss in boss_group:
            if pygame.sprite.spritecollide(boss, bullet_group, False):
                if boss.alive:
                    boss.health -= 10
                    self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 50
        self.vel_y = -14
        self.speed = 10
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width , self.height):
                self.direction *= -1
                dx = self.direction * self.speed
                # check collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.speed = 0
                # check collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    # check if above the ground, ie falling
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        dy = tile[1].top - self.rect.bottom
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        #change the direction of grenade
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1

        #countdown_timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

            if sound == True:
                grenade_fx.play()

            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            #do damage to anyone in radius
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
            abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2:
                player.health -= 40
            for ranged in ranged_group:
                if abs(self.rect.centerx - ranged.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centerx - ranged.rect.centerx) < TILE_SIZE * 2:
                    ranged.health -= 40
            for melee in melee_group:
                if abs(self.rect.centerx - melee.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centerx - melee.rect.centerx) < TILE_SIZE * 2:
                    melee.health -= 40
            for boss in boss_group:
                if abs(self.rect.centerx - boss.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centerx - boss.rect.centerx) < TILE_SIZE * 2:
                    boss.health -= 40
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'Shooter-main/img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        #update explosion animation
        self.counter += 1
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #if animation complete self.kill()
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    def update(self):
        self.rect.x += screen_scroll

class Cactus(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2 , y + (TILE_SIZE - self.image.get_height()))
    def update(self):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        #iterate through each value in level data file
        for y,row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile == 12:
                        cactus = Cactus(img, x * TILE_SIZE, y * TILE_SIZE)
                        cactus_group.add(cactus)
                    elif tile >= 11 and tile <= 14 and tile != 12:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:#create player
                        player = Player('player', x * TILE_SIZE, y * TILE_SIZE, 1.5, 100, 5, 4)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:#create enemy
                        ranged = Ranged('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.5, 25, 2, 0)
                        ranged_group.add(ranged)
                    elif tile == 18:
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 21:
                        melee = Melee('melee', x * TILE_SIZE, y * TILE_SIZE, 1.5, 50, 2, 0)
                        melee_group.add(melee)
                    elif tile == 22:
                        boss = Boss('boss', x * TILE_SIZE, y * TILE_SIZE, 1.5, 50, 2, 0 )
                        boss_group.add(boss)
                    elif tile == 20:  # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

#create buttons
start_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 250, start_img, 1)
exit_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, exit_img, 1)
exit_button_death = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, exit_img, 1)
exit_button_pause = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, exit_img, 1)
restart_button_death = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100 , restart_img, 3)
resume_button_pause = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, resume_img, 3)
options_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100 , options_img, 1)
back_button_options = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, back_img, 1)
audio_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, audio_img, 1)
lv_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, lv_img, 1)
lv1_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 250, lv1_img, 1)
lv2_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150, lv2_img, 1)
lv3_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, lv3_img, 1)
back_button_lv = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, back_img, 1)

#create sprite
ranged_group = pygame.sprite.Group()
melee_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
cactus_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
status = True

#create empty list
def world_generation():
    """

    """
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)
    with open(f'Shooter-main/level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    return world_data

world = World()
player, health_bar = world.process_data(world_generation())

while status:
    if start_game == False:
      if start_menu == True:
        draw_bg()
        if start_button.draw(screen):
            start_game = True
            start_intro = False
        if exit_button.draw(screen):
            status = False
        if options_button.draw(screen):
            options_menu = True
            start_menu = False
        
        if lv_button.draw(screen):
            lv_menu = True
            start_menu = False
      if options_menu == True:
        draw_bg()
        if audio_button.draw(screen):
            if sound == True:
                sound = False
                pygame.mixer.music.stop()
            elif sound == False:
                sound = True
                pygame.mixer.music.play()
        if back_button_options.draw(screen):
            options_menu = False
            start_menu = True
      if lv_menu == True:
        draw_bg()
        if lv1_button.draw(screen):
            level = 1
            world_data = reset_level()
            world = World()
            world_data = world_generation()
            player, health_bar = world.process_data(world_data)
        if lv2_button.draw(screen):
            level = 2
            world_data = reset_level()
            world = World()
            world_data = world_generation()
            player, health_bar = world.process_data(world_data)
        if lv3_button.draw(screen):
            level = 3
            world_data = reset_level()
            world = World()
            world_data = world_generation()
            player,health_bar = world.process_data(world_data)
        if back_button_lv.draw(screen):
            lv_menu = False
            start_menu = True
      if pause_menu == True:
        draw_bg()
        if exit_button_pause.draw(screen):
            start_menu = True
            pause_menu = False
            world_data = reset_level()
            world_data = world_generation()
            world = World()
            player, health_bar = world.process_data(world_data)
        if resume_button_pause.draw(screen):
            pause_menu = False
            start_game = True

    else:
        start_menu = False
        clock.tick(FPS)
        #draw backgroud
        draw_bg()
        #draw world
        world.draw()
        health_bar.draw(player.health)
        draw_text(f'GRENADE: {player.grenade_count}', font, BLACK, 200, 10)

        player.update()
        player.draw()

        for ranged in ranged_group:
            ranged.ai()
            ranged.update()
            ranged.draw()
        for melee in melee_group:
            melee.ai()
            melee.update()
            melee.draw()
        for boss in boss_group:
            boss.ai()
            boss.update()
            boss.draw()
        #update and draw groups
        bullet_group.update()
        bullet_group.draw(screen)
        grenade_group.update()
        grenade_group.draw(screen)
        explosion_group.update()
        explosion_group.draw(screen)
        item_box_group.update()
        item_box_group.draw(screen)
        decoration_group.update()
        decoration_group.draw(screen)
        water_group.update()
        water_group.draw(screen)
        cactus_group.update()
        cactus_group.draw(screen)
        exit_group.update()
        exit_group.draw(screen)

        #update intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0
        #check for movement
        if player.alive:
            if shoot:
                player.shoot()
            elif grenade_throw:
                player.grenade_throw()
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            if level_complete == True :
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVEL:
                    pass
                else:
                    start_game = False
                    start_menu = True
                    level = 1
                world_data = world_generation()
                world = World()
                player, health_bar = world.process_data(world_data)
        else:
            screen_scroll = 0
            if death_fade.fade():
                if restart_button_death.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    world = World()
                    player,health_bar = world.process_data(world_generation())

                if exit_button_death.draw(screen):
                    start_game = False
                    world_data = reset_level()
                    world = World()
                    player,health_bar = world.process_data(world_generation())
                    start_menu = True

    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and player.alive and player.in_air == False:
                player.jump = True
                if sound == True:
                    jump_fx.play()
            if event.key == pygame.K_a:
                moving_left = True
            elif event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_o:
                grenade_throw = True
            if event.key == pygame.K_ESCAPE:
                pause_menu = True
                start_game = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_o:
                grenade_throw = False
    pygame.display.update()

pygame.quit()