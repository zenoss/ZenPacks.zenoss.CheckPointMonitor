#!/usr/bin/env python
##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################

#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2021, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
"""
Checks a Check Point firewall using SNMP to verify that the firewall module
currently has a policy installed.
"""

import sys
import optparse

import easysnmp


fwModuleStateOID = '.1.3.6.1.4.1.2620.1.1.1.0'


def main():
    agent = easysnmp.Agent()
    option_parser = optparse.OptionParser(option_list=agent.options)
    options = option_parser.parse_args()[0]

    agent.initialize(options)
    results = agent.get(fwModuleStateOID)
    state = results.get(fwModuleStateOID)


    if state is None:
        print("no firewall state returned")
        sys.exit(1)
    elif state == "Installed":
        print("firewall policy is installed")
        sys.exit(0)
    else:
        print("firewall policy is not installed")
        sys.exit(1)

if __name__ == '__main__':
    main()
