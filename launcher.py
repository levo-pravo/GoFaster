d = 1.6

import sys
import os
import json
from time import time as timer, sleep
from pygame import *
from random import random, randint
font.init()
mixer.init()

def statistic():
    global text_score
    global text_goals
    global text_now_score
    global text_now_goals
    global text_record_score
    global text_record_goals
    text_score = font2.render('Общ. время: ' + str(score), 1, (255, 255, 255))
    window.blit(text_score, (int(10/d), int(150//d)))
    text_goals = font2.render('Общ. счёт: ' + str(goals), 1, (255, 255, 255))
    window.blit(text_goals, (int(10/d), int(200/d)))
    text_record_score = font2.render('Рекорд время: ' + str(record_score), 1, (255, 255, 255))
    window.blit(text_record_score, (int(10/d), int(250/d)))
    text_record_goals = font2.render('Рекорд счёт: ' + str(record_goals), 1, (255, 255, 255))
    window.blit(text_record_goals, (int(10/d), int(300/d)))


#setup
with open('gamemode.json', 'r', encoding='utf-8') as file:
    gamemode = json.load(file)
music_for_usual = mixer.Sound("music.ogg")
with open('score.txt', 'r', encoding='utf-8') as file:
    score = int(file.read())
with open('goal.txt', 'r', encoding='utf-8') as file:
    goals = int(file.read())
with open('record_score.txt', 'r', encoding='utf-8') as file:
    record_score = int(file.read())
with open('record_goal.txt', 'r', encoding='utf-8') as file:
    record_goals = int(file.read())

window = display.set_mode((int(1920/d), int(1080/d)))
display.set_caption('GoFaster!')
display.set_icon(transform.scale(image.load('player.png'), (int(1920/d), int(1080/d))))
clock = time.Clock()
background = transform.scale(image.load('background.png'), (int(1920/d), int(1080/d)))

font2 = font.SysFont('calibri', int(36/d))

font3 = font.SysFont('calibri', int(80/d))
text_play_usual = font3.render('Обычный режим', 1, (100, 255, 100))
text_width_play_usual = text_play_usual.get_width()
text_height_play_usual = text_play_usual.get_height()

x_c_p_u = []
for i in range (int(441/d), text_width_play_usual+int(441/d)):
    x_c_p_u.append(i)
y_c_p_u = []
for i in range (text_height_play_usual):
    y_c_p_u.append(i)

text_play_statistic = font3.render('Статистика', 1, (0, 255, 0))
text_width_play_statistic = text_play_statistic.get_width()
text_height_play_statistic = text_play_statistic.get_height()

x_c_p_s = []
for i in range (int(441/d), text_width_play_usual+int(441/d)):
    x_c_p_s.append(i)
y_c_p_s = []
for i in range (int(100/d), text_height_play_usual + int(100/d)):
    y_c_p_s.append(i)

text_play = font3.render('Играть!', 1, (255, 165, 0))
text_width_play = text_play.get_width()
text_height_play = text_play.get_height()

x_c_p = []
for i in range (int(370/d), text_width_play+int(370/d)):
    x_c_p.append(i)
y_c_p = []
for i in range (int(800/d), text_height_play+int(800/d)):
    y_c_p.append(i)

x = -1
y = -1
x_n = -1
y_n = -1

t_m_u = timer()
music_for_usual.play()

s_a = 0

while True:
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = e.pos
        if e.type == MOUSEMOTION:
            x_n, y_n = e.pos
    if x_n in x_c_p_u and y_n in y_c_p_u:
        text_play_usual = font3.render('Обычный режим', 1, (255, 255, 255))
    else:
        text_play_usual = font3.render('Обычный режим', 1, (100, 255, 100))
    if x in x_c_p_s and y in y_c_p_s and s_a == 0:
        text_play_statistic = font3.render('Статистика', 1, (255, 0, 0))
        s_a = 1
        x = -1
        y = -1
        gamemode['statistic'] = 0
    elif x in x_c_p_s and y in y_c_p_s and s_a == 1:
        text_play_statistic = font3.render('Статистика', 1, (0, 255, 0))
        s_a = 0
        x = -1
        y = -1
        gamemode['statistic'] = 1
    if x_n in x_c_p and y_n in y_c_p:
        text_play = font3.render('Играть!', 1, (255, 255, 255))
    else:
        text_play = font3.render('Играть!', 1, (255, 165, 0))
    if x in x_c_p_u and y in y_c_p_u:
        gamemode = {"health": 0, "statistic": 1}
        with open('gamemode.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(gamemode))
        music_for_usual.stop()
        window.blit(background, (0, 0))
        text_play_usual = font3.render('Игра загружается', 1, (0, 255, 0))
        window.blit(text_play_usual, (int(441/d), 0))
        statistic()
        display.update()
        os.system('main.exe')
        break
    elif x in x_c_p and y in y_c_p:
        with open('gamemode.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(gamemode))
        music_for_usual.stop()
        window.blit(background, (0, 0))
        text_play_usual = font3.render('Игра загружается', 1, (0, 255, 0))
        window.blit(text_play_usual, (int(441/d), 0))
        statistic()
        display.update()
        os.system('main.exe')
        break
    if timer() - t_m_u >= 20:
        t_m_u = timer()
        music_for_usual.play()
    window.blit(background, (0, 0))
    window.blit(text_play_usual, (int(441/d), 0))
    window.blit(text_play_statistic, (int(441/d), int(100/d)))
    window.blit(text_play, (int(370/d), int(800/d)))
    statistic()
    with open('gamemode.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(gamemode))
    display.update()
    clock.tick(60)