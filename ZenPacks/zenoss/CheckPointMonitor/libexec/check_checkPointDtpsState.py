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

dtpsStateOID = '.1.3.6.1.4.1.2620.1.9.102.0'

exitStatus = 0

class CheckPointDtpsStatePlugin(EasySnmpPlugin):
    """
    Checks a Check Point firewall using SNMP to verify that the policy server
    (for SecureClient) is running.
    """
    
    oids = [dtpsStateOID,]
    
    def onSuccess(self, result):
        state = result[dtpsStateOID]
        global exitStatus
        if state is None:
            print "no policy server state returned"
            exitStatus = 1
        elif state == "Down":
            print "policy server is down"
            exitStatus = 1
        else:
            print "policy server is running"
        
    def onError(self, result):
        print "error getting policy server state"
        global exitStatus
        exitStatus = 1


if __name__ == "__main__":
    cmd = CheckPointDtpsStatePlugin()
    cmd.run()
    sys.exit(exitStatus)
