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

QUESTION = glob.glob("media/question2/*.mp3")
shuffle(QUESTION)
print(QUESTION)
CURRENT_QUESTION = QUESTION.pop(0)
SCORE = 0

'''Initialization'''
reader = SimpleMFRC522()
FONT_SIZE = 50
disp = Adafruit_SSD1306.SSD1306_128_64(rst=0)
disp.begin()
disp.clear()
disp.display()
WIDTH = disp.width
HEIGHT = disp.height
led_font=ImageFont.truetype("./ARIALUNI.TTF", FONT_SIZE)
'''Initialization'''

'''Define Display Drawing'''
def Eyes(check):
    load = os.getloadavg()
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    if check == True:
        draw.text((43, 0), 'O',  font=led_font, fill=255)
        pygame.mixer.music.load('media/sound2/success.mp3')
        pygame.mixer.music.play()

    else:
        draw.text((43, 0), 'X',  font=led_font, fill=255)
        pygame.mixer.music.load('media/sound2/fail.mp3')
        pygame.mixer.music.play()

    disp.image(image)
    disp.display()
    time.sleep(3)
'''Define Display Drawing'''
def change_current_question():
    global CURRENT_QUESTION, QUESTION
    CURRENT_QUESTION = QUESTION.pop(0)

def check_answer(ans):
    if ans == int(CURRENT_QUESTION[16:-4]):
        return True
    else:
        return False



while True:

    try:
        id, text = reader.read()
        sleep(0.2)
        card = int(text)
        print(CURRENT_QUESTION[16:-4],card)
        if check_answer(card):
            print('correct')
            SCORE += 1
            print(SCORE)
            change_current_question()
            Eyes(True)

        else:
            print('wrong')
            change_current_question()
            Eyes(False)
        if len(QUESTION) == 0:
            print(SCORE)
            break
    except:
        print('', end='')
    finally:
        GPIO.cleanup()
        disp.clear()
        disp.display()