# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time


PWMA = 18   # 왼쪽 모터 속도 제어 
PWMB = 23   # 오른쪽 모터 속도 제어 
AIN1 = 22   # 왼쪽 모터 방향 제어 1
AIN2 = 27   # 왼쪽 모터 방향 제어 2
BIN1 = 25   # 오른쪽 모터 방향 제어 1
BIN2 = 24   # 오른쪽 모터 방향 제어 2


SW1 = 5     # 전진
SW2 = 6     # 우회전
SW3 = 13    # 좌회전
SW4 = 19    # 후진

# 스위치 입력 설정 (풀다운 저항 사용)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 모터 출력 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# PWM 객체 생성
L_Motor = GPIO.PWM(PWMA, 500)
L_Motor.start(0)  # 왼쪽 모터 정지
R_Motor = GPIO.PWM(PWMB, 500)
R_Motor.start(0)  # 오른쪽 모터 정지

# 앞으로 전진
def forward():
    print('forward button')
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)
    time.sleep(1.0)
    # 모터 정지
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)
    time.sleep(1.0)

# 오른쪽 회전
def right():
    print('right button')
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)
    time.sleep(1.0)
    # 모터 정지
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)
    time.sleep(1.0)

# 왼쪽 회전
def left():
    print('left button')
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)
    time.sleep(1.0)
    # 모터 정지
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)
    time.sleep(1.0)

# 후진
def back():
    print('back button')
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(50)
    R_Motor.ChangeDutyCycle(50)
    time.sleep(1.0)
    # 모터 정지
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)
    time.sleep(1.0)

try:
    while True:
        # 스위치 상태 읽기 (1=눌림)
        SW1Status = GPIO.input(SW1)
        SW2Status = GPIO.input(SW2)
        SW3Status = GPIO.input(SW3)
        SW4Status = GPIO.input(SW4)

        # 각 버튼에 따라 동작 실행
        if SW1Status == 1:
            forward()
        elif SW2Status == 1:
            right()
        elif SW3Status == 1:
            left()
        elif SW4Status == 1:
            back()

except KeyboardInterrupt:  
    pass

# GPIO 핀 초기화
GPIO.cleanup()
