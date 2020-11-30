import sys, pygame #pygame game logic
from time import sleep #hard coding
import glob #get a list of files
from random import shuffle # random question sequence

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init() 

DISPLAY_WIDTH = 500
DISPLAY_HEIGHT = 700
START_BUTTON_POSITION = DISPLAY_WIDTH / 2 / 2 
QUIT_BUTTON_POSITION = DISPLAY_WIDTH / 2 + START_BUTTON_POSITION
font = pygame.font.SysFont('Consolas', 30)
RED = (200, 0, 0)
BRIGHT_RED = (255,0,0)
GREEN = (0,200,0)
BRIGHT_GREEN = (0,255,0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
SCORE = 0

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
        TextSurf, TextRect = text_objects("Welcome", font)
        TextRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        screen.blit(TextSurf, TextRect)
        button("Start", START_BUTTON_POSITION,450,100,50, GREEN, BRIGHT_GREEN, game_loop)
        button("Quit", QUIT_BUTTON_POSITION,450,100,50, RED, BRIGHT_RED, quitgame)
        pygame.display.update()
        clock.tick(15)

def game_loop():
    gameExit = False
    counter, time = 1, '1'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    QUESTION = glob.glob("media/question/*.mp3")
    shuffle(QUESTION)
    pygame.mixer.music.load(QUESTION.pop(0))
    pygame.mixer.music.play()
    while not gameExit:
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT:
                counter -= 1
                time = str(counter).rjust(3) if counter > 0 else 'TIMES UP'
     
                if counter % 10 == 0:
                    pygame.mixer.music.load(QUESTION.pop(0))
                    pygame.mixer.music.play()
                #TODO: RFID AND LED

                if counter == 0:
                    game_end()
            if e.type == pygame.QUIT:
                gameExit = True

        screen.fill(WHITE)
        screen.blit(font.render(time, True, BLACK), (DISPLAY_WIDTH / 2, 48))
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
            TEXT = "EXCELLENT"
            COLOR = BRIGHT_GREEN
        elif SCORE > 15:
            TEXT = "GOOD"
            COLOR = GREEN
        else:
            TEXT = "NOT BAD"
            COLOR = RED
        screen.blit(font.render(TEXT, True, COLOR), (DISPLAY_WIDTH / 2, 48))
        screen.blit(font.render(str(SCORE), True, COLOR), (DISPLAY_WIDTH / 2 / 2, 100))
        
        button("Restart", START_BUTTON_POSITION,450,100,50, GREEN, BRIGHT_GREEN, game_loop)
        button("Quit", QUIT_BUTTON_POSITION,450,100,50, RED, BRIGHT_RED, quitgame)
        
        pygame.display.flip()
        clock.tick(60)

def quitgame():
    pygame.quit()
    quit()
    #TODO: os.sys("sudo shutdown now -h")

game_intro()
pygame.quit()
quit()