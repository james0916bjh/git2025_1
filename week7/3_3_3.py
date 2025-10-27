# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 핀 설정
BUZZER = 12
SW1 = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# PWM 객체 생성
pwm = GPIO.PWM(BUZZER, 440)

# 음계 주파수 
FREQ = {
    "도": 262, "레": 294, "미": 330, "파": 349,
    "솔": 392, "라": 440, "시": 494, "도5": 523
}

# "떳다 떳다 비행기" 
MELODY = [
    ("미",1), ("미",1), ("파",1), ("솔",1),
    ("솔",1), ("파",1), ("미",1), ("레",1)
]

BPM = 120
beat_sec = 60.0 / BPM

def play_melody():
    pwm.start(50)
    for note, beats in MELODY:
        freq = FREQ[note]
        pwm.ChangeFrequency(freq)
        time.sleep(beat_sec * beats * 0.9)
        pwm.ChangeDutyCycle(0)
        time.sleep(beat_sec * beats * 0.1)
        pwm.ChangeDutyCycle(50)
    pwm.stop()

try:
    prev_val = 0
    while True:
        val = GPIO.input(SW1)
        # 0 -> 1 변화 (눌렀을 때만)
        if prev_val == 0 and val == 1:
            print("SW1 click → 경적 울림")
            play_melody()
            time.sleep(0.2)  # 디바운스
        prev_val = val
        time.sleep(0.01)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
