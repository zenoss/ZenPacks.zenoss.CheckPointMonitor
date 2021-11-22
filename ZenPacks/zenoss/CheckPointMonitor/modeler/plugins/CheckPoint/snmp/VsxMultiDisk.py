##############################################################################
#
# Copyright (C) Zenoss, Inc. 2021, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
"""
CheckPoint Monitor (VSX) modeler plugin for Multi Disk components.

Uses CHECKPOINT-MIB
"""

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap, GetMap

from ZenPacks.zenoss.PS.Util.python_snmp.PythonSnmpModeler import PythonSnmpModeler


class VsxMultiDisk(PythonSnmpModeler):
    """VsxRAID modeler plugin for Multi Disk components."""

    modname = 'ZenPacks.zenoss.CheckPointMonitor.VsxMultiDisk'
    relname = 'vsxMultiDisks'

    snmpGetTableMaps = (
        GetTableMap(
            'multiDiskTable', '.1.3.6.1.4.1.2620.1.6.7.6', {
                '.1.1': 'multiDiskIndex',
                '.1.2': 'multiDiskName',
                '.1.3': 'multiDiskSize'
            },
        ),
    )

    def process(self, device, results, log):
        """Method for processing data collected from Multi Disk components"""

        _, tabledata = results
        multiDiskTable = tabledata.get('multiDiskTable', {})

        maps = []

        # Multi Disk
        rm = self.processMultiDisk(multiDiskTable)
        maps.append(rm)

        return maps

    def processMultiDisk(self, data):
        """Method process() for Multi Disk components"""

        rm = self.relMap()

        for snmpindex, disk in data.items():
            om = self.objectMap({'id': self.prepId('multiDisk_{}'.format(disk.get('multiDiskIndex'))),
                                 'title': disk.get('multiDiskName'),
                                 'multiDiskSize': disk.get('multiDiskSize'),
                                 'snmpindex': snmpindex})

            rm.append(om)
        return rm
