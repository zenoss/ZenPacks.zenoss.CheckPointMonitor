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

Starting from 3.0.0 version the ZenPacks.zenoss.CheckPointMonitor includes the new SNMP structures for Virtual Firewalls
to support the CheckPoint R80.30 version. For modeling/monitoring VSX devices SNMP v3 and SNMP VS Mode were used.


Prerequisites
-------------

==================  ==========================================================
Prerequisite        Restriction
==================  ==========================================================
Product             Zenoss 6.0 or higher
Required ZenPacks   ZenPacks.zenoss.PS.Util>=1.9.9
                    ZenPacks.zenoss.ZenPackLib>=2.1.1
==================  ==========================================================


Device Classes
--------------

ZenPack provides the following device classes:

* /Network/Check Point
* /Network/Check Point/Gaia
* /Network/Check Point/SPLAT
* /Network/Check Point/VSX
* /Network/Check Point/VSX/Gateway
* /Network/Check Point/VSX/Device


Configuring Check Point Firewalls to Allow SNMP Queries
-------------------------------------------------------

This ZenPack supports SNMP for collecting modeling data and metrics. CheckPointMonitor ZenPack supports SNMP v3.
Configure the Check Point firewall to allow SNMP queries from Zenoss platform, and to send SNMP traps to Zenoss platform.


Configuring Zenoss platform
---------------------------

All Check Point devices must exist under the */Devices/Network/Check Point* device class.

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
    zSnmpMonitorIgnore  Whether or not to ignore monitoring SNMP on a device. This should be set to *False*
    zSnmpPort           Port that the SNMP agent listens on (the default port is *161*)
    zSnmpVer            SNMP version used. Valid values are v1, v2c, v3 (the default is *v2c*)
    zSnmpAuthPassword   The shared private key used for authentication
    zSnmpAuthType       Use *"MD5"* or *"SHA"* signatures to authenticate SNMP requests
    zSnmpPrivPassword   The shared private key used for encrypting SNMP requests
    zSnmpPrivType       *"DES"* or *"AES"* cryptographic algorithms
    zSnmpSecurityName   The Security Name (user) to use when making SNMPv3 requests.
    ==================  ==========================================================

3. Click *Save* to save your changes. You will now be able to start collecting the Check Point firewall metrics from this device.

4. Navigate to Graphs and you should see some placeholders for performance graphs. After approximately fifteen minutes you should see the graphs start to become populated with information.


VSX
---

Virtual System Extension. Check Point virtual networking solution, hosted on a computer or cluster with virtual abstractions of Check Point Security Gateways and other network devices.


Gateway
=======

A VSX Gateway is a physical machine that hosts virtual networks of Virtual Devices, with the functionality of their physical network counterparts such as: Security Gateways, routers and switches.


Modeler Plugins:

* CheckPoint.DeviceMap
* CheckPoint.snmp.VsxDevice
* CheckPoint.snmp.VsxRAID
* CheckPoint.snmp.VsxMultiDisk


zDeviceTemplates:

* Device
* GatewayDevice


zProperties:

* *zVsxCreateDevices* - Whether or not to create Virtual Firewalls (True by default)


Components Modeled:

* Multi Disk
* RAID Volume
* RAID Disk
* VSX Device


SNMP Based Monitoring Events:

* vsxDeviceTemplate (monitoring template for VSX Device component)

    Monitors High Availability status for Virtual Devices with oid

    =================================  =======================
    OID                                Name
    =================================  =======================
    1.3.6.1.4.1.2620.1.16.22.1.1.9     vsxStatusHAState
    =================================  =======================

    Raises event with eventClass '/Status/VSX/HA' and message

    *"vsxStatusHAState is '{vsxStatusHAState}'"*


Devices (Virtual Firewalls)
===========================

Types of Virtual Devices:

 - Virtual Router (VR)
 - Virtual Switch (VSW)
 - Virtual System (VS)


Virtual Devices (Virtual Firewalls) are created during Gateway modeling (if *zVsxCreateDevices* set to True)


zDeviceTemplates:

* VirtualDevice
* VsHaState
* VsVpnSiteToSite
* VsVpnRemoteAccess
* VsClusterStatus
* VsUrlFilter
* VsAppControl
* VsAntiBotVirus
* VsIdentityAwareness
* VsThreatEmulation
* VsSmartEvent


SNMP Based Monitoring Events:

* VsHaState

    Monitors High Availability status for Virtual Devices with oid

    =================================  =======================
    OID                                Name
    =================================  =======================
    1.3.6.1.4.1.2620.1.16.22.1.1.9     vsxStatusHAState
    =================================  =======================

    Raises event with eventClassKey 'VsHA' (mapped to /Status/VSX/HA) and message

    *"HA state is '{vsxStatusHAState}'"*

* VsVpnRemoteAccess

    Monitors Virtual System VPN Remote Access user state with oid

    =================================  =======================
    OID                                Name
    =================================  =======================
    1.3.6.1.4.1.2620.500.9000.1.20.0   raUserState
    =================================  =======================


    Events generated from Thresholds
        * Remote Access User State

    Raises event with eventClass '/Status/VSX/RA'

* VsClusterStatus

    Monitors Virtual System Cluster status with oids

    =================================  =======================
    OID                                Name
    =================================  =======================
    1.3.6.1.4.1.2620.1.5.5.0           haStarted
    1.3.6.1.4.1.2620.1.5.6.0           vsHaState
    1.3.6.1.4.1.2620.1.5.101.0         haStatCode
    1.3.6.1.4.1.2620.1.5.102.0         haStatShort
    =================================  =======================

    Raises 2 events with eventClassKey 'VsCluster' (mapped to /Status/VSX/Cluster) and messages

    1. *"Status code: {haStatCode}; Short description: {haStatShort};"*
    2. *"Cluster started: {haStarted}; Cluster state: {haState};"*

* VsUrlFilter

    Monitors Virtual System URL Filter status with oids

    =================================  =======================
    OID                                Name
    =================================  =======================
    1.3.6.1.4.1.2620.1.43.3.1.0        RADStatusCode
    1.3.6.1.4.1.2620.1.43.3.2.0        RADStatusDesc
    1.3.6.1.4.1.2620.1.43.3.101.0      urlFilteringStatus
    1.3.6.1.4.1.2620.1.43.3.102.0      urlFilteringShort
    =================================  =======================

    Raises 2 events with eventClassKey 'VsUrlFilter' (mapped to /Status/VSX/URLFilter) and messages

    1. *"Status code: {urlFilteringStatus}; Short description: {urlFilteringShort};"*
    2. *"RAD status code: {RADStatusCode}; RAD status description: {RADStatusDesc};"*

* VsAppControl

    Monitors Virtual System Application Control status with oids

    =================================  =======================
    OID                                Name
    =================================  =======================
    1.3.6.1.4.1.2620.1.39.101.0        appStatusCode
    1.3.6.1.4.1.2620.1.39.102.0        appShortDesc
    =================================  =======================

    Raises event with eventClassKey 'VsAppControl' (mapped to /Status/VSX/AppControl) and message

    *"Status code: {appStatusCode}; Short description: {appShortDesc};"*

* VsAntiBotVirus

    Monitors Virtual System Anti-Bot & Anti-Virus status with oids

    =================================  =======================
    OID                                Name
    =================================  =======================
    1.3.6.1.4.1.2620.1.46.101.0        amwStatusCode
    1.3.6.1.4.1.2620.1.46.102.0        amwStatusShortDesc
    =================================  =======================

    Raises event with eventClassKey 'VsAntiBotVirus' (mapped to /Status/VSX/AMW) and message

    *"Status code: {amwStatusCode}; Short description: {amwStatusShortDesc};"*

* VsIdentityAwareness

    Monitors Virtual System Identity Awareness status with oids

    =================================  =======================
    OID                                Name
    =================================  =======================
    1.3.6.1.4.1.2620.1.38.101.0        idaStatus
    1.3.6.1.4.1.2620.1.38.102.0        idaStatusShortDesc
    =================================  =======================

    Raises event with eventClassKey 'VsIdentityAwareness' (mapped to /Status/VSX/IDA) and message

    *"Status code: {idaStatus}; Short description: {idaStatusShortDesc};"*

* VsThreatEmulation

    Monitors Virtual System Threat Emulation status with oids

    =================================  =======================
    OID                                Name
    =================================  =======================
    1.3.6.1.4.1.2620.1.49.101.0        teStatusCode
    1.3.6.1.4.1.2620.1.49.102.0        teStatusShortDesc
    =================================  =======================

    Raises event with eventClassKey 'VsThreatEmulation' (mapped to /Status/VSX/TE) and message

    *"Status code: {teStatusCode}; Short description: {teStatusShortDesc};"*

* VsSmartEvent

    Monitors Virtual System Smart Event status with oids

    =================================  =======================
    OID                                Name
    =================================  =======================
    1.3.6.1.4.1.2620.1.25.101.0        cpsemdStatCode
    1.3.6.1.4.1.2620.1.25.102.0        cpsemdStatShortDescr
    1.3.6.1.4.1.2620.1.25.1.1          cpsemdProcAlive
    =================================  =======================

    Raises event with eventClassKey 'VsSmartEvent' (mapped to /Status/VSX/CPSEMD) and message

    *"Status code: {cpsemdStatCode}; Short description: {cpsemdStatShortDescr};"*

    Events generated from Thresholds
        * CPSEMD Process Status


SNMP VS Mode Notes
------------------

* Check Point VSX OID Branch 1.3.6.1.4.1.2620.1.16 is available only in the context of VS0. The SNMP response contains the data from all configured Virtual Devices [Limitation ID 01453316].

* SNMP OIDs other than VSX OID Branch 1.3.6.1.4.1.2620.1.16 can be queried per Virtual Device. The SNMP response contains the data only from the specific queried Virtual Device.

* Only SNMP daemon running in the context of VS0 supports SNMP traps.

* To query specific Virtual Device (not VS0), use SNMP v3 and specify the required Virtual Device context in the following format:

    `[Expert@HostName:0]# snmpwalk -v3 -u SNMPv3_USER -l <authNoPriv | authPriv> -A PASSPHRASE -n vsid<VSID_NUMBER> <IP_ADDRESS_OF_VSX_GATEWAY_ITSELF> <OID>`


Changelog
---------

2.0.1

    * Released on 2016/09/06
    * Compatible with Zenoss Resource Manager 4.1.x, Zenoss Resource Manager 4.2.x, Zenoss Resource Manager 5.0.x, Zenoss Resource Manager 5.1.x, Zenoss Resource Manager 5.x.x
