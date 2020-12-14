# BME3S02 Doll Therapy

1. media/question2 is for testing
2. media/sound2 is for shorter loading time, better performance

test_rfid.py for testing the code of RFID card
write_rfid.py for writing the code of RFID card
test_oled.py for tsting the OLED monitor

The program splits at two part (threads)
1. work()---for raspberry pi GPIO I2C
2. pygame---for the game logic
!!! The work() used pygame's music function (BAD practce)(interrupt constatly -> sound interrupt / bugs -> restart computer)
!!! The Close computer button is real close, dont't click it!!!
!!! Use the Ctrl + C to interrupt the terminal to close the program!!!
!!! Run the program by typing python3 main.py!!!
