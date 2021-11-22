##############################################################################
#
# Copyright (C) Zenoss, Inc. 2008, 2014, 2021 all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from copy import deepcopy

from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.Zuul import getFacade

from zenoss.protocols.protobufs.zep_pb2 import (
    STATUS_NEW, STATUS_ACKNOWLEDGED, STATUS_SUPPRESSED,
    SEVERITY_CRITICAL, SEVERITY_ERROR, SEVERITY_WARNING,
    )

from . import schema as schema
from .jobs import VsxDeviceJob



class CheckPointDevice(schema.CheckPointDevice):
    """A Check Point firewall"""

    factory_type_information = deepcopy(schema.CheckPointDevice.factory_type_information)
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
        return self.getComponentStatus('firewall')

    def getHaInstalled(self):
        if self.haInstalled:
            return True
        return False

    def getHaStarted(self):
        if self.haStarted and self.haStarted == "yes":
            return True
        return False

    def getHaStatus(self):
        return self.getComponentStatus('HA')

    def getDtpsLicensedUsers(self):
        if self.dtpsLicensedUsers is not None:
            return self.dtpsLicensedUsers
        return "Unknown"

    def getDtpsStatus(self):
        return self.getComponentStatus('policy server')

    def getComponentStatus(self, component_id):
        zep = getFacade('zep')

        event_filter = zep.createEventFilter(
            tags=[self.getUUID()],
            element_sub_identifier=[component_id],
            severity=[SEVERITY_WARNING, SEVERITY_ERROR, SEVERITY_CRITICAL],
            status=[STATUS_NEW, STATUS_ACKNOWLEDGED, STATUS_SUPPRESSED],
            event_class=['/Status/*'])

        summaries = zep.getEventSummaries(
            offset=0, limit=0, filter=event_filter)

        return summaries['total']

    def setDevices(self, vsxDevices):
        """
        Creates managed devices under /Network/Check Point/VSX/Device device class.
        """
        if vsxDevices:
            self.dmd.JobManager.addJob(
                VsxDeviceJob,
                description="Creating virtual devices for VSX Gateway %s" % self.id,
                kwargs={
                    "vsxGatewayID": self.id,
                    "vsxDevices": vsxDevices,
                }
            )

