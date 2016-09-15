# rpi-6dof-robot

Code for controlling a Sainsmart 6-DOF robot with a Raspberry Pi
controller and Adafruit servo hat.

This code is used to control a Sainsmart 6-Axis robot arm.  I
purchased mine from Amazon, at the following link:

https://www.amazon.com/SainSmart-Control-Palletizing-Arduino-MEGA2560/dp/B00UMOSQCI/ref=sr_1_fkmr1_2?ie=UTF8&qid=1473911632&sr=8-2-fkmr1&keywords=sainsmart+6dof+robot+arm

Make sure you choose the "6-Axis" arm (and not the "6-Axis DIY").

For electronics, I am using:

* Rasperry Pi 2 Model B board.  Later models may also work.

* Adafruit 16-Channel PWM Servo HAT for Raspberry Pi.  This board can control the PWM signals for many servos.  I need six for the arm, and eventually one additional servo for a gripper.

* A power supply that outputs 5 volts 10 amps.  This may be overkill in amperage, but experiments show that more than 2 amps are necessary and this does the job.  (It can be purchased on Adafruit, and the page for the above 16-Channel PWM Servo HAT has recommended power supplies.)

In addition, I am using an open-source python library from Adafruit to control the servo board.  [URL will be added later.]
