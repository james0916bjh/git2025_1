import RPi.GPIO as GPIO
import time

SW1 = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    prevValue = 0 
    while True:
        sw1Value = GPIO.input(SW1)
        if sw1Value == 1 and prevValue == 0:  
            print("click")
        prevValue = sw1Value 
        time.sleep(0.05)       

except KeyboardInterrupt:
    pass

GPIO.cleanup()
