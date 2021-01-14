from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

try:
    while True:
            id, text = reader.read()
            card = int(text)
            print(card)

except KeyboardInterrupt:
    print('close')

finally:
    GPIO.cleanup()