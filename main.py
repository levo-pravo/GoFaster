d = 1.6

#the_numbers['']
the_numbers = {
    'text_score_x': int(10/d),
    'text_score_y': int(150//d),
    'text_goals_x': int(10/d),
    'text_goals_y': int(200/d),
    'text_now_score_x': int(10/d),
    'text_now_score_y': int(250/d),
    'text_now_goals_x': int(10/d),
    'text_now_goals_y': int(300/d),
    'text_record_score_x': int(10/d),
    'text_record_score_y': int(350/d),
    'text_record_goals_x': int(10/d),
    'text_record_goals_y': int(350/d)
}

import sys
from time import time as timer, sleep
from pygame import *
from random import random, randint
import json
font.init()
mixer.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed_x, player_speed_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (int(100/d), int(100/d)))
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
            return 1
        if sprite.spritecollide(self, enemies, False):
            return 2
        if sprite.spritecollide(self, line_enemies, False):
            return 3
    def goal(self):
        global goals
        global now_goals
        if sprite.collide_rect(self, goal):
            goal.new = True
            goals += 1
            now_goals += 1
    '''def set_gamemode(self, file):
        file'''

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
        if self.rect.x >= int(1920/d) or self.rect.y >= int(1080/d):
            self.rect.x = (int(1920/d) - self.rect.x) - int(100/d)
            self.rect.y = (int(1080/d) - self.rect.y) - int(100/d)

class Goal(GameSprite):
    def update(self):
        if self.new == True:
            self.new = False
            self.rect.x = randint(0, int(1820/d))
            self.rect.y = randint(0, int(980/d))

def statistic():
    global text_score
    global text_goals
    global text_now_score
    global text_now_goals
    global text_record_score
    global text_record_goals
    text_score = font2.render('Общ. время: ' + str(score), 1, (255, 255, 255))
    window.blit(text_score, (the_numbers['text_score_x'], the_numbers['text_score_y']))
    text_goals = font2.render('Общ. счёт: ' + str(goals), 1, (255, 255, 255))
    window.blit(text_goals, (the_numbers['text_goals_x'], the_numbers['text_goals_y']))
    text_now_score = font2.render('Время: ' + str(now_score), 1, (255, 255, 255))
    window.blit(text_now_score, (the_numbers['text_now_score_x'], the_numbers['text_now_score_y']))
    text_now_goals = font2.render('Счёт: ' + str(now_goals), 1, (255, 255, 255))
    window.blit(text_now_goals, (the_numbers['text_now_goals_x'], the_numbers['text_now_goals_y']))
    if now_score > record_score:
        text_record_score = font2.render('Рекорд время: ' + str(now_score), 1, (255, 255, 255))
        window.blit(text_record_score, (the_numbers['text_record_score_x'], the_numbers['text_record_score_y']))
    else:
        text_record_score = font2.render('Рекорд время: ' + str(record_score), 1, (255, 255, 255))
        window.blit(text_record_score, (the_numbers['text_record_score_x'], the_numbers['text_record_score_y']))
    if now_goals > record_goals:
        text_record_goals = font2.render('Рекорд счёт: ' + str(now_goals), 1, (255, 255, 255))
        window.blit(text_record_goals, (the_numbers['text_record_goals_x'], the_numbers['text_record_goals_y']))
    else:
        text_record_goals = font2.render('Рекорд счёт: ' + str(record_goals), 1, (255, 255, 255))
        window.blit(text_record_goals, (the_numbers['text_record_goals_x'], the_numbers['text_record_goals_y']))

while True:
    #setup
    with open('gamemode.json', 'r', encoding='utf-8') as file:
        gamemode = json.load(file)
        score = gamemode["score"]
        goals = gamemode["goals"]
        record_score = gamemode["record_score"]
        record_goals = gamemode["record_goals"]
    sound = mixer.Sound("music.ogg")
    looser = mixer.Sound("looser.ogg")
    flag_for_score = True #данный флаг показывает, надо ли обнулять ласт тайм
    last_time = timer()
    new_time = timer()
    lx = [int(7/d), int(7/d), 0, int(7/d), 0, 0]
    ly = [0, 0, int(7/d), 0, int(7/d), int(7/d)]

    window = display.set_mode((int(1920/d), int(1080/d)))
    display.set_caption('GoFaster!')
    display.set_icon(transform.scale(image.load('player.png'), (int(1920/d), int(1080/d))))
    clock = time.Clock()
    new_background = transform.scale(image.load('new_background.png'), (int(1920/d), int(1080/d)))
    background = transform.scale(image.load('background.png'), (int(1920/d), int(1080/d)))
    now_score = 0
    now_goals = 0

    player = Player('player.png', int(1820/d), int(980/d), int(10/d), None)
    killer = Enemy('killer.png', 0, 0, int(2/d), None)
    goal = Goal('goal.png', randint(0, int(1820/d)), randint(0, int(980/d)), None, None)

    enemies = sprite.Group()
    for i in range(0, 6):
        if d > 3:
            enemy = Enemy('enemy.png', randint(0, int(960/d)), randint(0, int(540/d)), 1, 1)
        else:
            enemy = Enemy('enemy.png', randint(0, int(960/d)), randint(0, int(540/d)), randint(1, 3), randint(1, 3))
        enemies.add(enemy)
    line_enemies = sprite.Group()
    for i in range(0, 6):
        if lx[i] == 0:
            line_enemy = Enemy('line_enemy.png', randint(0, int(1820/d)), int(-100/d), lx[i], ly[i])
        else:
            line_enemy = Enemy('line_enemy.png', int(-100/d), randint(0, int(920/d)), lx[i], ly[i])     
        line_enemies.add(line_enemy)

    font2 = font.SysFont('calibri', int(30/d))

    font3 = font.SysFont('calibri', int(300/d))
    text_play = font3.render('Играть', 1, (0, 255, 0))
    text_width_play = text_play.get_width()
    text_height_play = text_play.get_height()
    font4 = font.SysFont('calibri', int(133/d))

    x_c_p = []
    for i in range (int(441/d), text_width_play+int(441/d)):
        x_c_p.append(i)
    y_c_p = []
    for i in range (text_height_play):
        y_c_p.append(i)

    text_help = font3.render('Помощь', 1, (255, 165, 0))
    text_width_help = text_help.get_width()
    text_height_help = text_help.get_height()

    font5 = font.SysFont('calibri', int(66/d))

    text_genius = font4.render('Открой Помощь.txt гений', 1, (255, 165, 0))

    text_can = font5.render('Попробуй набить ' + str(int(record_score//10)*10 + 10) + ' времени и ' + str(int(record_goals//10)*10 + 10) + ' счёта', 1, (128, 166, 255))

    x_c_h = []
    for i in range (int(370/d), text_width_help+int(370/d)):
        x_c_h.append(i)
    y_c_h = []
    for i in range (int(800/d), text_height_help+int(800/d)):
        y_c_h.append(i)

    x = -1
    y = -1
    x_n = -1
    y_n = -1
    while True:
        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    x, y = e.pos
            if e.type == MOUSEMOTION:
                x_n, y_n = e.pos
        if x_n in x_c_p and y_n in y_c_p:
            text_play = font3.render('Играть', 1, (255, 255, 255))
        else:
            text_play = font3.render('Играть', 1, (0, 255, 0))
        if x_n in x_c_h and y_n in y_c_h:
            text_help = font3.render('Помощь', 1, (255, 255, 255))
        else:
            text_help = font3.render('Помощь', 1, (255, 165, 0))
        if x in x_c_p and y in y_c_p:
            break
        elif x in x_c_h and y in y_c_h:
            window.blit(background, (0, 0))
            window.blit(text_genius, (int(30/d), int(100/d)))
            display.update()
            sleep(3)
            sys.exit()
        window.blit(background, (0, 0))
        window.blit(text_play, (int(441/d), 0))
        window.blit(text_help, (int(370/d), int(800/d)))
        window.blit(text_can, (int(370/d), int(600/d)))
        if gamemode['statistic'] == 1:
            statistic()
        display.update()
        clock.tick(60)

    last_time_for_background = timer()
    last_time_for_sound = timer()
    sound.play()

    while True:
        for e in event.get():
            if e.type == QUIT:
                sys.exit()

        if timer() - last_time_for_background >= 3:
            window.blit(background, (0, 0))
        else:
            window.blit(new_background, (0, 0))

        if timer() - last_time_for_sound >= 20:
            last_time_for_sound = timer()
            sound.play()

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
        if player.kill_player() == 1:
            player.image = transform.scale(image.load('player1.png'), (int(100/d), int(100/d)))
            player.reset()
            if gamemode['statistic'] == 1:
                statistic()
            display.update()
            sound.stop()
            looser.play()
            sleep(3)
            break
        if player.kill_player() == 2:
            player.image = transform.scale(image.load('player2.png'), (int(100/d), int(100/d)))
            player.reset()
            if gamemode['statistic'] == 1:
                statistic()
            display.update()
            sound.stop()
            looser.play()
            sleep(3)
            break
        if player.kill_player() == 3:
            player.image = transform.scale(image.load('player3.png'), (int(100/d), int(100/d)))
            player.reset()
            if gamemode['statistic'] == 1:
                statistic()
            display.update()
            sound.stop()
            looser.play()
            sleep(3)
            break

        if gamemode['statistic'] == 1:
            statistic()
        
        display.update()
        clock.tick(60)

        gamemode['score'] = score
        gamemode['goals'] = goals
        if now_score >= record_score:
            gamemode['record_score'] = now_score
        if now_goals >= record_goals:
            gamemode['record_goals'] = now_goals
        with open('gamemode.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(gamemode))