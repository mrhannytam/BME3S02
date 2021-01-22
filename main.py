import sys, pygame #pygame game logic
from time import sleep #hard coding
import glob #get a list of files
from random import shuffle, choice # random question sequence
from tinytag import TinyTag # access mp3 title
import math #set question repeat time
import RPi.GPIO as GPIO #RFID + OLED
from mfrc522 import SimpleMFRC522 #RFID
from PIL import Image #OLED
from PIL import ImageDraw #OLED
from PIL import ImageFont #OLED
import Adafruit_SSD1306 #OLED
import os # shutdown computer
import time #set timeout to prevent RFID detect too many time
from queue import Queue #Split the program to 2 threads
from threading import Thread #Split the program to 2 threads
import re

'''GPIO Initialization'''
GPIO.setwarnings(False)
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
led_font=ImageFont.truetype("/home/pi/Desktop/Doll_Therapy/media/font/ARIALUNI.TTF", FONT_SIZE)
'''GPIO Initialization'''


'''QUESTION Initialization'''
QUESTION = glob.glob("/home/pi/Desktop/Doll_Therapy/media/question/*.mp3")
QUESTION_COUNT = len(QUESTION)
shuffle(QUESTION)
CURRENT_QUESTION = QUESTION.pop(0)
CURRENT_QUESTION_NUMBER = CURRENT_QUESTION[re.search('\d', CURRENT_QUESTION).start():].replace('.mp3', '')
SCORE = 0
card = 0
HOLD = True
'''QUESTION Initialization'''


'''Pygame Initialization'''
pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
CURRENT_STAGE = 'game_intro'
'''Pygame Initialization'''

def worker():
    def Eyes(check):
         def blink(iamge): # blink 3 times 
             for i in range(3):
                 disp.image(image)
                 disp.display()
                 sleep(0.5) # Blink blink time
                 disp.clear()
                 disp.display()

         def slow_blink(iamge): # blink 3 times
             for i in range(5):
                 disp.image(image)
                 disp.display()
                 sleep(2) # Blink blink time
                 disp.clear()
                 disp.display()
             
         load = os.getloadavg()
         image = Image.new('1', (WIDTH, HEIGHT))
         draw = ImageDraw.Draw(image)
         draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0) #initialize the display structure
         if check == 'True':
             channel1.play(pygame.mixer.Sound('/home/pi/Desktop/Doll_Therapy/media/sound/effect/success.wav'))
             draw.text((43, 0), 'O',  font=led_font, fill=255) #Draw 'O' on OLED monitor
             blink(image)         
            
         elif check == 'False':
             channel1.play(pygame.mixer.Sound('/home/pi/Desktop/Doll_Therapy/media/sound/effect/fail.wav'))
             draw.text((43, 0), 'X',  font=led_font, fill=255) #Draw 'X' on OLED monitor
             blink(image)
             
         elif check == 'intro':
             random_eyes = ['^', '=', '*', 'O', 'X']
             random_eyes = choice(random_eyes)
             #print(random_eyes)             
             draw.text((50, 0), random_eyes,  font=led_font, fill=255) #Draw 'X' on OLED monitor
             slow_blink(image)

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
             pwm.ChangeDutyCycle(angle_to_duty_cycle(120))
             time.sleep(0.3)
             pwm.ChangeDutyCycle(angle_to_duty_cycle(60))
             time.sleep(0.3)
             pwm.ChangeDutyCycle(angle_to_duty_cycle(120))
             time.sleep(0.3)
             pwm.ChangeDutyCycle(angle_to_duty_cycle(60))
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
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(60))
            time.sleep(0.3)
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(10))
            time.sleep(0.3)
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(60))
            time.sleep(0.3)
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(10))
            time.sleep(0.3)
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(60))
            time.sleep(0.3)
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(10))
            time.sleep(0.3)
            pwm2.ChangeDutyCycle(angle_to_duty_cycle2(60))
            time.sleep(0.3)

        pwm2.stop()

     #Change another question when correct/wrong
    def change_current_question():
         global CURRENT_QUESTION, QUESTION, QUESTION_COUNT, CURRENT_QUESTION_NUMBER
         QUESTION_COUNT -= 1
         CURRENT_QUESTION = QUESTION.pop(0)
         CURRENT_QUESTION_NUMBER = CURRENT_QUESTION[re.search('\d', CURRENT_QUESTION).start():].replace('.mp3', '')


     #Check whether the answer is correct or not
    def check_answer(ans):
        try:
            if ans == CURRENT_QUESTION_NUMBER:
                return True
            else:
                return False
        except:
            return False


    # Combine two function of motor
    def shake_head_correct(): 
        Motor_head(True)
        Motor_mouth(False)

    def shake_head_wrong():
        Motor_head(False)
        Motor_mouth(True)    
         
         
    while True:
        #print(CURRENT_QUESTION)
        #global CURRENT_STAGE
        print(CURRENT_STAGE)
        if CURRENT_STAGE == 'game_intro' or CURRENT_STAGE == 'difficulty':
             Eyes('intro')
            
        elif CURRENT_STAGE == 'game_loop':
            id, text = reader.read()
            sleep(0.3)
            card = int(text)
            print('Current Question number is: ', CURRENT_QUESTION_NUMBER, 'Tapped number is: ', card)
            
                            
            ans_sound = CURRENT_QUESTION
            ans_sound = ans_sound.replace('question_hard', 'ans').replace('question', 'ans')
            ans_sound = ans_sound.replace(CURRENT_QUESTION_NUMBER, str(card)).replace('mp3', 'wav')
            print('Playing answer sound:', ans_sound)
    
            if check_answer(card): #Checking answer
                global SCORE
                SCORE += 1 #Add score
                change_current_question() #Change question
                
                channel1.play(pygame.mixer.Sound(ans_sound))
                sleep(3)
                
                t = Thread(target=shake_head_correct) #Set up the thread
                t.daemon = True        
                t.start() #Start spliting the program into 2 threads
                Eyes('True') #show eyes image and play music
                
            else:
                if HOLD == False:
                    change_current_question()

                channel1.play(pygame.mixer.Sound(ans_sound))
                sleep(3)
                
                t = Thread(target=shake_head_wrong) #Set up the thread
                t.daemon = True
                t.start() #Start spliting the program into 2 threads
                Eyes('False')

            disp.clear()
            disp.display() #Display nothing to the OLED monitor (Clear)


gpio_thread = Thread(target=worker) #Set up the thread
gpio_thread.daemon = True
gpio_thread.start() #Start spliting the program into 2 threads


#PYGAME (Game logic part)
pygame.init() #Initializae pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()


#Pygame parameter
DISPLAY_WIDTH = 480 #Define LCD monitor width
DISPLAY_HEIGHT = 800 #Define LCD monitor height
START_BUTTON_POSITION_X = DISPLAY_WIDTH / 2 / 2 /2
QUIT_BUTTON_POSITION_X = DISPLAY_WIDTH / 2 / 2 + START_BUTTON_POSITION_X * 2
EASY_BUTTON_POSITION_X = DISPLAY_WIDTH / 2 / 2 /2
HARD_BUTTON_POSITION_X = DISPLAY_WIDTH / 2 / 2 + EASY_BUTTON_POSITION_X * 2
font = pygame.font.Font('/home/pi/Desktop/Doll_Therapy/media/font/mnjzbh.ttf', 62)



#Colur
RED = (200, 0, 0)
BRIGHT_RED = (255,0,0)
GREEN = (0,200,0)
BRIGHT_GREEN = (0,255,0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)


screen = pygame.display.set_mode((DISPLAY_WIDTH , DISPLAY_HEIGHT), pygame.RESIZABLE) #show screen
clock = pygame.time.Clock() #initialize the clock

PLAYSOUNDEVENT = pygame.USEREVENT + 2 #Define sound event
pygame.time.set_timer(PLAYSOUNDEVENT, 1000) #Play question mp3 every 1s


#Define the text in the shade area(button)
def text_objects(text, font, color=BLACK):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


#Define Button
def button(msg, x, y, w, h, ic , ac, action = None, parameter = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            sleep(0.3) #Prevent click too fast 
            if parameter == None: #Check parameter, otherwise all function with parameter will be click automatically
                action()
            else:
                action(parameter)
            pygame.display.flip()

    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    textSurf, textRect = text_objects(msg, font)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

#Game introduction, showing hello
def game_intro():
    global CURRENT_STAGE
    CURRENT_STAGE = 'game_intro'
    while True:
        for e in pygame.event.get(): #this part is for game event, something like a receiver
            if e.type == PLAYSOUNDEVENT and not pygame.mixer.music.get_busy():
                intro_sound = glob.glob('/home/pi/Desktop/Doll_Therapy/media/sound/opening/*.mp3')
                intro_sound = choice(intro_sound)
                pygame.mixer.music.load(intro_sound)
                pygame.mixer.music.play()
         
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)

        screen.fill(WHITE) #Set the screen to white constatly

        TextSurf, TextRect = text_objects("你好", font)
        TextRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        screen.blit(TextSurf, TextRect)

        button("開始", START_BUTTON_POSITION_X, DISPLAY_HEIGHT/1.5, 140, 65, GREEN, BRIGHT_GREEN, difficulty)
        button("關機", QUIT_BUTTON_POSITION_X, DISPLAY_HEIGHT/1.5, 140, 65, RED, BRIGHT_RED, quitgame)
        pygame.display.flip() # Update the display screen
        clock.tick(60) #Update the display screen


def difficulty():
    global CURRENT_STAGE
    CURRENT_STAGE = 'difficulty'
    pygame.mixer.music.stop()
    while True:
        for e in pygame.event.get(): #this part is for game event, something like a receiver
            if e.type == PLAYSOUNDEVENT and not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("/home/pi/Desktop/Doll_Therapy/media/sound/difficulty/choice.mp3")
                pygame.mixer.music.play()
         
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)

        screen.fill(WHITE) #Set the screen to white constatly

        TextSurf, TextRect = text_objects("請選擇難度", font)
        TextRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        screen.blit(TextSurf, TextRect)

        button("簡單", EASY_BUTTON_POSITION_X, DISPLAY_HEIGHT/1.5, 140, 65, GREEN, BRIGHT_GREEN, game_loop, 'easy')
        button("困難", HARD_BUTTON_POSITION_X, DISPLAY_HEIGHT/1.5, 140, 65, RED, BRIGHT_RED, game_loop, 'hard')
        button("關機", QUIT_BUTTON_POSITION_X, DISPLAY_HEIGHT/10, 140, 65, RED, BRIGHT_RED, quitgame)

        pygame.display.update() # Update the display screen
        clock.tick(60) #Update the display screen


def udpateScore(): #For Testing
    global SCORE, CURRENT_QUESTION, QUESTION_COUNT, CURRENT_QUESTION_NUMBER
    SCORE += 1
    QUESTION_COUNT -= 1
    if QUESTION_COUNT != 0:
        CURRENT_QUESTION = QUESTION.pop(0)
        CURRENT_QUESTION_NUMBER = CURRENT_QUESTION[re.search('\d', CURRENT_QUESTION).start():].replace('.mp3', '')
    else:
        game_end()

#Main game logic
def game_loop(difficult = None):
    global CURRENT_STAGE
    CURRENT_STAGE = 'game_loop'
    #print('Here is game loop, the difficultly is ', difficult)
    #Access the global parameter for accessing game resources (First start + Restart)
    global QUESTION, QUESTION_COUNT, CURRENT_QUESTION, CURRENT_QUESTION_IMAGE, SCORE, CURRENT_QUESTION_NUMBER

    if difficult == 'easy':
        QUESTION = glob.glob("/home/pi/Desktop/Doll_Therapy/media/question/*.mp3")
    elif difficult == 'hard':
        QUESTION = glob.glob("/home/pi/Desktop/Doll_Therapy/media/question_hard/*.mp3")

    # Re-initilize global data 
    QUESTION_COUNT = len(QUESTION)
    shuffle(QUESTION)
    CURRENT_QUESTION = QUESTION.pop(0)
    CURRENT_QUESTION_NUMBER = CURRENT_QUESTION[re.search('\d', CURRENT_QUESTION).start():].replace('.mp3', '')
    SCORE = 0

    # Set countign time and event
    counter, time = 60, '60'.rjust(3) #SET COUNT TIME
    COUNTTIMEEVENT = pygame.USEREVENT + 1 #Define count time event
    pygame.time.set_timer(COUNTTIMEEVENT, 1500) #The count time event repeat every 1s

    # Load the first question before while loop
    quest = CURRENT_QUESTION #Get the first question before loping
    pygame.mixer.music.load(quest) #Safely load the question music
    pygame.mixer.music.play() #Play the question music
    tag = TinyTag.get(quest) #Get the mp3 file metadata (question)
    quest_text = tag.title
    if difficult == 'easy':
        temp = quest
        CURRENT_QUESTION_IMAGE = temp.replace('mp3', 'jpg').replace('question', 'game_image')
    elif difficult == 'hard':
        temp = quest
        CURRENT_QUESTION_IMAGE = temp.replace('mp3', 'jpg').replace('question_hard', 'game_image_hard')
    print('The question is :',quest, '; The question image is: ', CURRENT_QUESTION_IMAGE, '; Number of question left: ', QUESTION_COUNT)
    

    while True:
        for e in pygame.event.get(): #EVENT handling
            if e.type == COUNTTIMEEVENT: #counting time
                counter -= 1 # The time count decrease 1 (this event happen every 1s)
                time = str(counter).rjust(3) if counter > 0 else 'TIMES UP'
                if counter == 0: #if time count to 0, end game
                    game_end()

            if e.type == PLAYSOUNDEVENT and not pygame.mixer.music.get_busy() and not channel1.get_busy(): # play sound event after sound effect finish and the question is not asking
                quest = CURRENT_QUESTION
                pygame.mixer.music.load(quest)
                pygame.mixer.music.play()
                tag = TinyTag.get(quest)
                quest_text = tag.title
                if difficult == 'easy':
                    temp = quest
                    CURRENT_QUESTION_IMAGE = temp.replace('mp3', 'jpg').replace('question', 'game_image')

                elif difficult == 'hard':
                    temp = quest
                    CURRENT_QUESTION_IMAGE = temp.replace('mp3', 'jpg').replace('question_hard', 'game_image_hard')
                
                print('The question is :',quest, '; The question image is: ', CURRENT_QUESTION_IMAGE, '; Number of question left: ', QUESTION_COUNT)

            if e.type == pygame.QUIT: #Close the computer event
                quitgame()

        screen.fill(WHITE)

        #Show the time counting
        timeSurf, timeRect = text_objects(time, font)
        timeRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT/5)
        screen.blit(timeSurf, timeRect)

        #Show the question
        questSurf, questRect = text_objects(quest_text, font)
        questRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT/3.5)
        screen.blit(questSurf, questRect)

        #Show the question image
        quest_image = pygame.image.load(CURRENT_QUESTION_IMAGE)
        screen.blit(quest_image,((DISPLAY_WIDTH / 5), (DISPLAY_HEIGHT/2.5)))

        button("跳過", 0, 0, 140, 65, RED, BRIGHT_RED, pass_ans)
        
        ##if get_HOLD() == True:
            ##button("HELD", 280, 0, 140, 65, RED, BRIGHT_RED, set_HOLD)
        ##else:
            ##button("HOLD", 280, 0, 140, 65, GREEN, BRIGHT_GREEN, set_HOLD)

        #button("TEST", 0, 0, 120, 50, RED, BRIGHT_RED, udpateScore)


        if QUESTION_COUNT == 0: #End game if the number of question is 0
            game_end()

        if channel1.get_busy() and pygame.mixer.music.get_busy(): #Stop the question asking when playing sound effect
            pygame.mixer.music.stop()

        pygame.display.flip()
        clock.tick(60)


#End game
def game_end():
    global CURRENT_STAGE
    CURRENT_STAGE = 'game_end'
    end_sound = glob.glob('/home/pi/Desktop/Doll_Therapy/media/sound/timesup/*.mp3')
    end_sound = choice(end_sound)
    #print(end_sound)
    pygame.mixer.music.load(end_sound)   
    pygame.mixer.music.play()
    TEXT = ""
    COLOR = (0,0,0)
    
    if SCORE > 10:
        score_sound = ['/home/pi/Desktop/Doll_Therapy/media/sound/cheerup/vgood.mp3']
    elif SCORE > 5:
        score_sound = ['/home/pi/Desktop/Doll_Therapy/media/sound/cheerup/good.mp3']
    elif SCORE >= 1:
        score_sound = ['/home/pi/Desktop/Doll_Therapy/media/sound/cheerup/notbad.mp3']
    else:
        score_sound = ['/home/pi/Desktop/Doll_Therapy/media/sound/cheerup/again.mp3']
        
    while True:
        for e in pygame.event.get():
            if e.type == PLAYSOUNDEVENT and not pygame.mixer.music.get_busy() and len(score_sound) == 1:
                pygame.mixer.music.load(score_sound.pop(0))
                pygame.mixer.music.play()
                                   
            if e.type == pygame.QUIT:
                        quitgame()

        screen.fill(WHITE)  

        if SCORE > 10: #Show different label to the elderly according to their score
            TEXT = "十分好!!!"
            COLOR = BRIGHT_GREEN
            
        elif SCORE > 5:
            TEXT = "做得好!"
            COLOR = GREEN
            
        elif SCORE >= 1:
            TEXT = "不錯哦~"
            COLOR = GREEN
            
        else:
            TEXT = "再接再勵~"
            COLOR = RED
            
        #Show the cheer up response to the elderly
        textSurf, textRect = text_objects(TEXT, font, COLOR)
        textRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT/2)
        screen.blit(textSurf, textRect)

        #Show the score
        scoreSurf, scoreRect = text_objects(str(SCORE), font)
        scoreRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT/3)
        screen.blit(scoreSurf, scoreRect)

        button("開始", START_BUTTON_POSITION_X, DISPLAY_HEIGHT/1.5, 140, 65, GREEN, BRIGHT_GREEN, difficulty)
        button("關機", QUIT_BUTTON_POSITION_X, DISPLAY_HEIGHT/1.5, 140, 65, RED, BRIGHT_RED, quitgame)
        
        pygame.display.flip()
        clock.tick(60)


#Quit game function (PRODUCTION)
#def quitgame():
    #pygame.quit()
    #quit()
    #os.system('sudo shutdown now')


#Quit game function (DEV)
def quitgame():
    pygame.quit()
    disp.clear()
    quit()

   
def pass_ans():
    global CURRENT_QUESTION, QUESTION, QUESTION_COUNT
    QUESTION_COUNT -= 1
    CURRENT_QUESTION = QUESTION.pop(0)

def set_HOLD():
    global HOLD
    HOLD = not HOLD
    
def get_HOLD():
    global HOLD
    return HOLD
#Run the game introduction loop
#Close the program if introduction loop break


#worker()
game_intro()
pygame.quit()
quit()


