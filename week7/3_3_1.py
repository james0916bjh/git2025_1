
import RPi.GPIO as GPIO
import time

BUZZER = 12 # BCM 핀 번호 


# C4~C5 기준 주파수(Hz)
scale = [
    (u"도", 262),
    (u"레", 294),
    (u"미", 330),
    (u"파", 349),
    (u"솔", 392),
    (u"라", 440),
    (u"시", 494),
    (u"도", 523),
]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

# PWM 시작 
pwm = GPIO.PWM(BUZZER, 440)
pwm_started = False

try:
    for name, freq in scale:
        if not pwm_started:
            pwm.start(50)          # 50% duty
            pwm_started = True
        pwm.ChangeFrequency(freq)  # 음 높이 변경
        print((name, freq))        # 현재 재생하는 음과 주파수 표시
        time.sleep(0.4)            # 각 음 길이 (초)
        pwm.ChangeDutyCycle(0)     # 음 사이에 살짝 끊어주기
        time.sleep(0.05)
        pwm.ChangeDutyCycle(50)
finally:
    pwm.stop()
    GPIO.cleanup()
