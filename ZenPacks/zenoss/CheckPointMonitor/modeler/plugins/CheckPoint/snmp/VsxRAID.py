##############################################################################
#
# Copyright (C) Zenoss, Inc. 2021, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
"""
CheckPoint Monitor (VSX) modeler plugin for RAID Volume and RAID Disk components.

Uses CHECKPOINT-MIB
"""

from collections import defaultdict

from Products.DataCollector.plugins.DataMaps import RelationshipMap, ObjectMap
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap, GetMap

from ZenPacks.zenoss.PS.Util.python_snmp.PythonSnmpModeler import PythonSnmpModeler


RAID_TYPE_DICT = {
    0: 'RAID-0',
    1: 'RAID-1E',
    2: 'RAID-1',
    3: 'RAID_10',
    4: 'RAID-4',
    5: 'RAID-5',
    6: 'RAID-6',
    7: 'RAID-60',
    8: 'RAID-50'
}
RAID_DISK_NUMBER = {
    0: 'Appliance',
    1: 'upper disc',
    2: 'lower disc'
}


class VsxRAID(PythonSnmpModeler):
    """VsxRAID modeler plugin for RAID Volume and RAID Disk components."""

    modname = 'ZenPacks.zenoss.CheckPointMonitor.VsxRAIDVolume'
    relname = 'vsxRAIDVolumes'

    snmpGetTableMaps = (
        GetTableMap(
            'raidVolumeTable', '.1.3.6.1.4.1.2620.1.6.7.7.1', {
                '.1.1': 'raidVolumeIndex',
                '.1.2': 'raidVolumeID',
                '.1.3': 'raidVolumeType',
                '.1.4': 'numOfDisksOnRaid',
                '.1.5': 'raidVolumeMaxLBA',
                '.1.8': 'raidVolumeSize'
            },
        ),
        GetTableMap(
            'raidDiskTable', '.1.3.6.1.4.1.2620.1.6.7.7.2', {
                '.1.1': 'raidDiskIndex',
                '.1.2': 'raidDiskVolumeID',
                '.1.3': 'raidDiskID',
                '.1.4': 'raidDiskNumber',
                '.1.5': 'raidDiskVendor',
                '.1.6': 'raidDiskProductID',
                '.1.7': 'raidDiskRevision',
                '.1.8': 'raidDiskMaxLBA',
                '.1.12': 'raidDiskSize',

            },
        ),

    )


    def process(self, device, results, log):
        """Method for processing data collected from RAID Volume and RAID Disk components"""

        _, tabledata = results
        raidVolumeTable = tabledata.get('raidVolumeTable', {})
        raidDiskTable = tabledata.get('raidDiskTable', {})

        maps = []

        # RAID Volume
        rm, volumeCompnames = self.processVolume(raidVolumeTable)
        maps.append(rm)

        # RAID Disk
        rm = self.processDisk(raidDiskTable, volumeCompnames, log)
        maps.extend(rm)

        return maps

    def processVolume(self, data):
        """Method process() for RAID Volume components"""

        compnames = {}
        rm = self.relMap()

        for snmpindex, volume in data.items():
            om = self.objectMap({'id': self.prepId('raidVolume_{}'.format(volume.get('raidVolumeID'))),
                                 'raidVolumeIndex': volume.get('raidVolumeIndex'),
                                 'raidVolumeID': volume.get('raidVolumeID'),
                                 'raidVolumeType': RAID_TYPE_DICT.get(volume.get('raidVolumeType')),
                                 'numOfDisksOnRaid': volume.get('numOfDisksOnRaid'),
                                 'raidVolumeMaxLBA': volume.get('raidVolumeMaxLBA'),
                                 'raidVolumeSize': self.toBytes(volume.get('raidVolumeSize', 0)),
                                 'snmpindex': snmpindex})

            # compnames - used for building compname for disk component
            compnames[om.raidVolumeID] = "{}/{}".format(self.relname, om.id)
            rm.append(om)
        return rm, compnames

    def processDisk(self, data, volumeCompnames, log):
        """Method process() for RAID Disk components"""

        modname = 'ZenPacks.zenoss.CheckPointMonitor.VsxRAIDDisk'
        relname = 'vsxRAIDDisks'

        maps = []
        sortedData = defaultdict(list)

        # group data by 'raidDiskVolumeID' field
        for snmpindex, disk in data.items():
            volumeID = disk.get('raidDiskVolumeID')
            disk.update({'snmpindex': snmpindex})
            sortedData[volumeID].append(disk)

        for volumeID, raidDisks in sortedData.items():
            compname = volumeCompnames.get(volumeID)
            if compname:
                diskMaps = []
                for disk in raidDisks:
                    diskID = self.prepId('{}_raidDisk_{}'.format(compname.split('/')[1], disk.get('raidDiskID')))
                    diskMaps.append(ObjectMap(data={'id': diskID,
                                                    'raidDiskIndex': disk.get('raidDiskIndex'),
                                                    'raidDiskID': disk.get('raidDiskID'),
                                                    'raidDiskNumber': RAID_DISK_NUMBER.get(disk.get('raidDiskNumber')),
                                                    'raidDiskVendor': disk.get('raidDiskVendor'),
                                                    'raidDiskProductID': disk.get('raidDiskProductID'),
                                                    'raidDiskRevision': disk.get('raidDiskRevision'),
                                                    'raidDiskMaxLBA': disk.get('raidDiskMaxLBA'),
                                                    'raidDiskSize': self.toBytes(disk.get('raidDiskSize', 0)),
                                                    'snmpindex': disk.get('snmpindex')}))

            else:
                log.error('No compname. Skip creation of subcomponents for RAID Volume component '
                          '(raidVolumeID={})'.format(volumeID))
                return maps
            rm = RelationshipMap(compname=compname,
                                 relname=relname,
                                 modname=modname,
                                 objmaps=diskMaps)
            maps.append(rm)

        return maps

    def toBytes(self, value):
        """Convert GB to Bytes (1 Gigabytes = 1073741824 Bytes)"""
        return int(value)*1073741824
