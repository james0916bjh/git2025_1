# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

BUZZER = 12      
BPM    = 112     # 템포
DUTY   = 60      # 음량 느낌(듀티비)

FREQ = {
    u"도":262, u"레":294, u"미":330, u"파":349, u"솔":392, u"라":440, u"시":494,
    u"도5":523, u"레5":587, u"미5":659, u"파5":698, u"솔5":784, u"라5":880, u"시5":988
}


MELODY = [
    (u"미",1), (u"미",1), (u"파",1), (u"솔",1),   # 떳-다 떳-다 비-
    (u"솔",1), (u"파",1), (u"미",1), (u"레",1),   # 행-기py
]



beat_sec = 60.0 / BPM  # 1박 길이(초)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

pwm = GPIO.PWM(BUZZER, 440)  # 초기 주파수 임의
pwm_started = False

def play_note(name, beats):
    dur = beat_sec * beats
    if name == u"쉼":
        # 무음
        pwm.ChangeDutyCycle(0)
        time.sleep(dur)
        return
    freq = FREQ.get(name, None)
    if freq is None:
        return
    if not pwm_started:
        pass  

    pwm.ChangeFrequency(freq)
    pwm.ChangeDutyCycle(DUTY)
    time.sleep(dur * 0.9)   
    pwm.ChangeDutyCycle(0)
    time.sleep(dur * 0.1)

try:
    pwm.start(0)
    pwm_started = True
    for n, b in MELODY:
        play_note(n, b)
finally:
    pwm.stop()
    GPIO.cleanup()
