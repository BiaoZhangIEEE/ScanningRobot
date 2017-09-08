#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2017, UFactory, Inc.
# All rights reserved.
#
# Author: Duke Fong <duke@ufactory.cc>


import sys, os
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

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

swift.set_position(0, 217, 250, speed = 5000, wait = True)
# go down slowly 
swift.set_pump(True)
height = 100;
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

swift.set_position(0, 217, 250, speed = 5000, wait = True)
swift.set_position(250, 0, 150, speed = 10000, wait = True) 
sleep(0.5)
swift.set_pump(False);
swift.set_position(150, 0, 150, speed = 5000, wait = True)

swift.set_buzzer()

print('done ...')
