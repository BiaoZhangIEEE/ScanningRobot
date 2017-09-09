#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2017, UFactory, Inc.
# All rights reserved.
#
# Author: Duke Fong <duke@ufactory.cc>


import sys, os
from time import sleep

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

#logger_init(logging.VERBOSE)
#logger_init(logging.DEBUG)
logger_init(logging.INFO)

print('setup swift ...')

#swift = SwiftAPI(dev_port = '/dev/ttyACM0')
#swift = SwiftAPI(filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = SwiftAPI(cmd_pend_size = 3) # default by filters: {'hwid': 'USB VID:PID=2341:0042'}

print('sleep 2 sec ...')
sleep(2)

print('moving!')

swift.set_position(150, 0, 250, speed = 10000, wait = True) # Home

# Discard
swift.set_position(250, 0, 250, speed = 10000, wait = True) # Above Scanner 
swift.set_pump(True)
swift.set_position(250, 0, 130, speed = 5000, wait = True) # Scanner 
swift.set_position(250, 0, 250, speed = 5000, wait = True) # Above Scanner 
swift.set_position(0, -217, 250, speed = 10000, wait = True) # Above Discard Stack
swift.set_pump(False)
sleep(0.5)
swift.set_position(20, -20, 50, speed = 10000, wait = True) # Tuck
swift.set_position(20, 20, 50, speed = 10000, wait = True) # Tuck

# Draw
swift.set_position(0, 217, 250, speed = 10000, wait = True) # Above Draw Stack
swift.set_pump(True)
# go down slowly 
height = 250;
while 1:
  swift.set_position(0, 217, height, speed = 5000, wait = True)
  if not swift.get_limit_switch():
    print('pressed')
    break
  else:
    if height > 5:
      height -= 1
    else:
      print('What?!?! No photo!')
      break

swift.set_position(0, 217, height+50, speed = 5000, wait = True) # Above Draw Stack
swift.set_position(0, 217, 250, speed = 5000, wait = True) # Above Draw Stack
swift.set_position(250, 0, 150, speed = 10000, wait = True) # Scanner 
sleep(0.5)
swift.set_pump(False);
swift.set_position(250, 0, 250, speed = 5000, wait = True) # Above Scanner 
swift.set_position(150, 0, 250, speed = 5000, wait = True) # Home

print('done ...')
