#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction , SoundFile , Color
from pybricks.tools import wait

# Initialize the EV3 Brick
ev3 = EV3Brick()
ev3.speaker.beep()

#Defining angle limits
MAX_RIGHT_ANGLE = -110
MAX_LEFT_ANGLE = 110
gripper_motor = Motor(Port.A)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it. We would like positive speed values to make the
# arm go upward. This corresponds to counterclockwise rotation
# of the motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base. It has a 12-teeth and a
# 36-teeth gear connected to it. We would like positive speed values
# to make the arm go away from the Touch Sensor. This corresponds
# to counterclockwise rotation of the motor.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limit the elbow and base accelerations. This results in
# very smooth motion. Like an industrial robot.
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the elbow
# is in the starting position. This is when the sensor sees the
# white beam up close.
elbow_sensor = ColorSensor(Port.S2)

def elbow_stall():
    elbow_motor.run(-30)
    wait(1000)
    elbow_motor.stop()
    while elbow_motor.speed() < 0:
        print(elbow_motor.speed(), elbow_motor.stalled())
    
    print(elbow_motor.speed(), elbow_motor.stalled())
    elbow_motor.hold()
    return elbow_motor.angle()


def downward_stall_angle():
    elbow_motor.run_until_stalled(-20, then=Stop.HOLD, duty_limit=10)

    return elbow_motor.angle()

def gripper_open():
    gripper_motor.run_target(200, -90)
    gripper_motor.hold()

def gripper_close():
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    gripper_motor.hold()
    return gripper_motor.angle()

def reset_elbow():
    elbow_motor.run_target(60, 90)
    elbow_motor.hold()

def reset_base():
    base_motor.run_target(40, 0)
    base_motor.hold()

def colorcheck():
    elbow_motor.run_angle(60, 30)
    elbow_motor.hold()
    wait(250)
    color_1 = str(elbow_sensor.color())
    print(elbow_sensor.color())
    ev3.speaker.beep()
    wait(500)
    return color_1

def pick_up(base_angle=-100, color=False):
    gripper_open()
    base_motor.run_target(40, base_angle)
    base_motor.hold()
    downward_stall_angle()
    elbow_motor.run_angle(60, 17)

    gripper_close()
    if color and gripper_motor.angle() <= -5 :
        print("HEJ")
        color = colorcheck()
    print(gripper_motor.angle())

    reset_elbow()
    print(elbow_motor.angle())
    return (True, color)

def drop_off_position(block_color):
    drop_off_1 = 0
    drop_off_2 = 55
    drop_off_3 = 100
    if block_color == "Color.BLUE":
        ev3.speaker.say('blue')
        return 55

    elif block_color == "Color.GREEN":
        ev3.speaker.say('green')
        return 100

    elif block_color == "Color.YELLOW":
        ev3.speaker.say('yellow')
        return 0

    elif block_color == "Color.RED":
        ev3.speaker.say('red')
        return 55

    elif block_color == "Color.BLACK":
        ev3.speaker.say('black')
        return 0

    elif block_color == "Color.WHITE":
        ev3.speaker.say('white')
        return 100

    elif block_color == "Color.BROWN":
        ev3.speaker.say('brown')
        return 0
    return -100

def drop_off(base_angle=0):
    if gripper_motor.angle() >= -5:
        print(gripper_motor.angle())
        return
    print(gripper_motor.angle())
    base_motor.run_target(40, base_angle)
    base_motor.hold()
    downward_stall_angle()
    gripper_open()
    reset_elbow()
    gripper_close()
    


# Play three beeps to indicate that the initialization is complete.
for i in range(3):
    ev3.speaker.beep()
    wait(100)

#Calibrating start position for elbow
downward_stall_angle()
elbow_motor.hold()
elbow_motor.reset_angle(0)
GROUND_ANGLE = elbow_motor.angle()
elbow_motor.run_angle(60, 100)
wait(100)


#Calibrating start position for base
base_motor.run(-60)
while not base_switch.pressed(): 
    wait(100)
base_motor.hold()
wait(100)
base_motor.run_angle(40, 115)
base_motor.reset_angle(0)
wait(100)

#Calibrating start position of gripper
gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.hold()



while True:
    color = pick_up(color=True)[1]
    wait(1000)
    drop_off(drop_off_position(color))