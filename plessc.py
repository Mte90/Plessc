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
    version = 'v 1.1'
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
        #Connect the function with the signal
        self.ui.inputChoose.clicked.connect(self.openInputDialog)
        self.ui.outputChoose.clicked.connect(self.openOutputDialog)
        self.ui.setBoth.pressed.connect(self.setBoth)
        self.ui.setStandard.pressed.connect(self.setStandard)
        self.ui.optionIE.stateChanged.connect(self.setOptionIE)
        self.ui.optionSourceMap.stateChanged.connect(self.setOptionSourceMap)
        self.ui.setMinify.stateChanged.connect(self.setMinify)
        self.ui.inputEdit.pressed.connect(self.openEditor)
        self.ui.outputLog.clicked.connect(self.openLog)
        self.ui.lint.clicked.connect(self.lintLog)
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
        self.loadVersion()
        #Check the setting for load the path of the file
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
        #Check the setting for the minify mode for the css file
        if self.settings.value('min') == 'False':
            self.option['minify'] = ' ';
            self.settings.setValue('min','False')
            self.ui.setMinify.setChecked(False)
        else:
            self.option['minify'] = '-x'
            self.settings.setValue('min','True')
            self.ui.setMinify.setChecked(True)
        #Check for the export of the file
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
        #Add the function for the autocompile after the load of the setting
        self.ui.autoCompile.stateChanged.connect(self.autoCompile)
        self.autoCompile()
        #Setting for export the css for old IE version
        if self.settings.value('option_IE') == 'False':
            self.ui.optionIE.setChecked(False)
            self.option['ie'] = ' '
        else:
            self.ui.optionIE.setChecked(True)
            self.option['ie'] = '--no-ie-compat'
        #Setting for enable Sourcemap
        if self.settings.value('option_SourceMap') == 'False':
            self.ui.optionSourceMap.setChecked(False)
            self.option['sourcemap'] = ' '
        else:
            self.ui.optionSourceMap.setChecked(True)
            self.option['sourcemap'] = '--source-map'
        #Resize the window for hide the space of log
        self.resize(505,220)
        self.show()
    
    #Function for open a dialog for choose the input less file
    def openInputDialog(self):
        self.input_less = QFileDialog.getOpenFileName(self, 'Choose less file',self.ui.inputFile.text(),'LESS file (*.less)')
        if self.input_less != '':
             self.ui.inputFile.setText(self.input_less)
    
    #Function for open a dialog for choose the output css file
    def openOutputDialog(self):
        self.output_css = QFileDialog.getSaveFileName(self, 'Set css file',self.ui.outputFile.text(),'CSS file (*.css)')
        if self.output_css != '':
             self.ui.outputFile.setText(self.output_css)
    
    #Save the input file in the setting
    def setInputFile(self):
        self.settings.setValue('input_file',self.ui.inputFile.text())
    
    #Save the output file in the setting
    def setOutputFile(self):
        self.settings.setValue('output_file',self.ui.outputFile.text())
    
    #Save the output export of the css
    def setBoth(self):
        self.settings.setValue('both_or_standard','True')
    
    #Save the output export of the css
    def setStandard(self):
        self.settings.setValue('both_or_standard','False')
    
    #Check autoCompile and enable the watching of the input less file
    def autoCompile(self):
        #If not checked
        if self.ui.autoCompile.isChecked() == False:
            self.settings.setValue('auto_compile','False')
            #If previosuly was enabled the option this disable the watch of the file
            try:
                self.watcher.fileChanged.disconnect()
            except (RuntimeError, TypeError, NameError):
                pass
        else:
            self.settings.setValue('auto_compile','True')
            #Clean the path added to file watching for fix a problem with Qt4
            self.watcher.removePath(self.settings.value('input_file'))
            #Re add of the path
            self.watcher.addPath(self.settings.value('input_file'))
            self.watcher.fileChanged.connect(self.compileIt)
    
    #Save the Ie Setting
    def setOptionIE(self):
        if self.ui.optionIE.isChecked() == False:
            self.settings.setValue('option_IE','False')
            self.option['ie'] = ''
        else:
            self.settings.setValue('option_IE','True')
            self.option['ie'] = '--no-ie-compat'
    
    #Save the SourceMap
    def setOptionSourceMap(self):
        if self.ui.optionSourceMap.isChecked() == False:
            self.settings.setValue('option_SourceMap','False')
            self.option['sourcemap'] = ' '
        else:
            self.settings.setValue('option_SourceMap','True')
            self.option['sourcemap'] = '--source-map'
            
    #Save the minify setting
    def setMinify(self):
        if self.ui.setMinify.isChecked() == False:
            self.option['minify'] = ' '
            self.settings.setValue('min','False')
        else:
            self.option['minify'] = '-x'
            self.settings.setValue('min','True')
    
    #Compile the less file
    def compileIt(self):
        if os.path.isfile(self.settings.value('input_file')):
            self.ui.log.setHtml('')
            self.ui.info.setText('Compiling...')
            if self.settings.value('both_or_standard') == 'True':
                #if both save method True
                name = os.path.splitext(self.settings.value('output_file'))[0]
                name += '.min.css'
                complete = str(self.settings.value('less_path') + self.optionString() + '"' + self.settings.value('input_file') + '" "' + name + '"' )
                command = str(self.settings.value('less_path') + self.optionString() + ' --verbose "' + self.settings.value('input_file') + '" "' + self.settings.value('output_file') + '"')
                #Compile the min.css
                os.system(complete)
                self.proc.closeWriteChannel()
                #Compile a standard css
                self.proc.start(command)
                self.proc.waitForFinished()
                self.proc.closeWriteChannel()
                if os.path.isfile(name):
                    self.ui.info.setText('File Min Output: <b>' + self.sizeof_fmt(name) + '</b> | File Standard: <b>' + self.sizeof_fmt(self.settings.value('output_file')) + '</b> | ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                else:
                    QMessageBox.critical(self.window(), "Output File not exist","The output file choosen not exist!")
            else:
                #if standard = 0 False
                command = str(self.settings.value('less_path') + self.optionString() + ' --verbose "' + self.settings.value('input_file') + '" "' + self.settings.value('output_file') + '"' )
                self.proc.closeWriteChannel()
                self.proc.start(command)
                self.proc.waitForFinished()
                self.proc.closeWriteChannel()
                if os.path.isfile(self.settings.value('output_file')):
                    self.ui.info.setText('File Output: <b>' + self.sizeof_fmt(self.settings.value('output_file')) + '</b>' + ' | ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                else:
                    QMessageBox.critical(self.window(), "Output File not exist","The output file choosen not exist!")
        else:
            QMessageBox.critical(self.window(), "Input File not exist","The input file choosen not exist!")
        print(command)
        #Clean the path added to file watching for fix a problem with Qt4
        self.watcher.removePath(self.settings.value('input_file'))
        #Readd the path
        self.watcher.addPath(self.settings.value('input_file'))
    
    #Open all the less file in the folder onf the input file
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
    
    #Show the log
    def openLog(self):
        if self.ui.log.isVisible() == True:
            self.resize(523,239)
            self.ui.log.hide()
        else:
            self.resize(523,459)
            self.ui.log.show()

    def openSetDialog(self):
        #i need to explain this??
        window = QDialog()
        ui = SettingDialog()
        ui.setupUi(window)
        if ui.exec_() == 1:
            self.loadVersion()

    def openInfo(self):
        QMessageBox.about(self.window(), "About Plessc","<p align='center'>Plessc " + self.version + " <br><br>By <a href='http://www.mte90.net'><b>Mte90</b></a><br><br>GUI in Python and Qt4 for compile less file<br><br>Tested with lessc 1.4.x of LESS.JS<br><br><small>If other compiler use the same parameters i think that works else some monkeys do it for you</small><br><br>License: GPL 3</p>")

    #http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    def sizeof_fmt(self,file_):
        num = os.path.getsize(str(file_))
        for x in ['bytes','KB','MB','GB','TB']:
            if num < 1024.0:
                return str("%3.1f %s") % (num, x)
            num /= 1024.0
    
    #Clean the output of lessc 
    def replace_all(self,text):
        #remove the shellcode/ANSI of the color of the text
        text = text.replace('[39m', '<br>').replace('[31m', '').replace('[22m', '').replace('[0m', '').replace('1b', '')
        text = text.replace('[90m', '').replace('[27m', '').replace('[7m', '').replace('[1m', '').replace("b''",'').replace('\n\n','').replace('b\'','')
        text = text.replace('\\x', '').replace('\\n\\n\'', '').replace('\\n', '')
        
        return text.lstrip()
        
    #Execeute the lint and show it in the log area
    def lintLog(self):
        self.proc.closeWriteChannel()
        self.proc.start(str(self.settings.value('less_path') + ' --lint "' + self.settings.value('input_file') + '"'))
        self.openLog()
        self.proc.closeWriteChannel()
    
    #Check the content of log
    def checkLog(self):
        stdout = str(self.proc.readAllStandardOutput())
        check = stdout.strip()
        #If the log not exmpty and length > of 3 print
        if(check is not None and len(check) > 3):
            output = self.replace_all(stdout)
            if not output.startswith('lessc: wrote '):
                self.ui.log.setHtml(self.replace_all(stdout))
                self.openLog()
        else:
            self.ui.log.setHtml('OK!')
    
    #Execute the load of lessc version
    def loadVersion(self):
        self.less_version.closeWriteChannel()
        self.setWindowTitle('PLessc - lessc not defined')
        self.less_version.start(self.settings.value('less_path'),['--version'])
        
    #Update the title with less version
    def updateTitle(self):
        stdout = str(self.less_version.readAllStandardOutput())
        self.setWindowTitle('PLessc - ' + self.replace_all(stdout.rstrip('\'')))
    
    #Concate all the settings for lessc for use it in the command
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