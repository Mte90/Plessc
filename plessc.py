#!/usr/bin/python3
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, sys, signal, datetime

from ui_MainWindow import Ui_MainWindow
from settings import SettingDialog

class MainWindow ( QMainWindow , Ui_MainWindow):

	#var initialization
	settings = QSettings('Mte90','Plessc')
	settings.setFallbacksEnabled(False)
	version = 'V 1.0 Beta'
	input_less = ''
	output_css = ''
	mysize = ''
	option = {}
	proc = QProcess()
	less_version = QProcess()
	watcher = QFileSystemWatcher()

	def __init__ ( self, parent = None ):
		QMainWindow.__init__( self, parent )
		self.ui = Ui_MainWindow()
		self.ui.setupUi( self )
		self.setWindowTitle('PLessc - lessc not defined')
		#connect the function with the signal
		self.ui.inputChoose.clicked.connect(self.openInputDialog)
		self.ui.outputChoose.clicked.connect(self.openOutputDialog)
		self.ui.setMinify.pressed.connect(self.setMinify)
		self.ui.setYUI.pressed.connect(self.setYUICompress)
		self.ui.setBoth.pressed.connect(self.setBoth)
		self.ui.setStandard.pressed.connect(self.setStandard)
		self.ui.optionIE.stateChanged.connect(self.setOptionIE)
		self.ui.inputEdit.pressed.connect(self.openEditor)
		self.ui.outputLog.clicked.connect(self.openLog)
		self.ui.compile.clicked.connect(self.compileIt)
		self.ui.inputFile.textChanged.connect(self.setInputFile)
		self.ui.outputFile.textChanged.connect(self.setOutputFile)
		self.ui.menuInfo.triggered.connect(self.openInfo)
		self.ui.menuSetting.triggered.connect(self.openSetDialog)
		self.proc.finished.connect(self.checkLog)
		self.less_version.finished.connect(self.updateTitle)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		#hide log
		self.ui.log.hide()
		#check lessc version
		self.less_version.closeWriteChannel()
		self.less_version.start(self.settings.value('less_path'),['--version'])
		#check of the save option
		if self.settings.value('input_file') != -1:
			self.input_less = self.settings.value('input_file')
		else:
			self.input_less = '/'
		if self.settings.value('output_file') != -1:
			self.output_css = self.settings.value('output_file')
		else:
			self.output_css = '/'
		self.ui.inputFile.setText(self.input_less)
		self.ui.outputFile.setText(self.output_css)
		if self.settings.value('min_or_yui') == 'False':
			self.option['minify'] = '--yui-compress';
			self.settings.setValue('min_or_yui','False')
			self.ui.setYUI.toggle()
		else:
			self.option['minify'] = '-x'
			self.settings.setValue('min_or_yui','True')
			self.ui.setMinify.toggle()
		if self.settings.value('both_or_standard') == 'False':
			self.settings.setValue('both_or_standard','False')
			self.ui.setStandard.toggle()
		else:
			self.settings.setValue('both_or_standard','True')
			self.ui.setBoth.toggle()
		#Auto compile option
		if self.settings.value('auto_compile') == 'False':
			self.ui.autoCompile.setChecked(False)
		else:
			self.ui.autoCompile.setChecked(True)
		self.ui.autoCompile.stateChanged.connect(self.autoCompile)
		
		self.autoCompile()
		#Option IE 
		if self.settings.value('option_IE') == 'False':
			self.ui.optionIE.setChecked(False)
			self.option['ie'] = ' '
		else:
			self.ui.optionIE.setChecked(True)
			self.option['ie'] = '--no-ie-compat'
		#resize the window for hide the space of log
		self.resize(503,213)
		self.show()

	def openInputDialog(self):
		self.input_less = QFileDialog.getOpenFileName(self, 'Choose less file',self.ui.inputFile.text(),'LESS file (*.less)')
		if self.input_less != '':
			 self.ui.inputFile.setText(self.input_less)

	def openOutputDialog(self):
		self.output_css = QFileDialog.getSaveFileName(self, 'Set css file',self.ui.outputFile.text(),'CSS file (*.css)')
		if self.output_css != '':
			 self.ui.outputFile.setText(self.output_css)

	def setInputFile(self):
		self.settings.setValue('input_file',self.ui.inputFile.text())

	def setOutputFile(self):
		self.settings.setValue('output_file',self.ui.outputFile.text())

	def setMinify(self):
		self.option['minify'] = '-x'
		self.settings.setValue('min_or_yui','True')

	def setYUICompress(self):
		self.option['minify'] = '--yui-compress'
		self.settings.setValue('min_or_yui','False')

	def setBoth(self):
		self.settings.setValue('both_or_standard','True')

	def setStandard(self):
		self.settings.setValue('both_or_standard','False')
	
	def autoCompile(self):
		if self.ui.autoCompile.isChecked() == False:
			self.settings.setValue('auto_compile','False')
			try:
				self.watcher.fileChanged.disconnect()
			except (RuntimeError, TypeError, NameError):
				pass
			print(2)
		else:
			self.settings.setValue('auto_compile','True')
			self.watcher.addPath(self.settings.value('input_file'))
			self.watcher.fileChanged.connect(self.compileIt)
			print(1)
	
	def setOptionIE(self):
		if self.ui.optionIE.isChecked() == False:
			self.settings.setValue('option_IE','False')
			self.option['ie'] = ''
		else:
			self.settings.setValue('option_IE','True')
			self.option['ie'] = '--no-ie-compat'
	
	def compileIt(self):
		if os.path.isfile(self.settings.value('input_file')):
			self.ui.log.setHtml('')
			if self.settings.value('both_or_standard') == 'True':
				#if both save method True
				name = os.path.splitext(self.settings.value('output_file'))[0]
				self.ui.info.setText('Compiling...')
				name += '.min.css'
				complete = str(self.settings.value('less_path') + self.optionString() + '"' + self.settings.value('input_file') + '" "' + name + '"' )
				command = str(self.settings.value('less_path') + ' --verbose "' + self.settings.value('input_file') + '" "' + self.settings.value('output_file') + '"')
				os.system(complete)
				self.proc.closeWriteChannel()
				self.proc.start(command)
				self.ui.info.setText('File Min Output: ' + self.sizeof_fmt(name) + ' | File Standard: ' + self.sizeof_fmt(self.settings.value('output_file')) + ' | ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
			else:
				#if standard = 0 False
				self.ui.info.setText('Compiling...')
				command = str(self.settings.value('less_path') + self.optionString() + '"' + self.settings.value('input_file') + '" "' + self.settings.value('output_file') + '"' )
				self.proc.closeWriteChannel()
				self.proc.start(command)
				self.ui.info.setText('File Output: <b>' + self.sizeof_fmt(self.settings.value('output_file')) + '</b>' + ' | ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
		else:
			QMessageBox.critical(self.window(), "File input not exist","The file input choosen not exist!")
		print(command)

	def openEditor(self):
		open_file = self.settings.value('input_file')
		#get all file less and open on the editor if this option are set
		if self.settings.value('less_folder') == 'True':
			list_file = ''
			path_less = os.path.split(str(open_file))[0]
			for root, dirs, files in os.walk(path_less):
				files.sort()
				for name in files:
					filename = os.path.join(root, name)
					if filename.endswith('.less'):
						list_file = list_file + '"' + filename + '" '
			open_file = list_file
		os.system(str(self.settings.value('editor_path') + ' ' + open_file))

	def openLog(self):
		if self.ui.log.isVisible() == True:
			self.resize(503,213)
			self.ui.log.hide()
		else:
			self.resize(503,389)
			self.ui.log.show()

	def openSetDialog(self):
		#i need to explain this??
		window = QDialog()
		ui = SettingDialog()
		ui.setupUi(window)
		ui.exec_()

	def openInfo(self):
		QMessageBox.about(self.window(), "About Plessc","Plessc " + self.version + " <br><br>Software made by <a href='http://www.mte90.net'><b>Mte90</b></a><br><br><a href='https://github.com/Mte90/Plessc'>Official Site</a>")

	#http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
	def sizeof_fmt(self,file_):
		num = os.path.getsize(str(file_))
		for x in ['bytes','KB','MB','GB','TB']:
			if num < 1024.0:
				return str("%3.1f %s") % (num, x)
			num /= 1024.0

	def replace_all(self,text):
		#remove the shellcode of the color of the text
		text = text.replace('[39m', '<br>').replace('[31m', '').replace('[22m', '').replace('[0m', '').replace('1b', '')
		text = text.replace('[90m', '').replace('[27m', '').replace('[7m', '').replace('[1m', '').replace("b''",'').replace('\n\n','').replace('b\'','')
		text = text.replace('\\x', '').replace('\\n\\n\'', '').replace('\\n', '')
		
		return text.lstrip()
		
	def checkLog(self):
		stdout = str(self.proc.readAllStandardOutput())
		check = stdout.strip()
		if(check is not None and len(check) > 3):
			self.ui.log.setHtml(self.replace_all(stdout))
			self.openLog()
		else:
			self.ui.log.setHtml('OK!')
	
	def updateTitle(self):
		stdout = str(self.less_version.readAllStandardOutput())
		self.setWindowTitle('PLessc - ' + self.replace_all(stdout.rstrip('\'')))
		
	def optionString(self):
		string = ' '.join('{}'.format(val) for key, val in self.option.items())
		return ' ' + string + ' '
		
def main():
	app = QApplication(sys.argv)
	MainWindow_ = QMainWindow()
	ui = MainWindow()
	ui.setupUi(MainWindow_)
	sys.exit(app.exec_())

main()