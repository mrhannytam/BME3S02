import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

try:
    reader = SimpleMFRC522()
    text = input('New data')
    print('Place your tag to write')
    reader.write(text)
    print('Written')
finally:
    GPIO.cleanup()