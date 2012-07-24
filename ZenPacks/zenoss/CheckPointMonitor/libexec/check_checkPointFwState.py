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

fwModuleStateOID = '.1.3.6.1.4.1.2620.1.1.1.0'

exitStatus = 0

class CheckPointFwStatePlugin(EasySnmpPlugin):
    """
    Checks a Check Point firewall using SNMP to verify that the firewall module
    currently has a policy installed.
    """
    
    oids = [fwModuleStateOID,]
    
    def onSuccess(self, result):
        state = result[fwModuleStateOID]
        global exitStatus
        if state is None:
            print "no firewall state returned"
            exitStatus = 1
        elif state == "Installed":
            print "firewall policy is installed"
        else:
            print "firewall policy is not installed"
            exitStatus = 1
        
    def onError(self, result):
        print "error getting firewall state"
        global exitStatus
        exitStatus = 1


if __name__ == "__main__":
    cmd = CheckPointFwStatePlugin()
    cmd.run()
    sys.exit(exitStatus)
