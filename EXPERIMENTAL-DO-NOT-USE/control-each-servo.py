#!  /usr/bin/env  python

# Copyright 2016  Chris Lishka
#
# Please see LICENSE in top-level directory for licensing terms (Apache 2.0) 

import sys
import re
import time

from Adafruit_PWM_Servo_Driver import PWM



# Commands:
#
#  Q = quit
#
#  #+ = Increase servo position by 10, where # is a digit from 0 - 9
#  #- = Decrease servo position by 10, where # is a digit from 0 - 9
#
# e.g.  Command "2+" increases the servo 2 position by 10
#       Command "0-" decreases the servo 0 position by 10


# =============================================================================
# Initialization from z_Servo_Examply.py
# =============================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

global  servoMin, servoMax, k_PWM_ON

#ORIG servoMin = 150  # Min pulse length out of 4096
#ORIG servoMax = 600  # Max pulse length out of 4096
# servoMin = 250  # Min pulse length out of 4096
# servoMax = 550  # Max pulse length out of 4096
servoMin = 290  # Min pulse length out of 4096
servoMax = 320  # Max pulse length out of 4096
k_PWM_ON = 1    # Default is 0


# =============================================================================
# Globals
# =============================================================================

global  servoPos
servoPos = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

# Default servo position value is half-way between servoMin and servoMax
for c in range( 0, 10 ) :
  servoPos[ c ] = int( (servoMax - servoMin) / 2 ) + servoMin
  print 'Servo position for servo %d set to %d' % ( c, servoPos[ c ] )

# Override particular servos
# -- this DEPENDS ON HOW YOU ATTACHED THEM to the Servo Hat board!!!
servoPos[ 0 ] = 300
servoPos[ 1 ] = 300
servoPos[ 2 ] = 300
servoPos[ 3 ] = 300
servoPos[ 4 ] = 300
servoPos[ 5 ] = 300


# =============================================================================
# Main
# =============================================================================

# -----------------------------------------------------------------------------
def  main() :

  setAllServoPositions()

  mainLoop()

  sys.exit( 0 )  


# -----------------------------------------------------------------------------
# Original main() from z_Servo_Example.py
# It simply moves all servos back and forth in a loop
#
# This works in my testing with five small SG90 and one big MG996R servoes,
#   using a 5volt 10amp (!!!) power supply.
# One of the small servos is noisy (buzzes) in one position, but that may be
#   a characteristic of that one servo.
#
def  mainOrig() :

  pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

  while (True):

    # Change speed of continuous servo on channel O

    pwm.setAllPWM(0, servoMin)
    # pwm.setPWM(0, k_PWM_ON, servoMin)
    time.sleep(1)

    pwm.setAllPWM(0, servoMax)
    # pwm.setPWM(0, k_PWM_ON, servoMax)
    time.sleep(1)

  # End:  while (True)


# =============================================================================
# Functions
# =============================================================================

# -----------------------------------------------------------------------------
#
# Commands are of the form #+ or #-, where:
#
#    "#" is a servo from 0 through 9 that you want to change.
#      The number maps to the port that a servo is in
#
#    "+" means increase the servo position by 10
#
#    "-" means decrease the servo position by 10
#
def  mainLoop() :

  global  servoPos, servoMin, servoMax, k_PWM_ON

  print
  print 'servoMin value is %d' % servoMin
  print 'servoMax value is %d' % servoMax

  keepGoing = True
  while  keepGoing :

    print 'Current servo positions:'
    for  c in range( 0, len( servoPos ) ) :
      print '  Servo %d: %d' % ( c, servoPos[ c ] )

    print
    print 'cmd: ',
    line = sys.stdin.readline()
    cmd = line.strip()  # Remove leading and trailing white-space

    if  re.match( '^[0-9][+-=]', cmd ) :

      servo = int( cmd[0] )

      if  cmd[1] == '+' :    # Increase servo position

        servoPos[ servo ] += 10
        if servoPos[ servo ] >= servoMax :  servoPos[ servo ] = servoMax
        print 'Setting servo %d to %d' % ( servo, servoPos[ servo ] )
        setServoPosition( servo )

      elif  cmd[1] == '-' :  # Decrease servo position

        servoPos[ servo ] -= 10
        if servoPos[ servo ] <= servoMin :  servoPos[ servo ] = servoMin
        print 'Setting servo %d to %d' % ( servo, servoPos[ servo ] )
        setServoPosition( servo )

      elif  cmd[1] == '=' :  # Set servo position to a requested value

        servoPos[ servo ] = int( cmd[2:] )
        if servoPos[ servo ] <= servoMin :  servoPos[ servo ] = servoMin
        if servoPos[ servo ] >= servoMax :  servoPos[ servo ] = servoMax
        print 'Setting servo %d to %d' % ( servo, servoPos[ servo ] )
        setServoPosition( servo )

      else :  print '- Unrecognized operator [%s]' % cmd

    elif  cmd =='Q' :  keepGoing = False

    else :  '- Unrecognized command [%s]' % cmd
    

# -----------------------------------------------------------------------------
def  setServoPosition( servo ) :

  global  servoPos, k_PWM_ON

  pwm.setPWM( servo, k_PWM_ON, servoPos[ servo ] )


# -----------------------------------------------------------------------------
def  setAllServoPositions() :

  global  servoPos, k_PWM_ON

  for  s in range( 0, 10 ) :  setServoPosition( s )


# =============================================================================
if  __name__ == '__main__' :  main()
