##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import sys
from optparse import OptionParser
from twisted.internet import reactor
from pynetsnmp.twistedsnmp import AgentProxy


class EasySnmpPlugin:
    parser = None
    
    
    def __init__(self):
        self.buildOptions()
        self.checkParameters()
    
    
    def buildOptions(self):
        """
        If your plugin requires extra command line options you should
        override this method. Be sure to call EasySnmpPlugin.buildOptions(self)
        at the end of your overridden method to get all of these options too.
        """
        if self.parser is None:
            self.parser = OptionParser()
        
        self.parser.add_option('-H', '--host', dest='host',
            help='Hostname/IP of the SNMP agent')
        self.parser.add_option('-c', '--community', dest='community',
            default='public',
            help='SNMP community string')
        self.parser.add_option('-v', '--version', dest='version',
            default='v2c',
            help='SNMP version (v1, v2c, v3)')
        self.parser.add_option('-p', '--port', dest='port',
            default='161',
            help='SNMP port')
        self.parser.add_option('-t', '--timeout', dest='timeout',
            default='2.5',
            help='SNMP timeout (in seconds)')
        self.parser.add_option('-u', '--securityName', dest='securityName',
            help='SNMPv3 security name')
        self.parser.add_option('-a', '--authType', dest='authType',
            default='',
            help='SNMPv3 authentication type')
        self.parser.add_option('-A', '--authPassword', dest='authPassword',
            default='',
            help='SNMPv3 authentication password')
        self.parser.add_option('-x', '--privType', dest='privType',
            default='',
            help='SNMPv3 privilege type')
        self.parser.add_option('-X', '--privPassword', dest='privPassword',
            default='',
            help='SNMPv3 privilege password')
        self.options, args = self.parser.parse_args()
    
    
    def checkParameters(self):
        """
        If your plugin requires extra command line parameter checking you
        should override this method. Be sure to call
        EasySnmpPlugin.checkParameters(self) at the end of your overridden
        method to get the default options checked too.
        """
        if not self.options.host:
            print "You must specify the host parameter."
            sys.exit(1)
    
    
    def onSuccess(self, result):
        """This method should be overridden in subclass"""
        pass
    
    
    def onError(self, result):
        """This method should be overridden in subclass"""
        pass
    
    
    def getProxy(self):
        cmdLineArgs = []
        if '3' in self.options.version:
            if self.options.privType:
                cmdLineArgs += ['-l', 'authPriv']
                cmdLineArgs += ['-x', self.options.privType]
                cmdLineArgs += ['-X', self.options.privPassword]
            elif self.options.authType:
                cmdLineArgs += ['-l', 'authNoPriv']
            else:
                cmdLineArgs += ['-l', 'noAuthNoPriv']
            if self.options.authType:
                cmdLineArgs += ['-a', self.options.authType]
                cmdLineArgs += ['-A', self.options.authPassword]
            cmdLineArgs += ['-u', self.options.securityName]
        
        return AgentProxy(ip=self.options.host,
            port=int(self.options.port),
            timeout=self.options.timeout,
            snmpVersion=self.options.version,
            community=self.options.community,
            cmdLineArgs=cmdLineArgs,
            protocol=None,
            allowCache=False)
    
    
    def run(self):
        p = self.getProxy()
        p.open()
        d = p.get(self.oids)
        d.addBoth(self.closer, p)
        d.addCallback(self.onSuccess)
        d.addErrback(self.onError)
        reactor.run()
    
    
    def closer(self, result, proxy):
        reactor.stop()
        proxy.close()
        return result
