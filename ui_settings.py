# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/mte90/Desktop/Prog/Plessc/settings.ui'
#
# Created: Wed Feb  6 10:38:30 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.resize(400, 194)
        self.gridLayout = QtGui.QGridLayout(Settings)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(Settings)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lesscPath = QtGui.QLineEdit(self.groupBox)
        self.lesscPath.setObjectName(_fromUtf8("lesscPath"))
        self.gridLayout_3.addWidget(self.lesscPath, 0, 0, 1, 1)
        self.chooseLessc = QtGui.QPushButton(self.groupBox)
        self.chooseLessc.setObjectName(_fromUtf8("chooseLessc"))
        self.gridLayout_3.addWidget(self.chooseLessc, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Settings)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        self.editor = QtGui.QLineEdit(self.groupBox_2)
        self.editor.setObjectName(_fromUtf8("editor"))
        self.gridLayout_4.addWidget(self.editor, 0, 1, 1, 1)
        self.chooseEditor = QtGui.QPushButton(self.groupBox_2)
        self.chooseEditor.setObjectName(_fromUtf8("chooseEditor"))
        self.gridLayout_4.addWidget(self.chooseEditor, 0, 2, 1, 1)
        self.lessFolder = QtGui.QCheckBox(self.groupBox_2)
        self.lessFolder.setObjectName(_fromUtf8("lessFolder"))
        self.gridLayout_4.addWidget(self.lessFolder, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Settings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QtGui.QApplication.translate("Settings", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Settings", "Lessc Path", None, QtGui.QApplication.UnicodeUTF8))
        self.chooseLessc.setText(QtGui.QApplication.translate("Settings", "Choose", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Settings", "Editor config", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Settings", "Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.chooseEditor.setText(QtGui.QApplication.translate("Settings", "Choose", None, QtGui.QApplication.UnicodeUTF8))
        self.lessFolder.setText(QtGui.QApplication.translate("Settings", "Open all file less in folder", None, QtGui.QApplication.UnicodeUTF8))

