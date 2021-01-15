import RPi.GPIO as GPIO
import time

CONTROL_PIN = 17
PWM_FREQ = 50
STEP=15
<<<<<<< HEAD

GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)
GPIO.setwarnings(False)
pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)
=======
CONTROL_PIN2 = 18


GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)
pwm2 = GPIO.PWM(CONTROL_PIN2, PWM_FREQ)
pwm2.start(0)
>>>>>>> 34d5323c11d21c7a391a1323f908a68eaddb2d6e

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ *angle / 180)
    return duty_cycle

try:
    print('Ctrl+c to stop the program')
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
<<<<<<< HEAD
=======

    #motor 2 mouth
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(90))
    time.sleep(0.3)
    

>>>>>>> 34d5323c11d21c7a391a1323f908a68eaddb2d6e
    while True:
        next
except KeyboardInterrupt:
    print('close')
finally:
    pwm.stop()
    GPIO.cleanup()
