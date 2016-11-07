#!/usr/bin/env python
##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import sys
from EasySnmpPlugin import EasySnmpPlugin

haStateOID = '.1.3.6.1.4.1.2620.1.5.6.0'

exitStatus = 0

class CheckPointHaStatePlugin(EasySnmpPlugin):
    """
    Checks a Check Point firewall using SNMP to verify that HA is in a proper
    state.
    """
    
    oids = [haStateOID,]
    
    def onSuccess(self, result):
        state = str(result[haStateOID]).lower()
        global exitStatus
        if state is None:
            print "no HA state returned"
            exitStatus = 1
        elif state == "active":
            print "HA is active"
        elif state == "not active":
            print "HA is not active"
            exitStatus = 1
        elif state in ("standby", "stand-by"):
            print "HA is in stand-by"
        else:
            print "unknown HA state"
            exitStatus = 1
        
    def onError(self, result):
        print "error getting HA state"
        global exitStatus
        exitStatus = 1


if __name__ == "__main__":
    cmd = CheckPointHaStatePlugin()
    cmd.run()
    sys.exit(exitStatus)
