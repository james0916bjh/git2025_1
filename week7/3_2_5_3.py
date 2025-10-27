# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 스위치 핀 (BCM 기준)
switch_pins = [5, 6, 13, 19]
switch_names = ["1", "2", "3", "4"]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 입력 핀 설정 (내부 풀다운 사용)
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 이전 상태 저장용 리스트
prev_values = [0, 0, 0, 0]

try:
    while True:
        for idx, pin in enumerate(switch_pins):
            value = GPIO.input(pin)

            # ★ 0 -> 1 변화(즉, 눌렀을 때만) 감지 ★
            if prev_values[idx] == 0 and value == 1:
                print("click " + switch_names[idx])
                time.sleep(0.05)  # 디바운싱(짧은 지연)

            prev_values[idx] = value  # 현재 상태를 이전 상태로 저장

        time.sleep(0.01)  # CPU 부하 감소용 딜레이

except KeyboardInterrupt:
    pass

GPIO.cleanup()
