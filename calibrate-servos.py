#!  /usr/bin/env  python

# Copyright 2016  Chris Lishka
#
# Please see LICENSE in top-level directory for licensing terms (Apache 2.0) 

import sys
import os
import re
import json
import time

from Adafruit_PWM_Servo_Driver import PWM


# Note: I've kept the Python code in this program straight-forward, just
#       globals and functions, so it is easy to understand by folks who
#       are not familiar with the language.

# Commands:
#
#  Servo positions are limited between servoMin and servoMax for each servo
#  gInc by default is 10
#
#  Q     Quit
#
#  #+    Increase servo position by gInc, where # is a digit from 0 - 9
#  #-    Decrease servo position by gInc, where # is a digit from 0 - 9
#
#  #=##  Set servo to exact position (checked against servoMin and servoMax)
#        where # is a digi from 0-9
#  
#  #>##  Set servo max to exact value.  BE CAREFUL with setting too high of
#        a max value -- THIS CAN DAMAGE YOUR SERVOS!!!
#
#  #<##  Set servo min to exact value.  BE CAREFUL with setting too low of
#        a min value -- THIS CAN DAMAGE YOUR SERVOS!!!
#
#  i+#   Increase gInc value by #
#  i-#   Decrease gInc value by #
#
#  X=#   Set the final servo to control (counting from 0).  Note that this
#        effects both the servo value display AND which servos are set.  All
#        10 servos are still saved to the settings file, though.
#
#  D     Restore servo position, min, and max values to defaults
#
#  s  S  Save settings out to a JSON file "servo-settings.json"
#  l  L  Load settings from a JSON file "servo-settings.json"
#
# e.g.  Command "2+" increases the servo 2 position by 10
#       Command "0-" decreases the servo 0 position by 10
#       Command "4=290" sets the server 4 position exactly to 290


# =============================================================================
# Constants
# =============================================================================

global  k_servoJsonFilename
k_servoJsonFilename = 'servo-settings.json'

global  k_PWM_ON

k_PWM_ON = 1    # Default is 1


# =============================================================================
# Globals
# =============================================================================

# Initialise the PWM device using the default address (from Servo_Example.py)
# Use pwm = PWM(0x40, debug=True) for debug output
pwm = PWM(0x40)

gInc = 10       # Default servo increment / decrement is 10

# These arrays are fully populated in restoreServoDefaults(), called in main()
srvMin = [ ]
srvMax = [ ]
srvCur = [ ]

lastSrv = 9


# =============================================================================
# Main
# =============================================================================

def  main() :

  global  k_servoJsonFilename

  # Initialize pwm object
  pwm.setPWMFreq( 60 )  # Set frequecy to 60 Hertz

  restoreServoDefaults()

  if  os.path.isfile( k_servoJsonFilename ) :
    loadServoJSON( k_servoJsonFilename )

  setAllServoPositions()

  mainLoop()

  sys.exit( 0 )  


# =============================================================================
# Functions
# =============================================================================

# -----------------------------------------------------------------------------
def  mainLoop() :

  global  srvCur, srvMin, srvMax, lastSrv, gInc, k_PWM_ON

  print

  keepGoing = True
  while  keepGoing :

    print
    print 'Increment value is currently: %d' % gInc
    print 'Last servo is currently: %d' % lastSrv
    print 'Servo values:'
    for  c in range( 0, lastSrv + 1 ) :
      print(  '  Servo %d:  Min %d  Cur %d  Max %d'
              % ( c, srvMin[ c ], srvCur[ c ], srvMax[ c ] )  )

    print
    print 'Command: ',
    line = sys.stdin.readline()

    cmd = line.strip()  # Remove leading and trailing white-space
    keepGoing = parseCommand( cmd )
    
  # End:  while keepGoing


# -----------------------------------------------------------------------------
# Parses a single command and acts on it.  See comments at top of file for
# command descriptions.
#
# Returns True if a non-Quit command, False if a Quit command
#
# The cmd parameter should have all white-space stripped off beginning and end
#
def  parseCommand( cmd ) :

  global  srvCur, srvMin, srvMax, lastSrv, gInc, k_servoJsonFilename

  if  re.match( '^[0-9][+-=<>]', cmd ) :  # -----------------------------------

    servo = int( cmd[0] )

    if  cmd[1] == '+' :    # Increase servo position

      srvCur[ servo ] += gInc
      checkServoBounds( servo )
      print 'Setting servo %d to %d' % ( servo, srvCur[ servo ] )
      setServoPosition( servo )

    elif  cmd[1] == '-' :  # Decrease servo position

      srvCur[ servo ] -= gInc
      checkServoBounds( servo )
      print 'Setting servo %d to %d' % ( servo, srvCur[ servo ] )
      setServoPosition( servo )

    elif  cmd[1] == '=' :  # Set servo position to a requested value

      srvCur[ servo ] = int( cmd[2:] )
      checkServoBounds( servo )
      print 'Setting servo %d to %d' % ( servo, srvCur[ servo ] )
      setServoPosition( servo )

    elif  cmd[1] == '<' :  # Set servo min to a requested value

      srvMin[ servo ] = int( cmd[2:] )
      print 'Set servo min value to %d' % srvMin[ servo ]

    elif  cmd[1] == '>' :  # Set servo max to a requested value

      srvMax[ servo ] = int( cmd[2:] )
      print 'Set servo max value to %d' % srvMax[ servo ]

    else :  print '- Unrecognized operator [%s]' % cmd

  elif  cmd[0] == 'i' :  # ----------------------------------------------------

    if  len( cmd ) < 2 :
      print 'Invalid command for changing incremewnt'
      return  True

    direction  = cmd[1]
    value      = 1

    if  len( cmd ) > 2 :  value = int( cmd[2:] )

    if    direction == '-' :
      gInc -= value
      print 'Increment decreased to %d' % gInc

    elif  direction == '+' :
      gInc += value
      print 'Increment increased to %d' % gInc

    else :  print 'Increment irection must be "+" or "-"'

  elif  cmd == 'l'  or  cmd == 'L' :  # ---------------------------------------

    loadServoJSON( k_servoJsonFilename )
    print 'Servo values loaded from file %s' % k_servoJsonFilename

  elif  cmd == 's'  or  cmd == 'S' :  # ---------------------------------------

    saveServoJSON( k_servoJsonFilename )
    print 'Servo values saved to file %s' % k_servoJsonFilename

  elif  cmd[ 0 ] == 'X' :  # --------------------------------------------------

    if  len( cmd ) < 3 :
      print 'Not enough information to set the last servo'

    elif  cmd[1] != '=' :
      print 'Incorrect syntax for setting the last servo'

    else :

      value = int( cmd[ 2: ] )

      lastSrv = value
      print(  'Last servo set to %d.  Servo range is now 0 through %d'
              % ( lastSrv, lastSrv )  )

  elif  cmd == 'D' :  # -------------------------------------------------------

    restoreServoDefaults()    
    print 'Servo values restored to default values'

  elif  cmd == 'Q' :  # -------------------------------------------------------

    return  False

  else :  print 'Unrecognized command [%s]' % cmd  # --------------------------

  return  True


# -----------------------------------------------------------------------------
def  checkServoBounds( srvNum ) :

  global  srvCur, srvMin, srvMax

  if srvCur[ srvNum ] <= srvMin[ srvNum ] : srvCur[ srvNum ] = srvMin[ srvNum ]
  if srvCur[ srvNum ] >= srvMax[ srvNum ] : srvCur[ srvNum ] = srvMax[ srvNum ]


# -----------------------------------------------------------------------------
def  setServoPosition( srvNum ) :

  global  pwm, srvCur, k_PWM_ON

  pwm.setPWM( srvNum, k_PWM_ON, srvCur[ srvNum ] )
  print 'DBG  Set servo %d to value %d' % ( srvNum, srvCur[ srvNum ] )


# -----------------------------------------------------------------------------
def  setAllServoPositions() :

  global  lastSrv

  for s in range( 0, lastSrv + 1 ) :  setServoPosition( s )


# -----------------------------------------------------------------------------
def  loadServoJSON( fileName ) :

  global  srvCur, srvMin, srvMax, lastSrv, gInc

  if  not os.path.isfile( fileName ) :
    print 'Could not find JSON file to load with name %' % fileName
    return

  try :

    fIn = open( fileName, 'r' )
    jsonData = json.load( fIn )

    origLst = lastSrv
    origInc = gInc
    origCur = srvCur
    origMin = srvMin
    origMax = srvMax

    lastSrv  = jsonData[ 'lastSrv' ]
    gInc     = jsonData[ 'gInc'    ]
    srvCur   = jsonData[ 'srvCur'  ]
    srvMin   = jsonData[ 'srvMin'  ]
    srvMax   = jsonData[ 'srvMax'  ]

  except  Exception as e :

    print 'Unable to load from JSON file due to exception: %s' % str( e )

    srvCur   = origCur  # Restore to original values, so we do not leave any
    srvMin   = origMin  # of these arrays in an inconsistent state (i.e. some
    srvMax   = origMax  # loaded, some not)
    lastSrv  = origLst
    gInc     = origInc

  finally :  fIn.close()


# -----------------------------------------------------------------------------
def  saveServoJSON( fileName ) :

  global  srvCur, srvMin, srvMax, lastSrv, gInc

  try :

    data = { 'lastSrv':lastSrv, 'gInc':gInc,
             'srvCur':srvCur, 'srvMin':srvMin, 'srvMax':srvMax }

    fOut = open( fileName, 'w' )
    json.dump( data, fOut )

  except  Exception as e :

    print 'Unable to save JSON file due to exception: %s' % str( e )

  finally :

    fOut.close()

# -----------------------------------------------------------------------------
def  restoreServoDefaults() :

  global  srvCur, srvMin, srvMax

  srvMin = [ 280, 280, 280, 280, 280,  280, 280, 280, 280, 280 ]
  srvMax = [ 300, 300, 300, 300, 300,  300, 300, 300, 300, 300 ]

  srvCur = [ 290, 290, 290, 290, 290,  290, 290, 290, 290, 290 ]


# =============================================================================
if  __name__ == '__main__' :  main()
