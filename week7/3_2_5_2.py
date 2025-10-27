# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 스위치 핀 (BCM)
switch_pins = [5, 6, 13, 19]
switch_names = ["1", "2", "3", "4"]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prev_values = [0, 0, 0, 0]

try:
    while True:
        for idx, pin in enumerate(switch_pins):
            value = GPIO.input(pin)
            if value == 1 and prev_values[idx] == 0:  # 눌리는 순간
                print("click " + switch_names[idx])   
                time.sleep(0.2)                      # 디바운싱
            prev_values[idx] = value
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
