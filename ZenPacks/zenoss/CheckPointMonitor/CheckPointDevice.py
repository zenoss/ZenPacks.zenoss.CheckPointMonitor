######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class CheckPointDevice(Device):
    "A Check Point firewall"
    
    fwModuleState = ""
    
    fwVerMajor = None
    fwVerMinor = None
    fwPolicyName = ""
    fwInstallTime = ""
    
    cpvVerMajor = None
    cpvVerMinor = None
    
    haInstalled = None
    haVerMajor = None
    haVerMinor = None
    haStarted = None
    haState = ""
    
    svnVersion = ""
    
    osName = ""
    osVersionLevel = ""
    
    dtpsVerMajor = None
    dtpsVerMinor = None
    dtpsLicensedUsers = None
    
    _properties = Device._properties + (
        {'id':'fwModuleState', 'type':'string', 'mode':'w'},

        {'id':'fwVerMajor', 'type':'int', 'mode':'w'},
        {'id':'fwVerMinor', 'type':'int', 'mode':'w'},
        {'id':'fwPolicyName', 'type':'string', 'mode':'w'},
        {'id':'fwInstallTime', 'type':'string', 'mode':'w'},

        {'id':'cpvVerMajor', 'type':'int', 'mode':'w'},
        {'id':'cpvVerMinor', 'type':'int', 'mode':'w'},

        {'id':'haInstalled', 'type':'int', 'mode':'w'},
        {'id':'haVerMajor', 'type':'int', 'mode':'w'},
        {'id':'haVerMinor', 'type':'int', 'mode':'w'},
        {'id':'haStarted', 'type':'int', 'mode':'w'},
        {'id':'haState', 'type':'string', 'mode':'w'},

        {'id':'svnVersion', 'type':'string', 'mode':'w'},

        {'id':'osName', 'type':'string', 'mode':'w'},
        {'id':'osVersionLevel', 'type':'string', 'mode':'w'},

        {'id':'dtpsVerMajor', 'type':'int', 'mode':'w'},
        {'id':'dtpsVerMinor', 'type':'int', 'mode':'w'},
        {'id':'dtpsLicensedUsers', 'type':'int', 'mode':'w'},
        )
    
    
    factory_type_information = deepcopy(Device.factory_type_information)
    custom_actions = []
    custom_actions.extend(factory_type_information[0]['actions'])
    custom_actions.insert(2,
           { 'id'              : 'checkPointDeviceDetail'
           , 'name'            : 'Check Point'
           , 'action'          : 'checkPointDeviceDetail'
           , 'permissions'     : (ZEN_VIEW, ) },
           )
    factory_type_information[0]['actions'] = custom_actions
    
        
    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


    def getOsVersionString(self):
        if self.osName and self.osVersionLevel:
            return "%s (%s)" % (self.osName, self.osVersionLevel)
        return "Unknown"
    
    def getSvnVersionString(self):
        return self.svnVersion or "Unknown"
    
    def getFwVersionString(self):
        if self.fwVerMajor is not None and self.fwVerMinor is not None:
            return "%d.%d" % (self.fwVerMajor, self.fwVerMinor)
        return "Unknown"
    
    def getCpvVersionString(self):
        if self.cpvVerMajor is not None and self.cpvVerMinor is not None:
            return "%d.%d" % (self.cpvVerMajor, self.cpvVerMinor)
        return "Unknown"
    
    def getHaVersionString(self):
        if self.haVerMajor is not None and self.haVerMinor is not None:
            return "%d.%d" % (self.haVerMajor, self.haVerMinor)
        return "Unknown"
    
    def getDtpsVersionString(self):
        if self.dtpsVerMajor is not None and self.dtpsVerMinor is not None:
            return "%d.%d" % (self.dtpsVerMajor, self.dtpsVerMinor)
        return "Unknown"
    
    def getFwPolicyName(self):
        return self.fwPolicyName or "Unknown"
    
    def getFwInstallTime(self):
        return self.fwInstallTime or "Unknown"
    
    def getFwStatus(self):
        return self.getStatus(where="component = 'firewall'")
    
    def getHaInstalled(self):
        if self.haInstalled:
            return True
        return False
    
    def getHaStarted(self):
        if self.haStarted and self.haStarted == "yes":
            return True
        return False
    
    def getHaStatus(self):
        return self.getStatus(where="component = 'HA'")
    
    def getDtpsLicensedUsers(self):
        if self.dtpsLicensedUsers is not None:
            return self.dtpsLicensedUsers
        return "Unknown"
    
    def getDtpsStatus(self):
        return self.getStatus(where="component = 'policy server'")


InitializeClass(CheckPointDevice)
