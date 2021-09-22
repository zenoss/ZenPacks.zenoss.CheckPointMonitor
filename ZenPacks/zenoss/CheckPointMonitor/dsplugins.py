##############################################################################
#
# Copyright (C) Zenoss, Inc. 2021, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
"""
CheckPoint Monitor (VSX) monitoring plugin for VSX Device (Virtual Device).
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
