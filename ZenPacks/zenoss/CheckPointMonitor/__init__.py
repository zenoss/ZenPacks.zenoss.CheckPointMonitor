##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, 2021, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################

import os
import logging

from Products.CMFCore.DirectoryView import registerDirectory
from Products.Zuul.facades.manufacturersfacade import ManufacturersFacade

from ZenPacks.zenoss.ZenPackLib import zenpacklib


CFG = zenpacklib.load_yaml([os.path.join(os.path.dirname(__file__), "zenpack.yaml")], verbose=False, level=30)
schema = CFG.zenpack_module.schema

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

log = logging.getLogger("zen.CheckPoint")


MANUFACTURER_NAME = 'Check Point'
MANUFACTURER_UID = '/zport/dmd/Manufacturers/Check Point'


class ZenPack(schema.ZenPack):

    def install(self, app):
        super(ZenPack, self).install(app)

        # create 'Check Point' manufacturer and its products if they don't exist yet
        manufacturers = app.dmd.Manufacturers
        if MANUFACTURER_NAME not in manufacturers:
            mFacade = ManufacturersFacade(manufacturers)
            mFacade.addManufacturer(MANUFACTURER_NAME)
            log.info('New manufacturer [{}] was added'.format(MANUFACTURER_NAME))

            mFacade.addNewProduct({
                'uid': MANUFACTURER_UID,
                'prodname': 'Gaia (2.6)',
                'prodkeys': 'Gaia (2.6)',
                'type': 'Operating System',
                'partno': '',
                'description': ''
            })

            mFacade.addNewProduct({
                'uid': MANUFACTURER_UID,
                'prodname': 'SecurePlatform (NGX R65)',
                'prodkeys': 'SecurePlatform (NGX R65)',
                'type': 'Hardware',
                'partno': '',
                'description': ''
            })
