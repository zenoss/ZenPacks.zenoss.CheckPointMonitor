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
        summary = "{} status is '{}'".format(self.dsName, statusCode)
        message = "Status code: {};\nShort description: {};".format(statusCode, description)

        # if no value returned for statusCode oid
        if statusCode == -1:
            return data

        data['events'].append(self.getEvent(
            device=config.id,
            summary=summary,
            severity=severity,
            eventClassKey=self.eventClassKey,
            eventKey=self.eventKey,
            message=message
        ))

        return data


class ClusterStatusSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Cluster Status"""

    dsName = 'Cluster'
    eventKey = 'ClusterStatus'
    eventClassKey = 'Cluster'

    def onSuccess(self, result, config):
        """ Override to add Cluster state event

        '.1.3.6.1.4.1.2620.1.5.5.0' - haStarted oid
        '.1.3.6.1.4.1.2620.1.5.6.0' - haState oid
        """

        data = super(ClusterStatusSnmp, self).onSuccess(result, config)

        getData, _ = result

        try:
            haStarted = getData['.1.3.6.1.4.1.2620.1.5.5.0']
            haState = getData['.1.3.6.1.4.1.2620.1.5.6.0']
        except KeyError:
            # no need to create event - PS.Util handle case for missing datapoints
            return data

        # 0 - Clear, 4 - Error
        severity = 0 if haStarted == 'yes' else 4
        summary = "{} is started: {}".format(self.dsName, haStarted)
        message = "Cluster started: {};\nCluster state: {};".format(haStarted, haState)

        data['events'].append(self.getEvent(
            device=config.id,
            summary=summary,
            severity=severity,
            eventClassKey=self.eventClassKey,
            eventKey='HA',
            message=message
        ))

        return data


class UrlFilterSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - URL Filter"""

    dsName = 'URL Filter'
    eventKey = 'UrlFilterStatus'
    eventClassKey = 'UrlFilter'

    def onSuccess(self, result, config):
        """ Override to add RAD status event

        '.1.3.6.1.4.1.2620.1.43.3.1.0' - advancedUrlFilteringRADStatusCode oid
        '.1.3.6.1.4.1.2620.1.43.3.2.0' - advancedUrlFilteringRADStatusDesc oid
        """

        data = super(UrlFilterSnmp, self).onSuccess(result, config)

        getData, _ = result

        try:
            radCode = getData['.1.3.6.1.4.1.2620.1.43.3.1.0']
            radDesc = getData['.1.3.6.1.4.1.2620.1.43.3.2.0']
        except KeyError:
            # no need to create event - PS.Util handle case for missing datapoints
            return data

        # 0 - Clear, 4 - Error
        severity = 0 if radCode == 0 else 4
        summary = "RAD status code is: {}".format(radCode)
        message = "RAD status code: {};\nRAD status description: {};".format(radCode, radDesc)

        data['events'].append(self.getEvent(
            device=config.id,
            summary=summary,
            severity=severity,
            eventClassKey=self.eventClassKey,
            eventKey='RAD',
            message=message
        ))

        return data


class AppControlSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Application Control"""

    dsName = 'Application Control'
    eventKey = 'AppStatus'
    eventClassKey = 'AppControl'


class AntiBotVirusSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Anti-Bot & Anti-Virus status"""

    dsName = 'Anti Bot & Anti Virus'
    eventKey = 'AmwStatus'
    eventClassKey = 'AntiBotVirus'


class IdentityAwarenessSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Identity Awareness"""

    dsName = 'Identity Awareness'
    eventKey = 'IdaStatus'
    eventClassKey = 'IdentityAwareness'


class ThreatEmulationSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Threat Emulation"""

    dsName = 'Threat Emulation'
    eventKey = 'TeStatus'
    eventClassKey = 'ThreatEmulation'


class SmartEventSnmp(StatusCodeDescSnmp):
    """Datasource plugin for monitoring Virtual System - Smart Event"""

    dsName = 'Smart Event (CPSEMD)'
    eventKey = 'SmartEventStatus'
    eventClassKey = 'SmartEvent'
