=================================
ZenPacks.zenoss.CheckPointMonitor
=================================

.. contents::
    :depth: 3

About
-----
The ZenPacks.zenoss.CheckPointMonitor ZenPack monitors security appliances from Check Point.

With this ZenPack, you can ensure that the firewall module has a policy installed,
HA is in a proper state, and that the policy server (for SecureClient) is running.


Prerequisites
-------------

==================  ==========================================================
Prerequisite        Restriction
==================  ==========================================================
Product             Zenoss 6.0 or higher
Required ZenPacks   ZenPacks.zenoss.PS.Util>=1.9.9
                    ZenPacks.zenoss.ZenPackLib>=2.1.1
==================  ==========================================================


Configuring Check Point Firewalls to Allow SNMP Queries
-------------------------------------------------------

This ZenPack supports SNMP for collecting modeling data and metrics.
Configure the Check Point firewall to allow SNMP queries from Zenoss platform, and to send SNMP traps to Zenoss platform.


Configuring Zenoss platform
---------------------------

All Check Point devices must exist under the */Devices/Network/Check* Point device class.

1. Navigate to the device or device class in the Zenoss platform interface

  * If applying changes to a device class:

    a) Select the class in the devices hierarchy.
    b) Click **Details**.
    c) Select Configuration Properties.

  * If applying changes to a device:

    a) Click the device in the device list.
    b) Select Configuration Properties.

2. Edit the appropriate configuration properties for the device or devices.

  * Check Point Configuration Properties

    ==================  ==========================================================
    Name                Description
    ==================  ==========================================================
    zSnmpCommunity      Consult with your network administrators to determine the SNMP community permitted.
    zSnmpMonitorIgnore  This should be set to *False*
    zSnmpPort           The default port is *161*
    zSnmpVer            The default is *v2c*
    ==================  ==========================================================

3. Click *Save* to save your changes. You will now be able to start collecting the Check Point firewall metrics from this device.

4. Navigate to Graphs and you should see some placeholders for performance graphs. After approximately fifteen minutes you should see the graphs start to become populated with information.


Daemons
-------

=====================  ==============
Type                   Name
=====================  ==============
Modeler                zenmodeler
Performance Collector  zenperfsnmp
=====================  ==============


Releases
--------

Version 2.0.1

    Released on 2016/09/06

    Compatible with Zenoss Resource Manager 4.1.x, Zenoss Resource Manager 4.2.x, Zenoss Resource Manager 5.0.x, Zenoss Resource Manager 5.1.x, Zenoss Resource Manager 5.x.x
