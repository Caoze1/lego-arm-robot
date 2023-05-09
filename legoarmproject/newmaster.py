#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction , SoundFile , Color
from pybricks.tools import wait

# Initialize the EV3 Brick
ev3 = EV3Brick()
ev3.speaker.beep()

elbow_positions = []
base_positions = []
colors = {}

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

def colorcheck(target = False):
    if target:
        elbow_motor.run_target(60, 45)
        elbow_motor.hold()
    wait(250)
    color_1 = elbow_sensor.rgb()
    print(elbow_sensor.color())
    print(elbow_sensor.rgb())
    color_1= get_color_name(color_1)
    print(color_1)
    ev3.speaker.beep()
    return color_1

def get_color_name(rgb_tuple):
    
    if rgb_tuple[0] < 4 and rgb_tuple[2] <= 7:
        ev3.speaker.say("green")
        ev3.screen.clear()
        ev3.screen.draw_text(50, 50, "green", text_color=Color.BLACK, background_color=None)
        return "green"
    if rgb_tuple[0] < 4 and rgb_tuple[2] > 7:
        ev3.speaker.say("blue")
        ev3.screen.clear()
        ev3.screen.draw_text(50, 50, "blue", text_color=Color.BLACK, background_color=None)
        return "blue"
    if rgb_tuple[0] >= 4 and rgb_tuple[1] >= 5:
        ev3.speaker.say("yellow")
        ev3.screen.clear()
        ev3.screen.draw_text(50, 50, "yellow", text_color=Color.BLACK, background_color=None)
        return "yellow"
    if rgb_tuple[0] >= 4 and rgb_tuple[1] < 5:
        ev3.speaker.say("red")
        ev3.screen.clear()
        ev3.screen.draw_text(50, 50, "red", text_color=Color.BLACK, background_color=None)
        return "red"

def pick_up(base_angle=-100, color=False):
    gripper_open()
    base_motor.run_target(40, base_positions[0])
    base_motor.hold()
    elbow_motor.run_target(40, elbow_positions[0])

    gripper_close()
    if color and gripper_motor.angle() <= -5 :
        color = colorcheck(target = True)
        
    print(gripper_motor.angle())

    reset_elbow()
    print(elbow_motor.angle())
    return (True, color)


def drop_off_position(block_color):
    for i in list(colors.keys()):
        if block_color == i:
            return colors.get(i)
    return 100

def drop_off(position):
    if gripper_motor.angle() >= -5:
        ev3.speaker.say('no block')
        wait(5000)
        return
    base_motor.run_target(40, position[1])
    base_motor.hold()
    elbow_motor.run_target(40, position[0])
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

ev3.buttons.pressed()
i = 0
while len(elbow_positions) < 3:
    try:
        if str(ev3.buttons.pressed()[0]) == "Button.UP":
            elbow_motor.run(15)
        elif str(ev3.buttons.pressed()[0]) == "Button.DOWN":
            elbow_motor.run(-15)
        elif str(ev3.buttons.pressed()[0]) == "Button.RIGHT":
            base_motor.run(-15)
        elif str(ev3.buttons.pressed()[0]) == "Button.LEFT":
            base_motor.run(15)
        elif str(ev3.buttons.pressed()[0]) == "Button.CENTER":
            elbow_positions.append(elbow_motor.angle())
            base_positions.append(base_motor.angle())
            wait(1500)
            reset_elbow()
            while True:
                if i == 0:
                    i += 1
                    break
                print("in color check")
                wait(100)
                try:
                    if str(ev3.buttons.pressed()[0]) == "Button.CENTER":
                        colors[colorcheck()] = (elbow_positions[i], base_positions[i])
                        wait(1500)
                    elif str(ev3.buttons.pressed()[0]) == "Button.RIGHT":
                        i += 1
                        break
                except:
                    print("No color")


    except:
        print("Nothng pressed")
        elbow_motor.hold()
        base_motor.hold()


    print(ev3.buttons.pressed(), colors)
    wait(100)


print(elbow_positions, base_positions)
while True:
    color = pick_up(color=True)[1]
    #wait(1000)
    drop_off(drop_off_position(color))