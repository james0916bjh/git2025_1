# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time


BUZZER = 12          # PWM 가능: 물리 12
SW_MI  = 5           # 미
SW_FA  = 6           # 파
SW_SOL = 13          # 솔
SW_RE  = 19          # 레

# 음 주파수(Hz)
FREQ = {
    u"미": 330,
    u"파": 349,
    u"솔": 392,
    u"레": 294,
}

# 스캔 우선순위(앞에 있는 게 우선)
KEYS = [
    (SW_MI,  u"미"),
    (SW_FA,  u"파"),
    (SW_SOL, u"솔"),
    (SW_RE,  u"레"),
]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 입력(내부 풀다운)
for pin, _ in KEYS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 버저 출력(PWM)
GPIO.setup(BUZZER, GPIO.OUT)
pwm = GPIO.PWM(BUZZER, 440)
pwm.start(0)   # 처음엔 무음
current_note = None

try:
    while True:
        pressed_note = None

        # 어떤 스위치가 눌렸는지 확인 (0->1 눌림 상태 유지 시에도 울림)
        for pin, name in KEYS:
            if GPIO.input(pin) == 1:
                pressed_note = name
                break  # 첫 번째로 발견한 스위치만 재생

        if pressed_note is None:
            # 아무 것도 안 눌림 → 무음
            if current_note is not None:
                pwm.ChangeDutyCycle(0)
                current_note = None
        else:
            # 음이 바뀌었을 때만 주파수 변경
            if pressed_note != current_note:
                pwm.ChangeFrequency(FREQ[pressed_note])
                pwm.ChangeDutyCycle(60)   # 음량 느낌
                print(u"Play: " + pressed_note)
                current_note = pressed_note

        time.sleep(0.01)  # 폴링 주기

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
