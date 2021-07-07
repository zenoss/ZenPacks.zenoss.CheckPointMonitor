##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, 2021, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################

import os

from ZenPacks.zenoss.ZenPackLib import zenpacklib


CFG = zenpacklib.load_yaml([os.path.join(os.path.dirname(__file__), "zenpack.yaml")], verbose=False, level=30)
schema = CFG.zenpack_module.schema


class ZenPack(schema.ZenPack):

    def install(self, app):
        super(ZenPack, self).install(app)
        ## TODO move manufacturer from objects.xml
