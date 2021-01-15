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

'''GPIO Initialization'''
CONTROL_PIN = 17
CONTROL_PIN2 = 18
PWM_FREQ = 50
GPIO.setmode(GPIO.BCM) #Set the GPIO to BCM mode
GPIO.setup(CONTROL_PIN, GPIO.OUT) #for motor_head
GPIO.setup(CONTROL_PIN2, GPIO.OUT) #for motor_mouth

FONT_SIZE = 50
disp = Adafruit_SSD1306.SSD1306_128_64(rst=0) #initialize the OLED
reader = SimpleMFRC522() #Initializae the RFID
disp.begin()
disp.clear()
disp.display()
WIDTH = disp.width
HEIGHT = disp.height
led_font=ImageFont.truetype("/home/pi/Desktop/BME3S02/media/font/ARIALUNI.TTF", FONT_SIZE)
'''GPIO Initialization'''


'''QUESTION Initialization'''
QUESTION = glob.glob("/home/pi/Desktop/BME3S02/media/question/*.mp3")
QUESTION_COUNT = len(QUESTION)
shuffle(QUESTION)
CURRENT_QUESTION = QUESTION.pop(0)
SCORE = 0
card = 0
'''QUESTION Initialization'''


'''Pygame Initialization'''
pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
'''Pygame Initialization'''

def worker():
    def Eyes(check):
         def blink(iamge): # blink 4 times 
             disp.image(image)
             disp.display()
             sleep(0.5)
             disp.clear()
             disp.display()
             
             disp.image(image)
             disp.display()
             sleep(0.5)
             disp.clear()
             disp.display()
             
             disp.image(image)
             disp.display()
             sleep(0.5)
             disp.clear()
             disp.display()

             
         load = os.getloadavg()
         image = Image.new('1', (WIDTH, HEIGHT))
         draw = ImageDraw.Draw(image)
         draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0) #initialize the display structure
         if check == True:
             channel1.play(pygame.mixer.Sound('/home/pi/Desktop/BME3S02/media/sound2/success.wav'))
             draw.text((43, 0), 'O',  font=led_font, fill=255) #Draw 'O' on OLED monitor
             blink(image)         
            
         else:
             channel1.play(pygame.mixer.Sound('/home/pi/Desktop/BME3S02/media/sound2/fail.wav'))
             draw.text((43, 0), 'X',  font=led_font, fill=255) #Draw 'X' on OLED monitor
             blink(image)


    #motor_head
    def Motor_head(check):

         pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
         pwm.start(0)
         def angle_to_duty_cycle(angle=0):
             duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ *angle / 180)
             return duty_cycle

         if check == True:
             next
         else:
             pwm.ChangeDutyCycle(angle_to_duty_cycle(90))
             time.sleep(0.3)
             pwm.ChangeDutyCycle(angle_to_duty_cycle(135))
             time.sleep(0.3)
             pwm.ChangeDutyCycle(angle_to_duty_cycle(45))
             time.sleep(0.3)
             pwm.ChangeDutyCycle(angle_to_duty_cycle(135))
             time.sleep(0.3)
             pwm.ChangeDutyCycle(angle_to_duty_cycle(45))
             time.sleep(0.3)
             pwm.ChangeDutyCycle(angle_to_duty_cycle(90))
             time.sleep(0.3)
         pwm.stop()

    #motor_mouth
    def Motor_mouth(check):

        pwm2 = GPIO.PWM(CONTROL_PIN2, PWM_FREQ)
        pwm2.start(0)
        def angle_to_duty_cycle2(angle=0):
            duty_cycle2 = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ *angle / 180)
            return duty_cycle2

        if check == True:
            next
        else:
            #motor_mouth
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(90))
            time.sleep(0.5)
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(75))
            time.sleep(0.5)
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(90))
            time.sleep(0.5)
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(75))
            time.sleep(0.5)
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(90))
            time.sleep(0.5)

        pwm2.stop()

     #Change another question when correct/wrong
    def change_current_question():
         global CURRENT_QUESTION, QUESTION, QUESTION_COUNT
         QUESTION_COUNT -= 1
         CURRENT_QUESTION = QUESTION.pop(0)


     #Check whether the answer is correct or not
    def check_answer(ans):
         if ans == int(CURRENT_QUESTION[40:-4]):
             return True
         else:
             return False


    # Combine two function of motor
    def shake_head(): 
        check = check_answer(card)
        if check == True:
            Motor_head(True)
            Motor_mouth(False)
        elif check == False:
            Motor_head(False)
            Motor_mouth(True)    
         
         
    while True:
        print(CURRENT_QUESTION)
        id, text = reader.read()
        sleep(0.3)
        card = int(text)
        print(CURRENT_QUESTION[40:-4],card)
        if check_answer(card): #Checking answer
            print('correct')
            SCORE += 1 #Add score
            change_current_question() #Change question
            
            t = Thread(target=shake_head) #Set up the thread
            t.daemon = True        
            t.start() #Start spliting the program into 2 threads
            Eyes(True) #show eyes image and play music
            
        else:
            print('wrong')
            change_current_question()
                   
            t = Thread(target=shake_head) #Set up the thread
            t.daemon = True
            t.start() #Start spliting the program into 2 threads
            Eyes(False)

        disp.clear()
        disp.display() #Display nothing to the OLED monitor (Clear)


gpio_thread = Thread(target=worker) #Set up the thread
gpio_thread.daemon = True
gpio_thread.start() #Start spliting the program into 2 threads

while True:
    print('TESTING...')