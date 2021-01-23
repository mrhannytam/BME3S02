# B=M=E=3=S=0=2= D=o=l=l= T=h=e=r=a=p=y=

## Hardware Requirement
1. Raspberry pi
2. RC522
3. 128*64 OLED


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
3. requirement.txt
4. main.py
5. maintest.py
6. test_oled.py
7. test_rfid.py
8. write_rfid.py
9. test_motor.py
10. test_motor_move.py
11. media
    * ans
    * font
    * game_image
    * game_image_hard
    * question
    * question_hard
    * sound
    * cheerup
    * difficulty
    * effect
    * opening
    * timesup



## Main Program
* The main program splits two parts (threads)
    1. GPIO control
    2. Pygame game control

* Each threads access the global variables
    * QUESTION -> 
    * QUESTION_COUNT
    * CURRENT_QUESTION
    * CURRENT_QUESTION_NUMBER
    * CURRENT_CARD
    * SCORE
    * HOLD


* GPIO Control Functions
    * Eyes(boolean)
    * Eyes: blink()
    * Eyes: slowblink()
    * Motor_head(boolean)
    * Motor_mouth(boolean)
    * shake_head_correct()
    * shake_head_wrong()
    * change_current_question()
    * check_answer(int)


* Pygame Game Control Functions
    * text_objects(string, font, tuple)
    * button(string, int, int, int, int, tuple, tuple, function, string)
    * game_intro()
    * difficulty()
    * game_loop()
    * game_end()
    * quitgame()
    * updateScore()
    * pass_ans()
    * set_HOLD()
    * get_HOLD()


## Production Reminder
1. Change the quitgame() from DEV to PRODUCTION
2. Rotate the computer screen 90 degree
    * Add the following code into /boot/config.txt 
        ```
        max_usb_current=1
        hdmi_force_hotplug=1
        config_hdmi_boost=7
        hdmi_group=2
        hdmi_mode=1
        hdmi_mode=87
        hdmi_drive=1
        hdmi_cvt 800 480 60 6 0 0 0
        display_rotate = 3
        ```

    * Installing X Server driver
        ```
        sudo apt get install xserver-xorg-input-libinput
        sudo mkdir etc/X11/xorg.conf.d
        sudo cp /usr/share/X11/xorg.conf.d/40-libinput.conf /etc/X11/xorg.conf.d/
        sudo nano /etc/X11/xorg.conf.d/40-libinput.conf
        ```
    * Change the option CalibrationMatrix to "0 1 0 1 0 1 0 0 1"
    ![](https://i.imgur.com/vUmSD5B.png)

3. Adjust the screen size (DISPLAY_WIDTH and DISPLAY_HEIGHT)
4. Run the script when computer boot [Method 2 HERE](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)
5. Dont use other methods especially /etc/profile!!! since the program runs 2 threads. This will make the computer crush. [RECOVER HERE](https://www.paragon-software.com/home/linuxfs-windows/#oem)


## Upload Code
```
git pull
git add . 
git commit -m 'your comment'
git push
```
