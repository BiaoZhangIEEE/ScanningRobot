#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2017, UFactory, Inc.
# All rights reserved.
#
# Author: Duke Fong <duke@ufactory.cc>

from time import sleep
from ..utils.log import *


class Pump():
    def __init__(self, ufc, node, iomap):
        
        self.ports = {
            'service': {'dir': 'in', 'type': 'service', 'callback': self.service_cb},
            'limit_switch': {'dir': 'out', 'type': 'topic'},
            
            'cmd_sync': {'dir': 'out', 'type': 'service'},
            'report': {'dir': 'in', 'type': 'topic', 'callback': self.report_cb}
        }
        
        self.logger = logging.getLogger(node)
        ufc.node_init(node, self.ports, iomap)
    
    def set_pump(self, val, timeout = 0):
        if val == 'on':
            self.ports['cmd_sync']['handle'].call('M2231 V1')
        else:
            self.ports['cmd_sync']['handle'].call('M2231 V0')
        
        # TODO: modify the default timeout time with a service command
        if(timeout == 0):
          return 'ok'
        ret = None
        for _ in range(timeout*2):
            ret = self.ports['cmd_sync']['handle'].call('P2231')
            if val == 'on':
                if ret == 'ok V2': # grabbed
                    return 'ok'
            else:
                if ret == 'ok V0': # stop
                    return 'ok'
            sleep(0.5)
        return 'err, timeout for {}, last ret: {}'.format(val, ret)
    
    def report_cb(self, msg):
        if not self.ports['limit_switch']['handle']:
            return
        if msg == '6 N0 V0':
            self.ports['limit_switch']['handle'].publish('off')
        elif msg == '6 N0 V1':
            self.ports['limit_switch']['handle'].publish('on')
    
    def service_cb(self, msg):
        words = msg.split(' ', 1)
        action = words[0]
        
        words = words[1].split(' ', 1)
        param = words[0]
        
        if param == 'value':
            if action == 'get':
                ret = self.ports['cmd_sync']['handle'].call('P2231')
                self.logger.debug('get value ret: %s' % ret)
                
                if ret == 'ok V0':
                    return 'ok, stoped'
                elif ret == 'ok V1':
                    return 'ok, working'
                elif ret == 'ok V2':
                    return 'ok, grabbed'
                else:
                    return 'err, unkown ret: %s' % ret
            
            if action == 'set':
                self.logger.debug('set value: %s' % words[1])
                return self.set_pump(words[1])
        
        elif param == 'limit_switch':
            if action == 'get':
                ret = self.ports['cmd_sync']['handle'].call('P2233')
                self.logger.debug('get limit_switch ret: %s' % ret)
                
                if ret == 'ok V0':
                    return 'ok, off'
                elif ret == 'ok V1':
                    return 'ok, on'
                else:
                    return 'err, unkown ret: %s' % ret

