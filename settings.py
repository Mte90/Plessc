#!/usr/bin/env python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os

from ui_settings import Ui_Dialog

class SettingDialog ( QDialog , Ui_Dialog):

    def __init__ ( self, parent = None ):
        QDialog.__init__( self, parent )
        self.ui = Ui_Dialog()
        self.ui.setupUi( self )
