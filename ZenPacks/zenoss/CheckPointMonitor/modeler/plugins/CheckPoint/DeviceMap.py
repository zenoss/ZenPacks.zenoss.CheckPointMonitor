##############################################################################
#
# Copyright (C) Zenoss, Inc. 2008, 2014, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################


"""Models Check Point device information using SNMP.

Uses CHECKPOINT-MIB.

"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap, MultiArgs


class DeviceMap(SnmpPlugin):

    """Check Point device modeler plugin."""

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2620.1.1.1.0': 'fwModuleState',

        '.1.3.6.1.4.1.2620.1.1.22.0': 'fwVerMajor',
        '.1.3.6.1.4.1.2620.1.1.23.0': 'fwVerMinor',
        '.1.3.6.1.4.1.2620.1.1.25.1.0': 'fwPolicyName',
        '.1.3.6.1.4.1.2620.1.1.25.2.0': 'fwInstallTime',

        '.1.3.6.1.4.1.2620.1.2.2.0': 'cpvVerMajor',
        '.1.3.6.1.4.1.2620.1.2.3.0': 'cpvVerMinor',

        '.1.3.6.1.4.1.2620.1.5.2.0': 'haInstalled',
        '.1.3.6.1.4.1.2620.1.5.3.0': 'haVerMajor',
        '.1.3.6.1.4.1.2620.1.5.4.0': 'haVerMinor',
        '.1.3.6.1.4.1.2620.1.5.5.0': 'haStarted',
        '.1.3.6.1.4.1.2620.1.5.6.0': 'haState',

        '.1.3.6.1.4.1.2620.1.6.4.1.0': 'svnVersion',

        '.1.3.6.1.4.1.2620.1.6.5.1.0': 'osName',
        '.1.3.6.1.4.1.2620.1.6.5.2.0': 'osMajorVer',
        '.1.3.6.1.4.1.2620.1.6.5.3.0': 'osMinorVer',
        '.1.3.6.1.4.1.2620.1.6.5.7.0': 'osVersionLevel',

        '.1.3.6.1.4.1.2620.1.6.7.1.1.0': 'memTotalVirtual',
        '.1.3.6.1.4.1.2620.1.6.7.1.3.0': 'memTotalReal',
        '.1.3.6.1.4.1.2620.1.6.7.4.1.0': '_memTotalVirtual64',
        '.1.3.6.1.4.1.2620.1.6.7.4.3.0': '_memTotalReal64',

        '.1.3.6.1.4.1.2620.1.9.2.0': 'dtpsVerMajor',
        '.1.3.6.1.4.1.2620.1.9.3.0': 'dtpsVerMinor',
        '.1.3.6.1.4.1.2620.1.9.4.0': 'dtpsLicensedUsers',
        })

    def process(self, device, results, log):
        """Return DataMaps given device and results."""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        if getdata.get('fwModuleState') is None:
            return None

        maps = []
        om = self.objectMap(getdata)

        # Handle all of the OS possibilities.
        if "SecurePlatform" in om.osName or "Gaia" in om.osName:
            manufacturer = "Check Point"
        elif "Nokia" in om.osName:
            manufacturer = "Nokia"
        elif "Linux" in om.osName:
            manufacturer = "Linux"
        elif "Solaris" in om.osName:
            manufacturer = "Sun"
        elif "Windows" in om.osName:
            manufacturer = "Microsoft"
        else:
            manufacturer = "Unknown"

        if not om.osVersionLevel.strip():
            major = getdata.get('osMajorVer')
            minor = getdata.get('osMinorVer')
            if major is not None and minor is not None:
                om.osVersionLevel = '{}.{}'.format(major, minor)

        om.setOSProductKey = MultiArgs(
            "%s (%s)" % (om.osName, om.osVersionLevel),
            manufacturer)

        # Prefer 64bit version of memTotalReal if it exists.
        try:
            om.memTotalReal = int(getdata['_memTotalReal64'])
        except Exception:
            pass

        # Prefer 64bit version of memTotalVirtual if it exists.
        try:
            om.memTotalVirtual = int(getdata['_memTotalVirtual64'])
        except Exception:
            pass

        maps.append(om)
        maps.append(ObjectMap({"totalMemory": om.memTotalReal}, compname="hw"))
        maps.append(ObjectMap({"totalSwap": om.memTotalVirtual}, compname="os"))

        return maps
