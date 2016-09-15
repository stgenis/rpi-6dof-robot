#!/usr/bin/python

# Copyright 2016  Chris Lishka
#
# Please see LICENSE in top-level directory for licensing terms (Apache 2.0) 

import sys
import time

from Adafruit_PWM_Servo_Driver import PWM

#
# Example code to use Adafruit library to move servo 0 back & forth a small amt
#
# I use this for testing: I start the code, then plug a servo into pins for
# servo 0.  All servos on my Sainsmart 6-Axis Robot Arm work safely between
# kServoLow and kServoHi, so this is a safe test for *my* robot.  YOURS MAY
# VARY!!!
#

kServoLow = 300  # Min pulse length out of 4096
kServoHi  = 310  # Max pulse length out of 4096
kPWM_ON = 1    # Default is 0


# =============================================================================
def  main() :

  pwm = PWM(0x40, debug=False)  # Instantiate Adafruit PWM object
  pwm.setPWMFreq( 60 )          # Set frequency to 60 Hz

  keepGoing = True
  while( keepGoing ):

    # Change speed of continuous servo on channel O
    pwm.setPWM(0, kPWM_ON, kServoLow)
    time.sleep(1)
    pwm.setPWM(0, kPWM_ON, kServoHi)
    time.sleep(1)

  # End:  while( keepGoing )

  sys.exit( 0 )  # Currently not reached


# =============================================================================
# Parameters:
#   currPos  The position to be moved *from* (which cannot be read from servo)
#   newPos   The position to be moved *to*
#   step     How much to move in each increment
#   pause    How much to delay (in seconds) between steps
#
def  moveIncrementally( currPos, newPos, step, pause ) :

  pass  # XXXXX NOT IMPLEMENTED YET XXXXX


# =============================================================================
if  __name__ == '__main__' :  main()
