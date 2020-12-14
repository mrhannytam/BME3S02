import sys, pygame #pygame game logic
from time import sleep #hard coding
import glob #get a list of files
from random import shuffle # random question sequence
from tinytag import TinyTag # access mp3 title
import math #set question repeat time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_SSD1306
import os
import time
from queue import Queue
from threading import Thread
import re

GPIO.setmode(GPIO.BCM)

QUESTION = glob.glob("media/question/*.mp3")
QUESTION_COUNT = len(QUESTION)
shuffle(QUESTION)
CURRENT_QUESTION = QUESTION.pop(0)
SCORE = 0

pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

q = Queue()

def worker():
    '''Initialization'''
    FONT_SIZE = 50
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=0)
    disp.begin()
    disp.clear()
    disp.display()
    WIDTH = disp.width
    HEIGHT = disp.height
    led_font=ImageFont.truetype("./media/font/ARIALUNI.TTF", FONT_SIZE)
    '''Initialization'''


    '''Define Display Drawing'''
    def Eyes(check):
        load = os.getloadavg()
        image = Image.new('1', (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
        if check == True:
            draw.text((43, 0), 'O',  font=led_font, fill=255)
            #pygame.mixer.Channel(0).load('media/sound2/success.mp3')
            channel1.play(pygame.mixer.Sound('media/sound2/success.wav'))

        else:
            draw.text((43, 0), 'X',  font=led_font, fill=255)
            #pygame.mixer.music.Channel(0).load('media/sound2/fail.mp3')
            #pygame.mixer.music.Channel(0).play()
            channel1.play(pygame.mixer.Sound('media/sound2/fail.wav'))

        disp.image(image)
        disp.display()
        time.sleep(3)
    '''Define Display Drawing'''


    def change_current_question():
        global CURRENT_QUESTION, QUESTION, QUESTION_COUNT
        QUESTION_COUNT -= 1
        CURRENT_QUESTION = QUESTION.pop(0)


    def check_answer(ans):
        if ans == int(CURRENT_QUESTION[15:-4]):
            return True
        else:
            return False


    reader = SimpleMFRC522()
    while True:
        print('COUNT', QUESTION_COUNT)
        try:
            id, text = reader.read()
            sleep(0.3)
            card = int(text)
            print(CURRENT_QUESTION[15:-4],card)
            if check_answer(card):
                print('correct')
                global SCORE
                SCORE += 1
                change_current_question()
                Eyes(True)
            else:
                print('wrong')
                change_current_question()
                Eyes(False)
        except:
            print('', end='')
        finally:
            GPIO.cleanup()
            disp.clear()
            disp.display()


t = Thread(target=worker)
t.daemon = True
t.start()

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 500
START_BUTTON_POSITION_X = DISPLAY_WIDTH / 2 / 2 /2
QUIT_BUTTON_POSITION_X = DISPLAY_WIDTH / 2 / 2 + START_BUTTON_POSITION_X * 2
font = pygame.font.Font('media/font/mnjzbh.ttf', 30)

RED = (200, 0, 0)
BRIGHT_RED = (255,0,0)
GREEN = (0,200,0)
BRIGHT_GREEN = (0,255,0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)


screen = pygame.display.set_mode((DISPLAY_WIDTH , DISPLAY_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic , ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
            pygame.display.flip()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    #smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, font)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def game_intro():
    intro = True

    while intro:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(WHITE)
        TextSurf, TextRect = text_objects("你好", font)
        TextRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        screen.blit(TextSurf, TextRect)
        button("開始", START_BUTTON_POSITION_X, DISPLAY_HEIGHT/1.5, 120, 50, GREEN, BRIGHT_GREEN, game_loop)
        button("關機", QUIT_BUTTON_POSITION_X, DISPLAY_HEIGHT/1.5, 120, 50, RED, BRIGHT_RED, quitgame)
        pygame.display.update()
        clock.tick(15)

def game_loop():
    gameExit = False

    global QUESTION, QUESTION_COUNT, CURRENT_QUESTION, SCORE
    QUESTION = glob.glob("media/question/*.mp3")

    QUESTION_COUNT = len(QUESTION)
    shuffle(QUESTION)
    CURRENT_QUESTION = QUESTION.pop(0)
    SCORE = 0

    counter, time = 100, '100'.rjust(3) #SET COUNT TIME
    COUNTTIMEEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(COUNTTIMEEVENT, 1000)

    PLAYSOUNDEVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(PLAYSOUNDEVENT, 1000)

    quest = CURRENT_QUESTION
    pygame.mixer.music.load(quest)
    pygame.mixer.music.play()
    tag = TinyTag.get(quest)
    quest_text = tag.title

    while not gameExit:
        for e in pygame.event.get():
            if e.type == COUNTTIMEEVENT:
                counter -= 1
                time = str(counter).rjust(3) if counter > 0 else 'TIMES UP'
                if counter == 0:
                    game_end()

            if e.type == PLAYSOUNDEVENT and not pygame.mixer.music.get_busy() and not channel1.get_busy():
                quest = CURRENT_QUESTION
                pygame.mixer.music.load(quest)
                pygame.mixer.music.play()
                tag = TinyTag.get(quest)
                quest_text = tag.title
                print(quest)

            if e.type == pygame.QUIT:
                gameExit = True

        screen.fill(WHITE)
        timeSurf, timeRect = text_objects(time, font)
        timeRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT/4)
        screen.blit(timeSurf, timeRect)

        questSurf, questRect = text_objects(quest_text, font)
        questRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT/2)
        screen.blit(questSurf, questRect)

        if QUESTION_COUNT == 0:
            game_end()

        if channel1.get_busy() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        #screen.blit(font.render(time, True, BLACK), (DISPLAY_WIDTH / 2, 48))
        pygame.display.flip()
        clock.tick(60)


def game_end():
    pygame.mixer.music.load('media/sound/timesup.mp3')
    pygame.mixer.music.play()
    TEXT = ""
    COLOR = (0,0,0)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quitgame()

        screen.fill(WHITE)
        if SCORE > 10:
            TEXT = "十分好!!!"
            COLOR = BRIGHT_GREEN
        elif SCORE > 5:
            TEXT = "做得好!"
            COLOR = GREEN
        elif SCORE > 1:
            TEXT = "不錯哦~"
            COLOR = GREEN
        else:
            TEXT = "加油哦~"
            COLOR = RED
        textSurf, textRect = text_objects(TEXT, font)
        textRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT/2)
        scoreSurf, scoreRect = text_objects(str(SCORE), font)
        scoreRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT/3)
        screen.blit(textSurf, textRect)
        screen.blit(scoreSurf, scoreRect)
        #screen.blit(font.render(TEXT, True, COLOR), (DISPLAY_WIDTH / 2, 48))
        #screen.blit(font.render(str(SCORE), True, COLOR), (DISPLAY_WIDTH / 2 / 2, 100))

        button("開始", START_BUTTON_POSITION_X, DISPLAY_HEIGHT/1.5, 120, 50, GREEN, BRIGHT_GREEN, game_loop)
        button("關機", QUIT_BUTTON_POSITION_X, DISPLAY_HEIGHT/1.5, 120, 50, RED, BRIGHT_RED, quitgame)

        pygame.display.flip()
        clock.tick(60)

def quitgame():
    pygame.quit()
    #quit()
    os.system('sudo shutdown now')

game_intro()
pygame.quit()
quit()