# rpi-6dof-robot

Code for controlling a Sainsmart 6-DOF robot with a Raspberry Pi
controller and Adafruit servo hat.

***
*** PLEASE NOTE: This is currently PRELIMINARY code, and must be tuned for your robot!
***

NOTE: each servo used in the robot has a finite range that depends on the mechanics of the robot, and what position the servo was in when installed in the physical robot.  YOU WILL NEED TO TUNE YOUR SERVO RANGE in the code that controls robot arm.  I am doing this manually right now (trial and error), but I will come up with a method in the future.


This code is used to control a Sainsmart 6-Axis robot arm.  I
purchased mine from Amazon, at the following link:

https://www.amazon.com/SainSmart-Control-Palletizing-Arduino-MEGA2560/dp/B00UMOSQCI/ref=sr_1_fkmr1_2?ie=UTF8&qid=1473911632&sr=8-2-fkmr1&keywords=sainsmart+6dof+robot+arm

Make sure you choose the "6-Axis" arm (and not the "6-Axis DIY").

For electronics, I am using:

* Rasperry Pi 2 Model B board.  Later models may also work.

* Adafruit 16-Channel PWM Servo HAT for Raspberry Pi.  This board can control the PWM signals for many servos.  I need six for the arm, and eventually one additional servo for a gripper.

* A power supply that outputs 5 volts 10 amps.  This may be overkill in amperage, but experiments show that more than 2 amps are necessary and this does the job.  (It can be purchased on Adafruit, and the page for the above 16-Channel PWM Servo HAT has recommended power supplies.)

* It is a good idea to purchase some spare MG996R and SG90 servos, in case you burn any out in your robotic arm.  These are inexpensive, widely used in the RC community, and can be found on Amazon.  In addition, you can hook these up first to the Servo Hat board and test them, before hooking up your robot arm.

In addition, I am using an open-source python library from Adafruit to control the servo board.  The library can be found at the following URL, in the directory "Adafruit_PWM_Servo_Driver":
https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

You will need to set PYTHONPATH to include the directory where Adafruit python library resides.  For example:

$  export PYTHONPATH='---Your-Path---/adafruit-library/Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver'

Cheers,
  ChrisL (aka stgenis)