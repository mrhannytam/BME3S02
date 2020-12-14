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
worker()