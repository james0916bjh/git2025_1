# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 4개 스위치 (BCM 핀)
switch_pins  = [5, 6, 13, 19]
switch_names = ["SW1", "SW2", "SW3", "SW4"]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 입력 + 내부 풀다운
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 전/후 상태와 누른 횟수
prev_vals    = [0, 0, 0, 0]   # 이전 값 저장
click_counts = [0, 0, 0, 0]   # 스위치별 클릭 횟수

try:
    while True:
        # 현재 값들 한 번에 읽어서 리스트에 저장
        curr_vals = [GPIO.input(pin) for pin in switch_pins]

        # 0 -> 1(눌림) 변화만 감지
        for i in range(len(switch_pins)):
            if prev_vals[i] == 0 and curr_vals[i] == 1:
                click_counts[i] += 1
                # 예시 출력 형태: ('SW1 click', 1)
                print((switch_names[i] + " click", click_counts[i]))
                time.sleep(0.2)  # 간단 디바운스

        # 현재 값을 다음 루프를 위한 이전 값으로
        prev_vals = curr_vals[:]

        time.sleep(0.01)  

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
