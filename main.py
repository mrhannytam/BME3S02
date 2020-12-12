import sys, pygame #pygame game logic
from time import sleep #hard coding
import glob #get a list of files
from random import shuffle # random question sequence
from tinytag import TinyTag # access mp3 title 
import math #set question repeat time 

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 500
START_BUTTON_POSITION_X = DISPLAY_WIDTH / 2 / 2 /2
QUIT_BUTTON_POSITION_X = DISPLAY_WIDTH / 2 / 2 + START_BUTTON_POSITION_X * 2
font = pygame.font.Font('mnjzbh.ttf', 30)

RED = (200, 0, 0)
BRIGHT_RED = (255,0,0)
GREEN = (0,200,0)
BRIGHT_GREEN = (0,255,0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
SCORE = 0

screen = pygame.display.set_mode((DISPLAY_WIDTH , DISPLAY_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

QUESTION = glob.glob("media/question/*.mp3")
shuffle(QUESTION)
CURRENT_QUESTION = QUESTION.pop(0)

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

def change_current_question():
    CURRENT_QUESTION = QUESTION.pop(0)

def check_answer(ans):
    if ans == CURRENT_QUESTION:
        return True
    else:
        return False

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

    counter, time = 5, '5'.rjust(3)
    COUNTTIMEEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(COUNTTIMEEVENT, 1000)

    PLAYSOUNDEVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(PLAYSOUNDEVENT, 6000)

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

            if e.type == PLAYSOUNDEVENT:
                quest = CURRENT_QUESTION
                pygame.mixer.music.load(quest)
                pygame.mixer.music.play()
                tag = TinyTag.get(quest)
                quest_text = tag.title

            if e.type == pygame.USEREVENT:
                print('hi')


                #TODO: RFID AND LED

                
            if e.type == pygame.QUIT:
                gameExit = True
                
        screen.fill(WHITE)
        timeSurf, timeRect = text_objects(time, font)
        timeRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT/4)
        screen.blit(timeSurf, timeRect) 

        questSurf, questRect = text_objects(quest_text, font)
        questRect.center = (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT/2)
        screen.blit(questSurf, questRect)
        
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
        if SCORE > 25:
            TEXT = "十分好!!!"
            COLOR = BRIGHT_GREEN
        elif SCORE > 15:
            TEXT = "做得好!"
            COLOR = GREEN
        else:
            TEXT = "不錯哦~"
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
    quit()
    #TODO: os.sys("sudo shutdown now -h")

game_intro()
pygame.quit()
quit()
