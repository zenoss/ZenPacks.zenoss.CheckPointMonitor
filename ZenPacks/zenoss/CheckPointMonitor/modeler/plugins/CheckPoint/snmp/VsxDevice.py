##############################################################################
#
# Copyright (C) Zenoss, Inc. 2021, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
"""
CheckPoint Monitor (VSX) modeler plugin for VSX Device components.

Uses CHECKPOINT-MIB
"""

from Products.DataCollector.plugins.DataMaps import RelationshipMap, ObjectMap
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap, GetMap

from ZenPacks.zenoss.PS.Util.python_snmp.PythonSnmpModeler import PythonSnmpModeler


class VsxDevice(PythonSnmpModeler):
    """VsxDevice modeler plugin for VSX Device components."""

    modname = 'ZenPacks.zenoss.CheckPointMonitor.VsxDevice'
    relname = 'vsxDevices'

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2620.1.6.7.4.3.0': 'memTotalReal64',
        '.1.3.6.1.4.1.2620.1.6.7.4.1.0': 'memTotalVirtual64',
    })

    snmpGetTableMaps = (
        GetTableMap(
            'vsxStatusTable', '.1.3.6.1.4.1.2620.1.16.22.1', {
                '.1.1': 'vsxStatusVSId',
                '.1.2': 'vsxStatusVRId',
                '.1.3': 'vsxStatusVsName',
                '.1.4': 'vsxStatusVsType',
                '.1.5': 'vsxStatusMainIP',
                '.1.6': 'vsxStatusPolicyName',
                '.1.7': 'vsxStatusVsPolicyType',
                '.1.8': 'vsxStatusSicTrustState',
                '.1.10': 'vsxStatusVSWeight'
            },
        ),
    )


    def process(self, device, results, log):

        getdata, tabledata = results
        maps = []

        rm = self.relMap()
        vsxDevices = tabledata.get('vsxStatusTable', {})
        setDevices = {}
        for snmpindex, row in vsxDevices.items():
            # The results also includes the context of VSX Gateway itself (VS0).
            if not row.get('vsxStatusVSId') == 0:
                vsxID = row.get('vsxStatusVSId')
                vsxName = row.get('vsxStatusVsName')
                devDict = {
                    'title': vsxName,
                    'vsType': row.get('vsxStatusVsType'),
                    'vsMainIP': row.get('vsxStatusMainIP'),
                    'vsPolicyName': row.get('vsxStatusPolicyName'),
                    'vsPolicyType': row.get('vsxStatusVsPolicyType'),
                    'vsId': vsxID,
                    'snmpindex': snmpindex
                }

                rm.append(self.objectMap(dict(devDict, **{'id': self.prepId('vsxdev_%s' % vsxID)})))
                setDevices[vsxName] = dict(devDict, **{'id': self.prepId('vsxdiscovered_%s' % vsxID)})

        # discovered devices
        gatewayOm = ObjectMap()
        gatewayOm.setDevices = setDevices

        maps.append(rm)
        maps.append(gatewayOm)

        maps.append(ObjectMap({"totalMemory": int(getdata.get('memTotalReal64'))}, compname="hw"))
        maps.append(ObjectMap({"totalSwap": int(getdata.get('memTotalVirtual64'))}, compname="os"))

        return maps
