import sys
from time import time as timer
from pygame import *
from random import random, randint
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed_x, player_speed_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (100, 100))
        self.speed_x = player_speed_x
        self.speed_y = player_speed_y
        self.speed = player_speed_x
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed_x, player_speed_y):
        super().__init__(player_image, player_x, player_y, player_speed_x, player_speed_y)
        self.flag_for_score = True
    def update(self):
        keys_pressed = key.get_pressed()
        if (keys_pressed[K_a] or keys_pressed[K_LEFT]) and self.rect.x >= 0:
            self.rect.x -= self.speed
        if (keys_pressed[K_d] or keys_pressed[K_RIGHT]) and self.rect.x <= 1820:
            self.rect.x += self.speed
        if (keys_pressed[K_w] or keys_pressed[K_UP]) and self.rect.y >= 0:
            self.rect.y -= self.speed
        if (keys_pressed[K_s] or keys_pressed[K_DOWN]) and self.rect.y <= 980:
            self.rect.y += self.speed
    def update_score(self):
        global score
        global last_time
        global new_time
        global flag_for_score
        if flag_for_score == True:
            last_time = timer()
            flag_for_score = False
        new_time = timer()
        if (new_time - last_time) >= 1:
            score += 1
    def kill_player(self):
        if sprite.collide_rect(self, killer):
            return True
        if sprite.spritecollide(self, enemies, False):
            return True
        if sprite.spritecollide(self, line_enemies, False):
            return True

class Enemy(GameSprite):
    def update(self, enemy_type):
        if enemy_type == 'killer':
            if player.rect.x >= self.rect.x:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
            if player.rect.y >= self.rect.y:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed
        elif enemy_type == 'enemy':
            if self.speed_x > 0:
                self.rect.x += self.speed_x
            elif self.speed_x < 0:
                self.rect.x -= self.speed_x
            if self.speed_y > 0:
                self.rect.y += self.speed_y
            elif self.speed_y < 0:
                self.rect.y -= self.speed_y
        elif enemy_type == 'line_enemy':
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        if self.rect.x >= 1920 or self.rect.y >= 1080:
            self.rect.x = 1920 - self.rect.x
            self.rect.y = 1080 - self.rect.y

#setup
with open('score.txt', 'r', encoding='utf-8') as file:
    score = int(file.read())
flag_for_score = True #данный флаг показывает, надо ли обнулять ласт тайм
last_time = timer()
new_time = timer()
x = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
y = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
lx = [7, 7, 0, 7, 0, 0]
ly = [0, 0, 7, 0, 7, 7]

window = display.set_mode((1920, 1080))
display.set_caption('GoFaster!')
display.set_icon(transform.scale(image.load('player.png'), (1920, 1080)))
clock = time.Clock()
background = transform.scale(image.load('background.png'), (1920, 1080))

player = Player('player.png', 910, 490, 10, None)
killer = Enemy('killer.png', 710, 490, 2, None)

enemies = sprite.Group()
for i in range(0, 6):
    enemy = Enemy('enemy.png', randint(0, 960), randint(0, 540), x[i], y[i])
    enemies.add(enemy)
line_enemies = sprite.Group()
for i in range(0, 6):
    if lx[i] == 0:
        line_enemy = Enemy('line_enemy.png', randint(0, 1855), -65, lx[i], ly[i])
    else:
        line_enemy = Enemy('line_enemy.png', -65, randint(0, 1015), lx[i], ly[i])     
    line_enemies.add(line_enemy)

font2 = font.Font(None, 36)

while True:
    for e in event.get():
        if e.type == QUIT:
            sys.exit()

    window.blit(background, (0, 0))
    text_score = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
    window.blit(text_score, (100, 300))

    killer.update('killer')
    killer.reset()

    enemies.update('enemy')
    enemies.draw(window)
    line_enemies.update('line_enemy')
    line_enemies.draw(window)

    player.update()
    player.reset()
    player.update_score()
    if player.kill_player():
        break
    
    display.update()
    clock.tick(60)

    with open('score.txt', 'w', encoding='utf-8') as file:
        file.write(str(score))