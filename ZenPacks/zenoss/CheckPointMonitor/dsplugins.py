##############################################################################
#
# Copyright (C) Zenoss, Inc. 2021, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
"""
CheckPoint Monitor (VSX) monitoring plugin for VSX Device (Virtual Device and Virtual System).
"""

from ZenPacks.zenoss.PS.Util.datasources.PythonSnmpDataSource import PythonSnmpDataSourcePlugin


class VsxSnmpPlugin(PythonSnmpDataSourcePlugin):
    """Datasource plugin for monitoring VSX Virtual Device"""

    proxy_attributes = PythonSnmpDataSourcePlugin.proxy_attributes + ('devGatewayIp',)

    def collect(self, config, connInfoOverrides=None):
        """Override due to SNMP queries must be sent to the IP address of VSX Gateway"""

        ds0 = config.datasources[0]

        connInfoOverrides = {
            'manageIp': ds0.devGatewayIp
        }

        # call the parent collect with our custom connectionInfo
        return super(VsxSnmpPlugin, self).collect(config, connInfoOverrides)


class VirtualSystemSnmpPlugin(PythonSnmpDataSourcePlugin):
    """Datasource plugin for monitoring VSX Virtual System"""

    proxy_attributes = PythonSnmpDataSourcePlugin.proxy_attributes + ('devGatewayIp', 'devId')

    def collect(self, config, connInfoOverrides=None):
        """Override due to SNMP queries must be sent to the IP address of VSX Gateway and set context - vsid{x}"""

        ds0 = config.datasources[0]

        connInfoOverrides = {
            'manageIp': ds0.devGatewayIp,
            'zSnmpContext': ds0.devId
        }

        # call the parent collect with our custom connectionInfo
        return super(VirtualSystemSnmpPlugin, self).collect(config, connInfoOverrides)

    def onSuccess(self, result, config):
        data = super(VirtualSystemSnmpPlugin, self).onSuccess(result, config)
        return data


class StatusCodeDescSnmp(VirtualSystemSnmpPlugin):
    """Datasource plugin for monitoring Virtual System Statuses - used Status code and Status short desc values"""

    dsName = ''
    eventKey = ''
    eventClassKey = ''

    def onSuccess(self, result, config):
        data = super(StatusCodeDescSnmp, self).onSuccess(result, config)

        statusCode = -1
        description = ''
        getData, _ = result
        for k, v in getData.items():
            if '101' in k:
                statusCode = v
            elif '102' in k:
                description = v

        # 0 - Clear, 4 - Error
        severity = 0 if statusCode == 0 else 4
        summary = "{} status is '{}' ({})".format(self.dsName, statusCode, description)

        data['events'].append(self.getEvent(
            device=config.id,
            summary=summary,
            severity=severity,
            eventClassKey=self.eventClassKey,
            eventKey=self.eventKey,
            message=summary
        ))

        return data


class VpnSiteToSiteSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - VPN Site-to-Site"""

    dsName = 'VPN Site-to-Site'
    eventKey = 'VpnSiteToSiteStatus'
    eventClassKey = '/Status/VSX/VPNS2S'


class VpnRemoteAccessSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - VPN Remote Access"""

    dsName = 'VPN Remote Access'
    eventKey = 'VpnRemoteAccessStatus'
    eventClassKey = '/Status/VSX/RA'


class VSClusterStatusSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Cluster Status"""

    dsName = 'Cluster'
    eventKey = 'ClusterStatus'
    eventClassKey = '/Status/VSX/Cluster'


class UrlFilterSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - URL Filter"""

    dsName = 'URL Filter'
    eventKey = 'UrlFilterStatus'
    eventClassKey = '/Status/VSX/URLFilter'


class AppControlSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Application Control"""

    dsName = 'Application Control'
    eventKey = 'AppControlStatus'
    eventClassKey = '/Status/VSX/AppControl'


class AntiBotVirusSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Anti-Bot & Anti-Virus status"""

    dsName = 'Anti Bot & Anti Virus'
    eventKey = 'AntiBotVirusStatus'
    eventClassKey = '/Status/VSX/AMW'


class IdentityAwarenessSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Identity Awareness"""

    dsName = 'Identity Awareness'
    eventKey = 'IdentityAwarenessStatus'
    eventClassKey = '/Status/VSX/IDA'


class ThreatEmulationSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Threat Emulation"""

    dsName = 'Threat Emulation'
    eventKey = 'ThreatEmulationStatus'
    eventClassKey = '/Status/VSX/TE'


class SmartEventSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Smart Event"""

    dsName = 'Smart Event (CPSEMD)'
    eventKey = 'SmartEventStatus'
    eventClassKey = '/Status/VSX/CPSEMD'
