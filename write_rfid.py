import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

try:
    reader = SimpleMFRC522()
    text = input("type new data you want to written to the card: ")
    print('Place your tag to write')
    reader.write(text)
    print('Written')
finally:
    GPIO.cleanup()