######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

import Globals
import os

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import zenPath


class ZenPack(ZenPackBase):
    """ CheckPointMonitor loader
    """
    
    def install(self, app):
        ZenPackBase.install(self, app)
        self.copyDependencies()
        self.symlinkPlugin()
        
    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self.copyDependencies()
        self.symlinkPlugin()
        
    def remove(self, app, leaveObjects=False):
        self.removePluginSymlink()
        ZenPackBase.remove(self, app, leaveObjects)
    
        
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
