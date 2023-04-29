d = 2

import sys
from time import time as timer
from pygame import *
from random import random, randint
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed_x, player_speed_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (100//d, 100//d))
        self.speed_x = player_speed_x
        self.speed_y = player_speed_y
        self.speed = player_speed_x
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.new = True

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
        if (keys_pressed[K_d] or keys_pressed[K_RIGHT]) and self.rect.x <= 1820//d:
            self.rect.x += self.speed
        if (keys_pressed[K_w] or keys_pressed[K_UP]) and self.rect.y >= 0:
            self.rect.y -= self.speed
        if (keys_pressed[K_s] or keys_pressed[K_DOWN]) and self.rect.y <= 980//d:
            self.rect.y += self.speed
    def update_score(self):
        global score
        global now_score
        global last_time
        global new_time
        global flag_for_score
        if flag_for_score == True:
            last_time = timer()
            flag_for_score = False
        new_time = timer()
        if (new_time - last_time) >= 1 and flag_for_score == False:
            score += 1
            now_score += 1
            flag_for_score = True
    def kill_player(self):
        if sprite.collide_rect(self, killer):
            return True
        if sprite.spritecollide(self, enemies, False):
            return True
        if sprite.spritecollide(self, line_enemies, False):
            return True
    def goal(self):
        global goals
        global now_goals
        if sprite.collide_rect(self, goal):
            goal.new = True
            goals += 1
            now_goals += 1

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
        if self.rect.x >= 1920//d or self.rect.y >= 1080//d:
            self.rect.x = (1920//d - self.rect.x) - 100//d
            self.rect.y = (1080//d - self.rect.y) - 100//d

class Goal(GameSprite):
    def update(self):
        if self.new == True:
            self.new = False
            self.rect.x = randint(0, 1820//d)
            self.rect.y = randint(0, 980//d)

#setup
with open('score.txt', 'r', encoding='utf-8') as file:
    score = int(file.read())
with open('goal.txt', 'r', encoding='utf-8') as file:
    goals = int(file.read())
flag_for_score = True #данный флаг показывает, надо ли обнулять ласт тайм
last_time = timer()
new_time = timer()
x = [randint(1, 3), randint(1, 3), randint(1, 3), randint(1, 3), randint(1, 3), randint(1, 3)]
y = [randint(1, 3), randint(1, 3), randint(1, 3), randint(1, 3), randint(1, 3), randint(1, 3)]
lx = [7//d, 7//d, 0, 7//d, 0, 0]
ly = [0, 0, 7//d, 0, 7//d, 7//d]
last_time_for_background = timer()

window = display.set_mode((1920//d, 1080//d))
display.set_caption('GoFaster!')
display.set_icon(transform.scale(image.load('player.png'), (1920//d, 1080//d)))
clock = time.Clock()
new_background = transform.scale(image.load('new_background.png'), (1920//d, 1080//d))
background = transform.scale(image.load('background.png'), (1920//d, 1080//d))
now_score = 0
now_goals = 0

player = Player('player.png', 1820//d, 980//d, 10, None)
killer = Enemy('killer.png', 0, 0, 2, None)
goal = Goal('goal.png', randint(0, 1820/d), randint(0, 980//d), None, None)

enemies = sprite.Group()
for i in range(0, 6):
    enemy = Enemy('enemy.png', randint(0, 960//d), randint(0, 540//d), x[i], y[i])
    enemies.add(enemy)
line_enemies = sprite.Group()
for i in range(0, 6):
    if lx[i] == 0:
        line_enemy = Enemy('line_enemy.png', randint(0, 1820//d), -100//d, lx[i], ly[i])
    else:
        line_enemy = Enemy('line_enemy.png', -100//d, randint(0, 920//d), lx[i], ly[i])     
    line_enemies.add(line_enemy)

font2 = font.Font(None, 36//d)

'''while True:
    if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = e.pos()'''

while True:
    for e in event.get():
        if e.type == QUIT:
            sys.exit()

    if timer() - last_time_for_background >= 3:
        window.blit(background, (0, 0))
    else:
        window.blit(new_background, (0, 0))

    killer.update('killer')
    killer.reset()

    enemies.update('enemy')
    enemies.draw(window)
    line_enemies.update('line_enemy')
    line_enemies.draw(window)

    goal.update()
    goal.reset()

    player.goal()
    player.update()
    player.reset()
    player.update_score()
    if player.kill_player():
        break

    text_score = font2.render('Общ. время: ' + str(score), 1, (255, 255, 255))
    window.blit(text_score, (100//d, 300//d))
    text_score = font2.render('Общ. счёт: ' + str(goals), 1, (255, 255, 255))
    window.blit(text_score, (100//d, 350//d))

    text_now_score = font2.render('Время: ' + str(now_score), 1, (255, 255, 255))
    window.blit(text_now_score, (100//d, 400//d))
    text_now_score = font2.render('Счёт: ' + str(now_goals), 1, (255, 255, 255))
    window.blit(text_now_score, (100//d, 450//d))
    
    display.update()
    clock.tick(60)

    with open('score.txt', 'w', encoding='utf-8') as file:
        file.write(str(score))
    with open('goal.txt', 'w', encoding='utf-8') as file:
        file.write(str(goals))