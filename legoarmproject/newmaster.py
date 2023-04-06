#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

# Initialize the EV3 Brick
ev3 = EV3Brick()
ev3.speaker.beep()

#Defining angle limits
GROUND_ANGLE = -117
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

# Initialize the elbow. First make it go down for one second.
# Then make it go upwards slowly (15 degrees per second) until
# the Color Sensor detects the white beam. Then reset the motor
# angle to make this the zero point. Finally, hold the motor
# in place so it does not move.
#elbow_motor.run_time(-30, 1000)
#elbow_motor.run(15)
#while elbow_sensor.reflection() < 32:
#    wait(10)
#elbow_motor.reset_angle(0)
#elbow_motor.hold()


# Initialize the base. First rotate it until the Touch Sensor
# in the base is pressed. Reset the motor angle to make this
# the zero point. Then hold the motor in place so it does not move.
#base_motor.run(-60)
#while not base_switch.pressed():
#    wait(10)
#base_motor.reset_angle(0)
#base_motor.hold()

# Initialize the gripper. First rotate the motor until it stalls.
# Stalling means that it cannot move any further. This position
# corresponds to the closed position. Then rotate the motor
# by 90 degrees such that the gripper is open.
#gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
#gripper_motor.reset_angle(0)
#gripper_motor.run_target(200, -90)


def downward_stall_angle():
    elbow_motor.run_until_stalled(-70, then=Stop.COAST, duty_limit=10)

    return elbow_motor.angle()

def claw_open():
    gripper_motor.run_target(200, -90)
    gripper_motor.hold()

def claw_close():
    gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    gripper_motor.hold()

def reset_elbow():
    elbow_motor.run_target(60, -30)
    elbow_motor.hold()

def reset_base():
    base_motor.run_target(40, 0)
    base_motor.hold()

def pick_up(base_angle=0):
    base_motor.run_target(40, base_angle)
    base_motor.hold()
    if downward_stall_angle() <= GROUND_ANGLE + 2:
        reset_elbow()
        print(False)
        return False
    else:
        elbow_motor.run_angle(60, 50)
        claw_open()
        elbow_motor.run_angle(60, -40)
        claw_close()
        reset_elbow()
        print(True)
        return True

def drop_off(base_angle=0):
    base_motor.run_target(40, base_angle)
    base_motor.hold()
    downward_stall_angle()
    claw_open()
    reset_elbow()
    claw_close()
    


# Play three beeps to indicate that the initialization is complete.
for i in range(3):
    ev3.speaker.beep()
    wait(100)

#Calibrating start position for elbow
elbow_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=30)
elbow_motor.hold()
elbow_motor.reset_angle(0)
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

#base_motor.run(-60)
#while not base_switch.pressed(): 
#    wait(100)
#print(base_motor.angle())
#base_motor.hold()
#wait(1000)
#base_motor.run_until_stalled(60, then=Stop.COAST, duty_limit=20)
#print(base_motor.angle())

#Calibrating start position of claw
gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.hold()

while not pick_up(-95):
    print("Nothing to pickup")

wait(1000)

drop_off(80)
reset_base()