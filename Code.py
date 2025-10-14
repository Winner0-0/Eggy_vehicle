from machine import Pin, PWM, UART
import time

# Defining UART channel and Baud Rate
uart = UART(0, 9600)

# Motor 1 - Driver 1 (Left Motor)
In1 = Pin(6, Pin.OUT)
In2 = Pin(7, Pin.OUT)

# Motor 2 - Driver 2 (Right Motor)
In3 = Pin(4, Pin.OUT)
In4 = Pin(3, Pin.OUT)

# PWM for motor speed control
EN_A = PWM(Pin(8))
EN_B = PWM(Pin(2))

# Frequency for enabling pins
EN_A.freq(1500)
EN_B.freq(1500)

# Claw control pins
In5 = Pin(17, Pin.OUT)
In6 = Pin(19, Pin.OUT)
In7 = Pin(16, Pin.OUT)
In8 = Pin(15, Pin.OUT)

# PWM for claw control speed
EN_C = PWM(Pin(20))
EN_D = PWM(Pin(14))

# Frequency for claw control pins
EN_C.freq(1500)
EN_D.freq(1500)

# Move Forward
def move_forward():
    In1.low()
    In2.high()
    In3.low()
    In4.high()

# Move Backward
def move_backward():
    In1.high()
    In2.low()
    In3.high()
    In4.low()

# Turn Left
def turn_left():
    In1.high()
    In2.low()
    In3.low()
    In4.high()

# Turn Right
def turn_right():
    In1.low()
    In2.high()
    In3.high()
    In4.low()

# Claw control functions
def claw_up():
    print("Claw going up")
    In5.high()
    In6.low()
    In7.low()
    In8.high()

def claw_down():
    print("Claw going down")
    In5.low()
    In6.high()
    In7.high()
    In8.low()

def claw_close():
    print("Claw closing")
    In5.low()
    In6.high()
    In7.low()
    In8.high()

def claw_open():
    print("Claw opening")
    In5.high()
    In6.low()
    In7.high()
    In8.low()

# Stop motors
def stop():
    In1.low()
    In2.low()
    In3.low()
    In4.low()


# Main loop: Checking UART commands
while True:
    if uart.any():  # Checking if data available
        data = uart.read().decode('utf-8')  # Get data and decode it as string
        print(f"Received data: {data}")

        # Handle different commands based on UART input
        if 'forward' in data:
            move_forward()
        elif 'backward' in data:
            move_backward()
        elif 'right' in data:
            turn_right()
        elif 'left' in data:
            turn_left()
        elif 'claw_up' in data:
            claw_up()
        elif 'claw_down' in data:
            claw_down()
        elif 'claw_close' in data:
            claw_close()
        elif 'claw_open' in data:
            claw_open()
        elif 'stop' in data:
            stop()
        elif('E' in data):
            speed=data.split("|")
            print(speed[1])
            set_speed = float(speed[1])/100 * 65025
            EN_A.duty_u16(int(set_speed)) #Setting Duty Cycle
            EN_B.duty_u16(int(set_speed)) #Setting Duty Cycle
            EN_C.duty_u16(int(set_speed)) #Setting Duty Cycle
            EN_D.duty_u16(int(set_speed)) #Setting Duty Cycle
        else:
            stop() #Stop
