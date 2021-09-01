##############################################################################
#
# Copyright (C) Zenoss, Inc. 2021, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

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
    """TODO"""

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
                '.1.6': 'raidVolumeState',  # to monitor
                '.1.7': 'raidVolumeFlags',  # to monitor??
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
                '.1.9': 'raidDiskState',  # to monitor
                '.1.10': 'raidDiskFlags',  # to monitor??
                '.1.11': 'raidDiskSyncState',  # to monitor??
                '.1.12': 'raidDiskSize',

            },
        ),

    )


    def process(self, device, results, log):

        _, tabledata = results
        raidVolumeTable = tabledata.get('raidVolumeTable', {})
        raidDiskTable = tabledata.get('raidDiskTable', {})

        maps = []

        # RAID Volume
        rm, volumeCompnames = self.processVolume(raidVolumeTable)
        maps.append(rm)

        # RAID Disk
        rm = self.processDisk(raidDiskTable, volumeCompnames)
        maps.extend(rm)

        return maps

    def processVolume(self, data):
        compnames = {}
        rm = RelationshipMap(compname=self.compname, relname=self.relname, modname=self.modname)
        for snmpindex, row in data.items():
            om = self.objectMap({
                'id': self.prepId('raidVolume_%s' % row.get('raidVolumeID')),
                'raidVolumeIndex': row.get('raidVolumeIndex'),
                'raidVolumeID': row.get('raidVolumeID'),
                'raidVolumeType': RAID_TYPE_DICT.get(row.get('raidVolumeType')),
                'numOfDisksOnRaid': row.get('numOfDisksOnRaid'),
                'raidVolumeMaxLBA': row.get('raidVolumeMaxLBA'),
                'raidVolumeSize': row.get('raidVolumeSize')
            })
            compnames[om.raidVolumeID] = "{}/{}".format(self.relname, om.id)
            rm.append(om)
        return rm, compnames

    def processDisk(self, data, volumeCompnames):
        modname = 'ZenPacks.zenoss.CheckPointMonitor.VsxRAIDDisk'
        relname = 'vsxRAIDDisks'

        maps = []

        sortedData = {}
        for v in data.values():
            index = v.get('raidDiskVolumeID')
            if index in sortedData.keys():
                sortedData[index].append(v)
            else:
                sortedData[index] = [v]

        for volumeID, raidDisks in sortedData.items():
            compname = volumeCompnames[volumeID]
            rm = RelationshipMap(compname=compname, relname=relname, modname=modname)
            for disk in raidDisks:
                rm.append(self.objectMap({
                        'id': self.prepId('raidDisk_%s' % disk.get('raidDiskID')),
                        'raidDiskIndex': disk.get('raidDiskIndex'),
                        'raidDiskNumber': RAID_DISK_NUMBER.get(disk.get('raidDiskNumber')),
                        'raidDiskVendor': disk.get('raidDiskVendor'),
                        'raidDiskProductID': disk.get('raidDiskProductID'),
                        'raidDiskRevision': disk.get('raidDiskRevision'),
                        'raidDiskMaxLBA': disk.get('raidDiskMaxLBA'),
                        'raidDiskSize': disk.get('raidDiskSize')
                    }))
            maps.append(rm)
        return maps



