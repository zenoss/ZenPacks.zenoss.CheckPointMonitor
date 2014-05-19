##############################################################################
#
# Copyright (C) Zenoss, Inc. 2008, 2014, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from copy import deepcopy

from Globals import InitializeClass

from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW


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

    memTotalReal = None
    memTotalVirtual = None

    svnVersion = ""

    osName = ""
    osMajorVer = None
    osMinorVer = None
    osVersionLevel = ""

    dtpsVerMajor = None
    dtpsVerMinor = None
    dtpsLicensedUsers = None

    _properties = Device._properties + (
        {'id': 'fwModuleState', 'type': 'string', 'mode': 'w'},

        {'id': 'fwVerMajor', 'type': 'string', 'mode': 'w'},
        {'id': 'fwVerMinor', 'type': 'string', 'mode': 'w'},
        {'id': 'fwPolicyName', 'type': 'string', 'mode': 'w'},
        {'id': 'fwInstallTime', 'type': 'string', 'mode': 'w'},

        {'id': 'cpvVerMajor', 'type': 'string', 'mode': 'w'},
        {'id': 'cpvVerMinor', 'type': 'string', 'mode': 'w'},

        {'id': 'haInstalled', 'type': 'string', 'mode': 'w'},
        {'id': 'haVerMajor', 'type': 'string', 'mode': 'w'},
        {'id': 'haVerMinor', 'type': 'string', 'mode': 'w'},
        {'id': 'haStarted', 'type': 'string', 'mode': 'w'},
        {'id': 'haState', 'type': 'string', 'mode': 'w'},

        {'id': 'memTotalReal', 'type': 'int', 'mode': 'w'},
        {'id': 'memTotalVirtual', 'type': 'int', 'mode': 'w'},

        {'id': 'svnVersion', 'type': 'string', 'mode': 'w'},

        {'id': 'osName', 'type': 'string', 'mode': 'w'},
        {'id': 'osMajorVer', 'type': 'int', 'mode': 'w'},
        {'id': 'osMinorVer', 'type': 'int', 'mode': 'w'},
        {'id': 'osVersionLevel', 'type': 'string', 'mode': 'w'},

        {'id': 'dtpsVerMajor', 'type': 'string', 'mode': 'w'},
        {'id': 'dtpsVerMinor', 'type': 'string', 'mode': 'w'},
        {'id': 'dtpsLicensedUsers', 'type': 'string', 'mode': 'w'},
        )

    factory_type_information = deepcopy(Device.factory_type_information)
    custom_actions = []
    custom_actions.extend(factory_type_information[0]['actions'])
    custom_actions.insert(2, {
        'id': 'checkPointDeviceDetail',
        'name': 'Check Point Details',
        'action': 'checkPointDeviceDetail',
        'permissions': (ZEN_VIEW, ),
        })

    factory_type_information[0]['actions'] = custom_actions

    def getOsVersionString(self):
        if self.osName and self.osVersionLevel:
            return "%s (%s)" % (self.osName, self.osVersionLevel)
        return "Unknown"

    def getSvnVersionString(self):
        return self.svnVersion or "Unknown"

    def getFwVersionString(self):
        if self.fwVerMajor is not None and self.fwVerMinor is not None:
            return "%s.%s" % (self.fwVerMajor, self.fwVerMinor)
        return "Unknown"

    def getCpvVersionString(self):
        if self.cpvVerMajor is not None and self.cpvVerMinor is not None:
            return "%s.%s" % (self.cpvVerMajor, self.cpvVerMinor)
        return "Unknown"

    def getHaVersionString(self):
        if self.haVerMajor is not None and self.haVerMinor is not None:
            return "%s.%s" % (self.haVerMajor, self.haVerMinor)
        return "Unknown"

    def getDtpsVersionString(self):
        if self.dtpsVerMajor is not None and self.dtpsVerMinor is not None:
            return "%s.%s" % (self.dtpsVerMajor, self.dtpsVerMinor)
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
