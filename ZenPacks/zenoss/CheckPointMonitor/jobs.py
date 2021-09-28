##############################################################################
#
# Copyright (C) Zenoss, Inc. 2021 all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from Products.Jobber.jobs import Job

import time
import traceback
from ZODB.transact import transact

from Products.AdvancedQuery import Eq
from Products.Zuul import getFacade
from Products.Zuul.interfaces import ICatalogTool
from zExceptions import NotFound


ZENHUB_DELAY = 60


class VsxDeviceJob(Job):

    def _run(self, vsxDevices, vsxGatewayID):
        """
        TODO
        """

        zep = getFacade("zep", self.dmd)

        # Get the Gateway Device details
        gatewayDev = self.dmd.Devices.findDevice(vsxGatewayID)
        if not gatewayDev:
            self.log.error("Gateway Device {} Not Found - Was it re-id'd or removed?".format(vsxGatewayID))
            return

        collectorId = gatewayDev.getPerformanceServer().id

        # Find devices already added by this Gateway that we can skip
        # And devices added that have disappeared so we can move them into 'Decommissioned' state
        removeDevices = {}
        deviceClass = self.dmd.Devices.getOrganizer('/Network/Check Point/VSX/Device')
        catalog = ICatalogTool(deviceClass)
        query = ~ Eq('productionState', -1)
        devBrains = catalog.search(types=['Products.ZenModel.Device.Device'], query=query)
        if devBrains.total:
            for brain in devBrains:
                try:
                    dev = brain.getObject()
                except NotFound:
                    continue

                devId = dev.id
                if devId not in vsxDevices.keys():
                    removeDevices[devId] = dev
                    self.log.info("Existing device {} no longer managed by Gateway {})".format(devId, vsxGatewayID))
                else:
                    # Skip existing devices
                    vsxDevices.pop(devId)
                    self.log.info("Existing device {} has already been added by Gateway {}".format(devId, vsxGatewayID))

        ###
        # Move old Devices into 'Decommissioned' state

        total = len(removeDevices)
        count = 0
        for devId, device in removeDevices.iteritems():
            count += 1
            self.log.info("Moving into decommissioned production state %s %d/%d (%.2f%%)",
                          devId, count, total,
                          float(count) / total * 100)

            try:
                # -1 is value for Decommissioned state
                device.setProdState(-1)
                device.manageIp = ''
                device.renameDevice(newId='{}-DECOMMISSIONED'.format(devId))
            except Exception as ex:
                self.log.exception("Error while changing production state for device {}".format(devId))
                zep.create(
                    summary=ex.message,
                    severity="Error",
                    device=gatewayDev.id,
                    message=traceback.format_exc(),
                )
            zep.create(
                summary="VSX device {} ({}) not reported from Gateway {}".format(device.title, devId, gatewayDev.id),
                severity="Info",
                device=gatewayDev.id,
                message="Device is not reported in the list of devices for this Gateway. Production state was changed to Decommissioned",
                eventClassKey='VsxDeviceJob'
            )

        ###
        # Add new devices

        total = len(vsxDevices)
        count = 0
        newDevices = []
        for devId, devDetails in vsxDevices.iteritems():
            count += 1

            zenossDeviceId = devDetails['title']
            manageIp = None if devDetails['vsMainIP'] == 'N/A' else devDetails['vsMainIP']
            snmpindex = devDetails['snmpindex']
            vsId = devDetails['vsId']
            if not manageIp:
                self.log.warning("Device %s has no associated manageIp - will add to Zenoss without IP.", devId)

            self.log.info("Creating device %s %d/%d (%.2f%%)",
                          zenossDeviceId, count, total,
                          float(count) / total * 100)

            baseSummary = "VSX device {} reported from Gateway {}".format(devId, gatewayDev.id)
            severity = "Info"

            if gatewayDev.zVsxCreateDevices:
                try:
                    message = "New Device {} reported from Gateway {}. VSX device will be created".format(devId, gatewayDev.id)
                    summary = 'Adding device.' + baseSummary
                    newDevices.append(
                        self.addDevice(
                            zenossDeviceId, manageIp, collectorId, gatewayDev, deviceClass, snmpindex, vsId
                        )
                    )
                # except Exception as ex:
                except RuntimeError as ex:
                    self.log.exception("Error while creating device {}".format(zenossDeviceId))
                    summary = ex.message
                    severity = "Error"
                    message = traceback.format_exc()
            else:
                message = "New Device {} reported from Gateway {}. New VSX device won't be created " \
                          "(because zVsxCreateDevices set to False)".format(devId, gatewayDev.id)
                summary = 'Skip adding device.' + baseSummary

            zep.create(
                summary=summary,
                severity=severity,
                device=gatewayDev.id,
                message=message,
                eventClassKey='VsxDeviceJob'
            )

        # Model the new devices in the background
        if newDevices:
            self.log.info("Waiting {} seconds for ZenHub to learn about new devices".format(ZENHUB_DELAY))
            time.sleep(ZENHUB_DELAY)
            for device in newDevices:
                self.log.info("Scheduling modeling job for {}".format(zenossDeviceId))
                device.collectDevice(background=True, setlog=True)

    @transact
    def addDevice(self, zenossDeviceId, ip, collectorId, tenantDev, deviceClass, snmpindex, vsId):
        """
        TODO
        """

        # Check for duplicate IP
        if ip:
            existing = self.dmd.Devices.findDeviceByIdOrIp(ip)
            if existing:
                raise RuntimeError("Ip {} already in use, unable to create device {}".format(ip, zenossDeviceId))

        device = deviceClass.createInstance(zenossDeviceId)
        if device is None:
            raise RuntimeError("Unable to create device {}".format(zenossDeviceId))
        device.setPerformanceMonitor(collectorId)
        device.devGatewayIp = tenantDev.manageIp
        device.snmpindex = snmpindex
        # vsidN is the SNMP context name required by SNMP v3 (ex. vsid2)
        device.setZenProperty("zSnmpContext", 'vsid{}'.format(vsId))
        if ip:
            device.setManageIp(ip)
            # manageIp won't stick if it's already in use
            if not device.manageIp:
                device.deleteDevice()
                raise RuntimeError("Ip {} already in use, unable to create device {}".format(ip, zenossDeviceId))

        return device
