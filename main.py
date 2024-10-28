from machine import Pin, PWM
import time

fire_sensor_pin = Pin(15, Pin.IN)

motor_in1 = Pin(12, Pin.OUT)
motor_in2 = Pin(11, Pin.OUT)
motor_speed = PWM(Pin(13))
motor_speed.freq(1000)
slower_speed = 5000

servo = PWM(Pin(14))
servo.freq(50)
current_angle = 90

buzzer = PWM(Pin(16))
buzzer.freq(2000)


def set_servo_angle(angle):
    duty = 500 + int((angle / 180) * 2000)
    servo.duty_u16(int(duty * 65535 / 20000))


def smooth_servo_move(target_angle, delay=0.03):
    global current_angle
    if current_angle < target_angle:
        for angle in range(current_angle, target_angle + 1, 1):
            set_servo_angle(angle)
            current_angle = angle
            time.sleep(delay)
    elif current_angle > target_angle:
        for angle in range(current_angle, target_angle - 1, -1):
            set_servo_angle(angle)
            current_angle = angle
            time.sleep(delay)


smooth_servo_move(90)


def move_forward(speed=slower_speed):
    motor_in1.on()
    motor_in2.off()
    motor_speed.duty_u16(speed)


def stop_motor():
    motor_in1.off()
    motor_in2.off()
    motor_speed.duty_u16(0)


def start_buzzer():
    buzzer.duty_u16(50000)


def stop_buzzer():
    buzzer.duty_u16(0)


while True:
    if fire_sensor_pin.value() == 1:
        print("Fire Detected!")

        move_forward()

        start_buzzer()

        fire_direction = "left"

        if fire_direction == "left":
            smooth_servo_move(75)
        elif fire_direction == "right":
            smooth_servo_move(105)
        else:
            smooth_servo_move(90)

    else:
        print("No Fire Detected.")
        stop_motor()
        stop_buzzer()
        smooth_servo_move(90)

    time.sleep(1)
