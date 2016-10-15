#!  /usr/bin/env  python

# Copyright 2016  Chris Lishka
#
# Please see LICENSE in top-level directory for licensing terms (Apache 2.0) 

# Designed to be run on a Raspberry Pi with an Adafruit servo controller hat
#
# Please be sure to set PYTHONPATH to the location of the
# Adafruit_PWM_Server_driver library before running.

import sys
import os
import re
import json
import time

from Adafruit_PWM_Servo_Driver import PWM


# =============================================================================
# Constants
# =============================================================================

kDefaultMin = 290.0
kDefaultPos = 300.0
kDefaultMax = 310.0

kPwmOn = 1


# =============================================================================
# Main
# =============================================================================

def  main() :

  robot = ServoRobot()
  robot.loadFromJsonFile()

  print str( robot )

  print
  robot.dumpState()

  sys.exit( 0 )


# =============================================================================
# Classes
# =============================================================================

# =============================================================================
class  JointPose( object ) :

  # ---------------------------------------------------------------------------
  def  __init__( s, j0, j1, j2, j3, j4, j5, j6 ) :

    s._pos = []

    s._pos[ 0 ] = j0  # Base joint
    s._pos[ 1 ] = j1  # Angle from base
    s._pos[ 2 ] = j2  # Angle of parallelogram

    s._pos[ 3 ] = j3  # Rotation of forearm
    s._pos[ 4 ] = j4  # Angle of hand from forearm
    s._pos[ 5 ] = j5  # Rotation of wrist (gripper)
    
    s._pos[ 6 ] = j6  # Position of gripper


# =============================================================================
class  ServoJoint( object ) :

  # ---------------------------------------------------------------------------
  def  __init__( s, robotJoint=None ) :

    global  kDefaultMin, kDefaultPos, kDefaultMax

    s._jNum  = robotJoint

    if  s._jNum == None  or  s._jNum < 0  or  s._jNum > 6 :
      raise  Exception(  'ServoJoint: illegal robot joint number [%s]' %
                         str( robotJoint )  )

    s._pos = float( kDefaultPos )

    s._min = float( kDefaultMin )
    s._max = float( kDefaultMax )


  # ---------------------------------------------------------------------------
  def  __str__( s ) :

    return 'Servo( pos=%.2f, min=%.2f, max=%.2f )' % ( s._pos, s._min, s._max )
                                

  # ---------------------------------------------------------------------------
  def  get( s ) :       return  float( s._pos )
  def  set( s, val ) :  s._pos = float( val )


  # ---------------------------------------------------------------------------
  def  getMin( s ) :       return  float( s._min )
  def  setMin( s, val ) :  s._min = float( val )


  # ---------------------------------------------------------------------------
  def  getMax( s ) :       return  float( s._max )
  def  setMax( s, val ) :  s._max = float( val )


  # ---------------------------------------------------------------------------
  # Update the joint on the robot to its current value in s._pos, checking
  # against s._min and s._max first
  #
  def  update( s, pwm=None ) :

    global  kPwmOn

    if  s._pos < s._min :
      print 'ERROR: %s position is lower than minimum -- fixing'
      s._pos = s._min

    if  s._pos > s._max :
      print 'ERROR: %s position is greater than maximum -- fixing'
      s._pos = s._max

    # Update robot joint  XXXXX May want to round s._pos, instead of truncating
    pwm.setPWM( s._jNum, kPwmOn, int( s._pos ) )


# =============================================================================
class  ServoRobot( object ) :

  # ---------------------------------------------------------------------------
  def  __init__( s ) :

    s._joints = [ ServoJoint( 0 ), ServoJoint( 1 ), ServoJoint( 2 ),
                  ServoJoint( 3 ), ServoJoint( 4 ), ServoJoint( 5 ),
                  ServoJoint( 6 ) ]

    s._pwm = None

    s._initPwmLibrary()


  # ---------------------------------------------------------------------------
  def  __str__( s ) :

    j = s._joints

    return(  ( 'ServoRobot( 0=%.2f, 1=%.2f, 2=%.2f, ' +
               '3=%.2f, 4=%.2f, 5=%.2f, 6=%.2f )' ) %
             ( j[0].get(), j[1].get(), j[2].get(),
               j[3].get(), j[4].get(), j[5].get(), j[6].get() )  )


  # ---------------------------------------------------------------------------
  def  dumpState( s ) :

    print 'ServoRobot:'

    for jn in range( 0, 6 ) :  # Joints 0 through 5

      j = s._joints[ jn ]
      print(  '  Joint %d  Min %.2f  Pos %.2f  Max %.2f' %
              ( jn, j.getMin(), j.get(), j.getMax() )  )


  # ---------------------------------------------------------------------------
  # Updates a single joint on the robot to match current position from
  # corresponding Servo in s._joints
  #
  def  updateJoint( s, jointNum ) :  s._joints[ jointNum ].update( s._pwm )


  # ---------------------------------------------------------------------------
  # Updates robot to match current position of all joints from s._joints
  # 
  def  updateAllJoints( s ) :

    for jn in range( 0, 7 ) :  s.updateJoint( jn )  # Joints 0 through 6


  # ---------------------------------------------------------------------------
  def  getJoint( s, jNum ) :  return  s._joints[ jNum ].get()


  # ---------------------------------------------------------------------------
  def  setJoint( s, jNum, val ) :  s._joints[ jNum ].set( val )


  # ---------------------------------------------------------------------------
  def  loadFromJsonFile( s, fileName='./servo-settings.json' ) :

    # First load the file

    if  not os.path.isfile( fileName ) :
      print 'Could not find JSON file to load with name %s' % fileName
      return

    try :

      fIn = open( fileName, 'r' )
      jsonData = json.load( fIn )

      lastSrv  = jsonData[ 'lastSrv' ]
      gInc     = jsonData[ 'gInc'    ]
      srvCur   = jsonData[ 'srvCur'  ]
      srvMin   = jsonData[ 'srvMin'  ]
      srvMax   = jsonData[ 'srvMax'  ]

    except  Exception as e :

      print 'Unable to load from JSON file due to exception: %s' % str( e )
      return

    finally :  fIn.close()

    # Then set up the servo values

    for sn in range( 0, 7 ) :  # Load servos 0 through 6

      j = s._joints[ sn ]

      j.set( srvCur[ sn ] )
      
      j.setMin( srvMin[ sn ] )
      j.setMax( srvMax[ sn ] )


  # ---------------------------------------------------------------------------
  def  _initPwmLibrary( s ) :

    s._pwm = PWM( 0x40 )  # Use PRM( 0x40, debug=True ) for debug output

    s._pwm.setPWMFreq( 60 )  # Set frequency to 60 Hertz


# =============================================================================
if  __name__ == '__main__' :  main()
