##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, 2021, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import os


from Products.ZenUtils.Utils import zenPath
from ZenPacks.zenoss.ZenPackLib import zenpacklib


CFG = zenpacklib.load_yaml([os.path.join(os.path.dirname(__file__), "zenpack.yaml")], verbose=False, level=30)
schema = CFG.zenpack_module.schema


class ZenPack(schema.ZenPack):

    def install(self, app):
        super(ZenPack, self).install(self, app)
        self.copyDependencies()
        self.symlinkPlugin()
        
    def upgrade(self, app):
        super(ZenPack, self).upgrade(self, app)
        self.copyDependencies()
        self.symlinkPlugin()
        
    def remove(self, app, leaveObjects=False):
        self.removePluginSymlink()
        super(ZenPack, self).remove(self, app, leaveObjects)

        
    def copyDependencies(self):
        os.system("cp %s/EasySnmpPlugin.py %s/" % (
            self.path('libexec'), zenPath('libexec')))
    
    def symlinkPlugin(self):
        os.system('ln -sf %s/check_checkPointFwState.py %s/' % (
            self.path('libexec'), zenPath('libexec')))
        os.system('ln -sf %s/check_checkPointHaState.py %s/' % (
            self.path('libexec'), zenPath('libexec')))
        os.system('ln -sf %s/check_checkPointDtpsState.py %s/' % (
            self.path('libexec'), zenPath('libexec')))
            
    def removePluginSymlink(self):
        os.system('rm -f %s/check_checkPointFwState.py' % (
            zenPath('libexec')))
        os.system('rm -f %s/check_checkPointHaState.py' % (
            zenPath('libexec')))
        os.system('rm -f %s/check_checkPointDtpsState.py' % (
            zenPath('libexec')))
