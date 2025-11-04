# -*- coding: utf-8 -*-
# BT 조이스틱(J0:angle,power) 기반 모터 제어(버튼식) + 스무딩/안정화

import RPi.GPIO as GPIO
import serial
import threading
import time
import re

# 핀
PWMA = 18
PWMB = 23
AIN1 = 22
AIN2 = 27
BIN1 = 25
BIN2 = 24

# 파라미터
PWM_FREQ = 250
TIMEOUT_SEC = 0.7      # 수신 끊기면 정지
DEADZONE = 0.2         # 약한 입력 무시
SECTOR_STABLE_N = 2    # 같은 섹터 N회 연속 시 전환
RAMP_STEP = 10.0       # 듀티 변화량(0~100)
LOOP_DT = 0.02

# 각도 섹터
RIGHT_RANGE = lambda ang: (ang >= 315 or ang < 45)
FWD_RANGE   = lambda ang: (45 <= ang < 135)
LEFT_RANGE  = lambda ang: (135 <= ang < 225)
BACK_RANGE  = lambda ang: (225 <= ang < 315)

# GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, PWM_FREQ)
R_Motor = GPIO.PWM(PWMB, PWM_FREQ)
L_Motor.start(0)
R_Motor.start(0)

# 시리얼
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.05)

# 상태
last_rx_ts = time.time()
stop_event = threading.Event()
latest_angle = None
latest_power = 0.0
g_lock = threading.Lock()

prev_cmd = "stop"
pending_cmd = "stop"
pending_cnt = 0

cur_left_dc = 0.0
cur_right_dc = 0.0

# 유효 패킷: J0:angle,power
PKT_RE = re.compile(r'^J0:\s*([0-9]{1,3}(?:\.\d+)?),\s*(0(?:\.\d+)?|1(?:\.0+)?)$')

# 모터 제어
def set_dir_speed(left_dc, right_dc):
    if left_dc >= 0:
        GPIO.output(AIN1, 0); GPIO.output(AIN2, 1)
    else:
        GPIO.output(AIN1, 1); GPIO.output(AIN2, 0)
    if right_dc >= 0:
        GPIO.output(BIN1, 0); GPIO.output(BIN2, 1)
    else:
        GPIO.output(BIN1, 1); GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(min(100, abs(left_dc)))
    R_Motor.ChangeDutyCycle(min(100, abs(right_dc)))

def stop_motor():
    GPIO.output(AIN1, 0); GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 0); GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)

def targets_for_cmd(cmd):
    if cmd == "go":   return +100, +100
    if cmd == "left": return +50,  +100
    if cmd == "right":return +100, +50
    if cmd == "back": return -100, -100
    return 0.0, 0.0

def which_sector(angle_deg):
    if FWD_RANGE(angle_deg):  return "go"
    if LEFT_RANGE(angle_deg): return "left"
    if BACK_RANGE(angle_deg): return "back"
    return "right"

def ramp_to(cur, target, step):
    if target > cur:  return min(target, cur + step)
    if target < cur:  return max(target, cur - step)
    return cur

# 수신 스레드(라인 버퍼 + 정규식)
def serial_thread():
    global last_rx_ts, latest_angle, latest_power
    buf = ""
    while not stop_event.is_set():
        try:
            chunk = bleSerial.read(bleSerial.in_waiting or 1).decode('utf-8', errors='ignore')
            if not chunk:
                continue
            buf += chunk
            lines = buf.splitlines(keepends=False)
            if not buf.endswith('\n') and not buf.endswith('\r'):
                buf = lines.pop()
            else:
                buf = ""
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                m = PKT_RE.match(line)
                if not m:
                    continue
                ang = float(m.group(1)) % 360.0
                pwr = float(m.group(2))
                with g_lock:
                    latest_angle = ang
                    latest_power = pwr
                last_rx_ts = time.time()
        except Exception:
            time.sleep(0.01)

# 메인 루프
def main():
    global prev_cmd, pending_cmd, pending_cnt
    global cur_left_dc, cur_right_dc

    print("Bluetooth 조이스틱 각도 기반 자동차 제어 시작")
    stop_motor()
    print("▶ 정지")

    try:
        while not stop_event.is_set():
            now = time.time()

            # 타임아웃 → 감속 정지
            if (now - last_rx_ts) > TIMEOUT_SEC:
                cur_left_dc  = ramp_to(cur_left_dc,  0.0, RAMP_STEP)
                cur_right_dc = ramp_to(cur_right_dc, 0.0, RAMP_STEP)
                set_dir_speed(cur_left_dc, cur_right_dc)
                if prev_cmd != "stop":
                    prev_cmd = "stop"
                time.sleep(LOOP_DT)
                continue

            # 최신 샘플
            with g_lock:
                ang = latest_angle
                pwr = latest_power
            if ang is None:
                time.sleep(LOOP_DT)
                continue

            # 데드존/섹터 판정
            wanted_cmd = "stop" if pwr < DEADZONE else which_sector(ang)

            # 섹터 안정화
            if wanted_cmd == pending_cmd:
                pending_cnt += 1
            else:
                pending_cmd = wanted_cmd
                pending_cnt = 1
            if pending_cnt >= SECTOR_STABLE_N and prev_cmd != pending_cmd:
                prev_cmd = pending_cmd

            # 램핑 적용
            tL, tR = targets_for_cmd(prev_cmd)
            cur_left_dc  = ramp_to(cur_left_dc,  tL, RAMP_STEP)
            cur_right_dc = ramp_to(cur_right_dc, tR, RAMP_STEP)
            set_dir_speed(cur_left_dc, cur_right_dc)

            time.sleep(LOOP_DT)

    except KeyboardInterrupt:
        pass
    finally:
        stop_motor()
        try:
            L_Motor.stop(); R_Motor.stop()
        except:
            pass
        try:
            bleSerial.flush()
        except:
            pass
        GPIO.cleanup()
        print("사용자 중단, 종료")

# 시작
if __name__ == '__main__':
    t = threading.Thread(target=serial_thread, daemon=True)
    t.start()
    try:
        main()
    finally:
        stop_event.set()
        try:
            t.join(timeout=1.0)
        except:
            pass
        try:
            bleSerial.close()
        except:
            pass
        print("프로그램 종료")
