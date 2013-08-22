#!/usr/bin/python3
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os

from ui_settings import Ui_Settings

class SettingDialog ( QDialog , Ui_Settings):

	#var initialization
	settings = QSettings('Mte90','Plessc')
	settings.setFallbacksEnabled(False)

	def __init__ ( self, parent = None ):
		QDialog.__init__( self, parent )
		self.ui = Ui_Settings()
		self.ui.setupUi( self )
		self.ui.chooseLessc.clicked.connect(self.openLesscDialog)
		self.ui.chooseEditor.clicked.connect(self.openEditorDialog)
		self.ui.buttonBox.accepted.connect(self.saveSetting)
		#lessc path
		if self.settings.contains('lessc_path') == 'False' or len(self.ui.lesscPath.text()) == 0:
			self.settings.setValue('less_path','/usr/bin/lessc')
		#editor path
		if self.settings.contains('editor_path') == 'False':
			self.settings.setValue('editor_path','/usr/bin/kate')
		#checkbox for open all file in less file folder
		if self.settings.contains('less_folder') == 'False' or len(self.ui.editor.text()) == 0:
			self.settings.setValue('less_folder','False')
		if self.settings.value('less_folder') == 'False':
			self.ui.lessFolder.setChecked(False)
		else:
			self.ui.lessFolder.setChecked(True)

		self.ui.editor.setText(self.settings.value('editor_path'))
		self.ui.lesscPath.setText(self.settings.value('less_path'))
	
	#Function for open a dialog for choose the less compiler
	def openLesscDialog(self):
		lessc = QFileDialog.getOpenFileName(self, 'Choose less compiler',self.ui.lesscPath.text())
		self.ui.lesscPath.setText(self.lessc)
	
	#Function for open a dialog for choose the editor
	def openEditorDialog(self):
		editor = QFileDialog.getSaveFileName(self, 'Set editor',self.ui.editor.text())
		self.ui.editor.setText(editor)

	#Save the setting
	def saveSetting(self):
		if len(self.ui.editor.text()) > 0:
			self.settings.setValue('editor_path',self.ui.editor.text())
		else:
			self.ui.editor.setText('/usr/bin/kate')
			QMessageBox.critical(self.window(), "Editor empty","This field can't be empty!")
			
		if len(self.ui.lesscPath.text()) > 0:
			self.settings.setValue('less_path',self.ui.lesscPath.text())
		else:
			self.ui.lesscPath.setText('/usr/bin/lessc')
			QMessageBox.critical(self.window(), "Compiler empty","This field can't be empty!")
		
		if self.ui.lessFolder.isChecked() == False:
			self.settings.setValue('less_folder','False')
		else:
			self.settings.setValue('less_folder','True')