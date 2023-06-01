d = 1.6

import json
with open('gamemode.json', 'r', encoding='utf-8') as file:
    theme = json.load(file)["theme"]

if theme == 'normal':
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
        'text_record_goals_y': int(400/d),

        'font2': int(30/d),
        'font3': int(300/d),
        'font4': int(133/d),
        'font5': int(66/d),

        'text_play_color': (0, 255, 0),
        'text_play_color_motion': (255, 255, 255),
        'text_play_x': int(441/d),
        'text_play_y': 0,
        'text_help_color': (255, 165, 0),
        'text_help_color_motion': (255, 255, 255),
        'text_help_x': int(370/d),
        'text_help_y': int(800/d),
    }

elif theme == 'night':
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
        'text_record_goals_y': int(400/d),

        'font2': int(30/d),
        'font3': int(300/d),
        'font4': int(133/d),
        'font5': int(66/d),

        'text_play_color': (0, 0, 0),
        'text_play_color_motion': (0, 255, 0),
        'text_play_x': int(441/d),
        'text_play_y': 0,
        'text_help_color': (0, 0, 0),
        'text_help_color_motion': (255, 165, 0),
        'text_help_x': int(370/d),
        'text_help_y': int(800/d),
    }