# B=M=E=3=S=0=2= D=o=l=l= T=h=e=r=a=p=y=

## Hardware Requirement
1. Raspberry pi
2. RC522
3. 12864 OLED


## Software Requirement
1. Pre-installed Raspberry pi OS
2. Update OS (Follow the first boot instructions)
3. Download python3, pip3
4. Install all required python library

## Download
```
sudo apt-get update
sudo apt-get upgrade
pip3 install tinytag RPi.GPIO mfrc522 Adafruit-SSD1306
cd ~/Desktop/
git clone https://github.com/mrhannytam/Doll_Therapy.git
python3 /home/pi/Desktop/Doll_Therapy/main.py
```

## Introduction
Project Structure:
1. .git
2. README.MD
3. main.py (Main Program!!!)
4. test_oled.py (Test the OLED monitor)
5. test_rfid.py (Display content from IC card)
6. write_rfid.py (Write content to the IC card)
7. testing.py (for testing shit)
8. media
    * font 
    * image (For further development)
    * question (All mp3 question audio)
    * sound (Abandoned)
    * question 2 (For testing)
    * sound 2 (Sound effect)


## Main Program
* The main program splits two parts (threads)
    1. GPIO control
    2. Pygame game control

* Each threads access the global variables
    * QUESTION (A list contain all questions' mp3 path)
    * CURRENT_QUESTION (Sored the current question's mp3 path)
    * SCORE

* GPIO Control Functions
    * Eyes(bool) -> Control OLED monitor + play sound effect
    * change_current_question() -> Change CURRENT_QUESTION
    * check_answer(int) -> Check the content of IC Card == mp3 file name

* Pygame Game Control Functions
    * button(str, int, int, int, int, tuple, tuple, function) -> Define a button with action
    * text_objects(str, pygame.font.Font) -> Define a Text
    * game_intro() -> Welcome Page
    * game_loop() -> Main game logic
    * game_end() -> End game Page
    * quitgame() -> Quit entire game
        *  PRODUCTION: Really turn off the computer
        *  DEV: Turn off the pygame
        *  i.e. Comment or commend out the code by yourself!!!

## Production Reminder
1. Change the quitgame() from DEV to PRODUCTION
2. Rotate the computer screen 90 degree [HERE](https://www.debugpoint.com/2019/12/how-to-rotate-display-in-ubuntu-linux/) or "sudo nano /boot/config.txt"
3. Adjust the screen size (DISPLAY_WIDTH and DISPLAY_HEIGHT)
4. Run the script when computer boot [Method 1 HERE](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)
5. Dont use other methods especially /etc/profile!!! since the program runs 2 threads. This will make the computer like a SHIT. [RECOVER HERE 1](https://raspberrypi.stackexchange.com/questions/83369/how-to-stop-a-python-script-running-at-startup-by-default#:~:text=You%20can%20try%20spamming%20ALT,of%20the%20script%20execution%20command.), [RECOVER HERE 2](https://www.howtogeek.com/112888/3-ways-to-access-your-linux-partitions-from-windows/)


## Upload Code
1. git add . 
2. git commit -m 'your comment'
3. git push
