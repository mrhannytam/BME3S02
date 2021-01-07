import RPi.GPIO as GPIO
import time

CONTROL_PIN = 17
PWM_FREQ = 50
STEP=15

GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ *angle / 180)
    return duty_cycle

try:
    print('Ctrl+c to stop the program')
    for angle in range(0, 181, STEP):
        dc = angle_to_duty_cycle (angle)
        pwm.ChangeDutyCycle(dc)
        print('an={:>3}, p={:.2f}'.format(angle,dc))
        time.sleep(2)
    for angle in range(180, -1, -STEP):
        dc = angle_to_duty_cycle(angle)
        print('an={:>3}, p={:.2f}'.format(angle,dc))
        pwm.ChangeDutyCycle(dc)
        time.sleep(2)
    pwm.ChangeDutyCycle(angle_to_duty_cycle(90))
    while True:
        next
except KeyboardInterrupt:
    print('close')
finally:
    pwm.stop()
    GPIO.cleanup()