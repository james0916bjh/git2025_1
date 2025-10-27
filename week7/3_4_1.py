# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 왼쪽 모터 핀
PWMA = 18
AIN1 = 22
AIN2 = 27

# 오른쪽 모터 핀
PWMB = 23
BIN1 = 25
BIN2 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 핀 모드 설정
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)

GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# PWM 객체 생성 (주파수 500Hz)
L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)

L_Motor.start(0)
R_Motor.start(0)

try:
    while True:
        # 1️⃣ 정방향 회전 (50% 속도)
        GPIO.output(AIN1, 0)
        GPIO.output(AIN2, 1)
        GPIO.output(BIN1, 0)
        GPIO.output(BIN2, 1)
        L_Motor.ChangeDutyCycle(50)
        R_Motor.ChangeDutyCycle(50)
        print("정방향 50% 회전")
        time.sleep(1.0)

        # 2️⃣ 정지
        L_Motor.ChangeDutyCycle(0)
        R_Motor.ChangeDutyCycle(0)
        print("정지")
        time.sleep(1.0)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
