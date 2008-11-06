######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class DeviceMap(SnmpPlugin):
    """Maps device level information from Trango access points
    """
        
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
        '.1.3.6.1.4.1.2620.1.6.5.7.0': 'osVersionLevel',
        
        '.1.3.6.1.4.1.2620.1.6.7.1.1.0': 'memTotalVirtual',
        '.1.3.6.1.4.1.2620.1.6.7.1.3.0': 'memTotalReal',
        
        '.1.3.6.1.4.1.2620.1.9.2.0': 'dtpsVerMajor',
        '.1.3.6.1.4.1.2620.1.9.3.0': 'dtpsVerMinor',
        '.1.3.6.1.4.1.2620.1.9.4.0': 'dtpsLicensedUsers',
        })
    
    
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['fwModuleState'] is None: return None
        maps = []
        om = self.objectMap(getdata)
        om.setOSProductKey = "%s (%s)" % (om.osName, om.osVersionLevel)
        maps.append(om)
        maps.append(ObjectMap({"totalMemory": om.memTotalReal}, compname="hw"))
        maps.append(ObjectMap({"totalSwap": om.memTotalVirtual}, compname="os"))
        return maps
