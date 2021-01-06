import RPi.GPIO as GPIO
import time


PWM_FREQ = 50
STEP=15
CONTROL_PIN2 = 18


GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN2, GPIO.OUT)


pwm2 = GPIO.PWM(CONTROL_PIN2, PWM_FREQ)
pwm2.start(0)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ *angle / 180)
    return duty_cycle

try:
    print('Ctrl+c to stop the program')
    #motor 2 mouth
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(110))
    time.sleep(0.3)
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(160))
    time.sleep(0.3)
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(110))
    time.sleep(0.3)
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(160))
    time.sleep(0.3)
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(110))
    time.sleep(0.3)
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(110))
    time.sleep(0.3)
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(160))
    time.sleep(0.3)
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(110))
    time.sleep(0.3)
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(160))
    time.sleep(0.3)
    pwm2.ChangeDutyCycle(angle_to_duty_cycle(110))
    time.sleep(0.3)

    while True:
        next
except KeyboardInterrupt:
    print('close')
finally:
    pwm2.stop()
    GPIO.cleanup()
