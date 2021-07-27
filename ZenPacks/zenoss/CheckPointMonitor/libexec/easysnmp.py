##############################################################################
#
# Copyright (C) Zenoss, Inc. 2021, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import sys

from optparse import make_option

from pynetsnmp.twistedsnmp import AgentProxy
from twisted.internet import reactor
from twisted.python.failure import Failure


class Agent:
    """
    Utility class designed to make SNMP access from command line scripts
    as easy as possible.
    SNMP versions 1, 2c and 3 are supported.
    Warning: The get and walk methods start and stop the twisted reactor
    so you should not use this class within a program that's already
    using twisted.
    """

    _proxy = None
    _result = None

    options = [
        make_option('-H', '--host', dest='host', help='IP of the SNMP agent'),
        make_option('-c', '--community', dest='community', default='public', help='SNMP community string'),
        make_option('-v', '--version', dest='version', default='v2c', help='SNMP version (v1, v2c, v3)'),
        make_option('-p', '--port', dest='port', default='161', help='SNMP port'),
        make_option('-t', '--timeout', dest='timeout', default='2', help='SNMP timeout (in seconds)'),
        make_option('-u', '--securityName', dest='securityName', help='SNMPv3 security name'),
        make_option('-a', '--authType', dest='authType', default='', help='SNMPv3 authentication type'),
        make_option('-A', '--authPassword', dest='authPassword', default='', help='SNMPv3 authentication password'),
        make_option('-x', '--privType', dest='privType', default='', help='SNMPv3 privilege type'),
        make_option('-X', '--privPassword', dest='privPassword', default='', help='SNMPv3 privilege password'),
        make_option('-i', '--snmp_index', dest='snmp_index', default='0', help='SNMP index'),
        ]

    def initialize(self, options):
        """
        Validate options and initialize agent.
        Raises exception if options fail to validate or agent can't be
        initialized for any other reason.
        """
        if not options.host:
            raise Exception("You must specify the host parameter")

        cmdLineArgs = []
        if '3' in options.version:
            if not options.securityName:
                raise Exception("You must specify securityName with SNMPv3")

            if options.privType:
                cmdLineArgs += ['-l', 'authPriv']
                cmdLineArgs += ['-x', options.privType]
                cmdLineArgs += ['-X', options.privPassword]
            elif options.authType:
                cmdLineArgs += ['-l', 'authNoPriv']
            else:
                cmdLineArgs += ['-l', 'noAuthNoPriv']

            if options.authType:
                cmdLineArgs += ['-a', options.authType]
                cmdLineArgs += ['-A', options.authPassword]

            cmdLineArgs += ['-u', options.securityName]

        self._proxy = AgentProxy(
            ip=options.host,
            port=int(options.port),
            timeout=options.timeout,
            snmpVersion=options.version,
            community=options.community,
            cmdLineArgs=cmdLineArgs,
            protocol=None,
            allowCache=False)

        self._proxy.open()

    def get(self, oids):
        """
        SNMP get the given oids. Call callback with result.
        """
        if isinstance(oids, basestring):
            oids = [oids]

        d = self._proxy.get(oids)
        d.addBoth(self._cleanup)

        reactor.run()

        if isinstance(self._result, Failure):
            raise self._result.value

        return self._result

    def walk(self, base_oids):
        """
        SNMP walk from the given base OIDs. Call callback with result.
        """
        if isinstance(base_oids, basestring):
            base_oids = [base_oids]

        d = self._proxy.getTable(base_oids, maxRepetitions=1, limit=sys.maxint)
        d.addBoth(self._cleanup)

        reactor.run()

        if isinstance(self._result, Failure):
            raise self._result.value

        return self._result

    def _cleanup(self, result):
        self._result = result
        self._proxy.close()
        reactor.stop()