# PA1473 - Software Development: Agile Project

## Introduction
Our project is called lego robot arm and is made with python and an lego ev3 device. The robot can pick up a big lego block, determine it's color and place it at designated drop off location.


## Getting started

This section is supposed to guide a new developer through the steps of how to set up the project and install the deppendencies they need to start developing.

To get started using the lego robot an IDE compatible with pybricks and ev3 is needed if you wish to modify the code. Visual studio code with ev3dev-browser extension and lego mindstorm extension was used in the making of this code.
Below are all dependencies for the robot:

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction , SoundFile , Color
from pybricks.tools import wait

It is possible to copy the above lines of code into your project to get started.


## Building and running

The core functionallity of our program is built on the gripper functions as well as drop off, pick up and color check functions. These lay the foundation for all the base operations the robot can execute. 

Starting the robot will first trigger its calibration state. This is done to get consistent movement throughout different robots. The calibration mainly calibrates the elbow position. 

After the calibration state is done the robot will reset its arm to its defult state and be ready to set up drop off and pick up locations. This is done by manual input. The setup follows a sequence where the first calibrated location will always be the pick up zone. The lego arm is moved through pushing the buttons on the ev3 device. Each direction corresponds to a direction the arm will move. To confirm the location of either pick up or drop off zone press the button in the middle of the ev3 device. After calibrating the pick up zone the robot will reset its arm once again and be ready to calibrate its drop off zones.

The robot will enter a new state after a zone for drop off has been entered. The robot will reset its arm once again as usual but after entering a drop off zone it will always change state to a color calibration state. In this state it is decided which colors should be dropped off at the prior decided position. Any number of colors can be scanned at this time. The scanning is done by holding a lego block in front of the robot's color sensor and pressing the middle button on the ev3 device. To exit the color calibration state, press the right most button on the ev3 device. This will return the robot to it's prior state and you can once again move the robot with the directional buttons on the ev3 device. One pick up location and two drop off locations can be calibrated for this robot. The robot will enter its working state after the second drop off location is completed. 


## Features

- [x] US01: Pick up items.
- [x] US01B: Pick up items from a designated position.
- [x] US02: Drop off items.
- [x] US02B: Drop items off at a designated position.
- [x] US03: Determine if an item is present at a given location.
- [x] US04B: Robot to tell me the color of an item at a designated position.
- [x] US05: Drop items off at different locations based on the color of the item.
- [x] US06: Be able to pick up items from elevated positions.
- [x] US08B As a customer, I want to be able to calibrate items with three different colors and drop the items
off at specific drop-off zones based on color.
- [x] US09: As a customer, I want the robot to check the pickup location periodically to see if a new item has
arrived. 
- [ ] US10: As a customer, I want the robots to sort items at a specific time. 
- [ ] US11: As a customer, I want two robots to communicate and work together on items sorting without colliding with each other. 
- [x] US12: As a customer, I want to be able to manually set the locations and heights of one pick-up zone and two drop-off zones. (Implemented either by manually dragging the arm to a position or using buttons).
