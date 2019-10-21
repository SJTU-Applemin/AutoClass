import sys
import re
import os
from functools import partial

from PySide2.QtCore import QCoreApplication, Slot, Qt, QRegExp
from PySide2.QtWidgets import *
from PySide2.QtGui import QColor, QKeySequence, QValidator, QRegExpValidator

from PySide2 import QtCore, QtGui, QtWidgets
from MainWindow import Ui_MainWindow
from generate import *

import read_file


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.parser = None
        self.Content = ClassContent()
        self.fileContents = []
        self.classes = []
        self.functions = {}
        self.typeDescriptor = ['signed', 'unsigned', 'short', 'long']
        self.descriptor = ['auto', 'register', 'static', 'extern', 'thread_local', 'mutable']
        self.qualifier = ['const', 'restrict', 'volatile']
        #self.testName = ''
        #self.InputPara = []
        #self.OutputPara = [] bool dword char
        self.char_type = {'char', 'wchar_t'}
        self.int_type = {'int', 'uint8_t','int8_t' , 'uint16_t', 'int16_t', 'uint32_t', 'int32_t', 'uint64_t', 'int64_t'}
        self.float_type = {'float32', 'float64', 'float', 'double'}
        self.container = {'string', 'vector', 'deque', 'list', 'forward_list', 'queue', 'priority_queue', 'stack'}
        


        self.ui.pushButtonGenerate.clicked.connect(self.check_read_generate)
        self.ui.lineEditTestName.textChanged.connect(partial(self.changebg,'TestName'))
        self.ui.lineEditInputPara.textChanged.connect(partial(self.changebg,'InputPara'))
        self.ui.lineEditOutputPara.textChanged.connect(partial(self.changebg,'OutputPara'))

        self.ui.comboBoxClass.currentTextChanged.connect(self.fillFunctionSelect)
        self.ui.pushButtonSelectFile.clicked.connect(self.selectFilePath)
        self.ui.lineEditTestName.editingFinished.connect(self.checkTestName)
        self.ui.lineEditInputPara.editingFinished.connect(partial(self.fillLine,'InputPara'))
        self.ui.lineEditOutputPara.editingFinished.connect(partial(self.fillLine,'OutputPara'))
        self.ui.lineEditFile.editingFinished.connect(self.readHFile)

    @Slot()
    def changebg(self,name,text):
        if name == 'TestName':
            self.ui.lineEditTestName.setStyleSheet('QLineEdit {background-color: rgb(255, 255, 0);}')
        if name == 'InputPara':
            self.ui.lineEditInputPara.setStyleSheet('QLineEdit {background-color: rgb(255, 255, 0);}')
        if name == 'OutputPara':
            self.ui.lineEditOutputPara.setStyleSheet('QLineEdit {background-color: rgb(255, 255, 0);}')

    def clearComboboxSelect(self):
        self.classes = []
        self.functions = {}
        self.ui.comboBoxClass.clear()
        self.ui.comboBoxFunction.clear()

    def fillClassSelect(self):
        self.classes = self.parser.className
        self.ui.comboBoxClass.clear()
        for item in self.classes:
            self.ui.comboBoxClass.addItem(item)

    def fillFunctionSelect(self):
        self.ui.comboBoxFunction.clear()
        className = self.ui.comboBoxClass.currentText()
        if not className or className not in self.parser.className:
            return
        for item in self.parser.functions_of_class[className]:
            self.ui.comboBoxFunction.addItem(item)

    @Slot()
    def selectFilePath(self):
        fileName = QFileDialog.getOpenFileName(self, r'选择.h文件', filter='All files (*.h)')[0]
        if not fileName:
            return
        self.ui.lineEditFile.setText(fileName)
        self.readHFile()

    def readHFile(self):
        self.clearComboboxSelect()
        fileName = self.ui.lineEditFile.text()
        if not fileName.strip():
            return
        if not os.path.exists(fileName):
            self.ui.lineEditFile.clear()
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Error')
            msgBox.setInformativeText('File does not exists!')
            msgBox.exec_()
            return
        self.parser = read_file.read_h_file(fileName)
        self.Content.parser = self.parser
        self.Content.sourceFile = os.path.basename(fileName)
        mediaPath = fileName[:fileName.find('media')]
        self.Content.workspace = os.path.join(fileName[:fileName.find('media')], 'media\\media_embargo\\media_driver_next\\ult\\windows\\codec\\test')
        self.fillClassSelect()

    @Slot()
    def fillLine(self, name, flag = True):
        if name == 'TestName':
            pass
        if name == 'InputPara':
            pass
        if name == 'OutputPara':
            pass

    @Slot()
    def check_read_generate(self):
        blank = []
        if False == self.checkMainPageInput():
            return
        if not self.ui.lineEditTestName.text():
            self.ui.lineEditTestName.setStyleSheet('QLineEdit {background-color: rgb(255, 242, 0);}')
            blank.append('TestName')

        if not self.ui.lineEditInputPara.text():
            self.ui.lineEditInputPara.setStyleSheet('QLineEdit {background-color: rgb(255, 242, 0);}')
            blank.append('InputPara')

        if not self.ui.lineEditOutputPara.text():
            self.ui.lineEditOutputPara.setStyleSheet('QLineEdit {background-color: rgb(255, 242, 0);}')
            blank.append('OutputPara')

        if blank:
            msgBox = QQMessageBox()
            str = ','.join(blank)
            msgBox.setText("Please fill %s" % str)
            msgBox.exec_()
        else:
            self.Content.className = self.ui.comboBoxClass.currentText()
            self.Content.functionName = self.ui.comboBoxFunction.currentText()
            self.Content.clear()
            self.readInfoFromUi()
            self.Content.generateTestDataH()
            self.Content.generateInput()
            self.Content.generateReference()
            self.Content.generateTestCaseCpp()
            self.Content.generateTestCaseH()
            self.Content.generateTestH()
            self.Content.generateTestCpp()
            self.Content.generateResourceH()
            self.Content.generateMediaDriverCodecUlt()
            self.Content.generateUltSrcsCmake()

    def readInfoFromUi(self):

        self.Content.TestName=self.ui.lineEditTestName.text().strip() + 'TestData'

        inputPara = self.ui.lineEditInputPara.text().strip()
        inputPara = inputPara.split(',')    # if string contains ',' may cause error
        for input in inputPara:
            if not input.strip():
                continue
            input = input.split('=')    # if string contains '=', may cause error
            if len(input) == 2:
                value = input[1].strip()
            else:
                value = None
            self.Content.inputValue.append(value)
            input = input[0].strip()
            self.Content.inputPara.append(input)
            input = self.skipDescripter(input)
            input = self.skipQualifier(input)
            format = input.split(' ')[0].strip('*').strip('&')
            self.Content.inputType.append(format)

            name = input.split(' ')[-1].strip('*').strip('&')
            self.Content.inputName.append(name)
            #if format in self.int_type:
            #    self.Content.inputType.append('int_type')
            #elif format == 'bool':
            #    self.Content.inputType.append('bool')
            #elif format in self.float_type:
            #    self.Content.inputType.append('float')
            #elif format in self.char_type:
            #    self.Content.inputType.append('char')
            #else:
            #    self.Content.inputType.append('selfDefined')
            #self.Content.inputType.append()

        outputPara = self.ui.lineEditOutputPara.text().strip()
        outputPara = outputPara.split(',')
        for output in outputPara:
            output = output.strip(' ')
            if not output:
                continue
            self.Content.outputPara.append(output)
            output = self.skipDescripter(output)
            output = self.skipQualifier(output)
            format = output.split(' ')[0].strip('*').strip('&')
            self.Content.outputType.append(format)

            #self.Content.outputType.append()

    def generateClass(self):
        pass


    def isValidPara(self, text):
        if not text:
            return False
        else:
            if re.match(r'[0-9]',text):
                return False
            if text.startswith('**'):
                text = text[len('**'):]
            if text.startswith('*'):
                text = text[len('*'):]
            if text.startswith('&'):
                text = text[len('&'):]
            #if text.startswith(r'[0-9]'):
             #   return False
            words = text.split('_')
            for word in words:
                if not word:
                    continue
                elif word.isalpha() or word.isalnum():
                    continue
                else: 
                    return False
            return True


    def checkMainPageInput(self):
        msgBox = QMessageBox()
        if not self.ui.lineEditTestName.text().strip():
            msgBox.setText("Please input a valid Test Name!")
            msgBox.exec_()
            return False

        inputPara = self.ui.lineEditInputPara.text().strip()
        inputPara = inputPara.split(',')
        for input in inputPara:
            if not input:
                continue
            input = input.strip()

            #if input.startswith('const'):
            #    input = input[len('const'):].strip()
            #if input.startswith('volatile'):
            #    input = input[len('volatile'):].strip()
            #if input.startswith('restrict'):
            #    input = input[len('restrict'):].strip()
            input = self.skipDescripter(input)
            input = self.skipQualifier(input)
            if input.find('=') >= 0:
                input = input[:input.find('=')]
                # TODO: check value
                value = input[input.find('='):]
            input = input.strip().split(' ')
            para = input[-1]
            if not self.isValidPara(para):
                msgBox.setText("Please input valid Input Para!\n e.g. \" int num = 2, char ch = 'a' \"")
                msgBox.exec_()
                return False
        outputPara = self.ui.lineEditOutputPara.text().strip()
        outputPara = outputPara.split(',')
        for output in outputPara:
            if not output:
                continue
            output = output.strip()
            #if output.startswith('const'):
            #    output = output[len('const'):].strip()
            #if output.startswith('volatile'):
            #    output = output[len('volatile'):].strip()
            #if output.startswith('restrict'):
            #    output = output[len('restrict'):].strip()
            output = self.skipDescripter(output)
            output = self.skipQualifier(output)
            output = output.strip().split(' ')
            para = output[-1]
            if not self.isValidPara(para):
                msgBox.setText("Please input valid Output Para!\n e.g \" int num, char ch\".")
                msgBox.exec_()
                return False
        return True

    def skipDescripter(self,Edit):
        for d in self.descriptor:
            if Edit.startswith(d):
                Edit = Edit[len(d):].strip()
        return Edit


    def skipQualifier(self, Edit):
        for q in self.qualifier:
            if Edit.startswith(q):
                Edit = Edit[len(q):].strip()
        return Edit
        #if Edit.startswith('const'):
        #    Edit = Edit[len('const'):].strip()
        #if Edit.startswith('volatile'):
        #    Edit = Edit[len('volatile'):].strip()
        #if Edit.startswith('restrict'):
        #    Edit = Edit[len('restrict'):].strip()

    #def parseType(self,format):
    #    if format in self.int_type:
    #        return 'int'
    #    elif format in self.float_type:
    #        return 'float'
    #    elif format in self.char_type:
    #        return 'char'
    #    elif format == 'bool':
    #        return 'bool'
    #    else:
    #        for item in self.container:
    #            if item in format:
    #                return 'container'
    #    return 'selfDefined'




    @Slot()
    def checkTestName(self):
        # remove white space at start and end
        text = self.ui.lineEditTestName.text().strip()
        if not text:
            return
        # pure white space should not be detected as input
        #if not text:
        #    return
        ## test name should only contain _, number, letter
        #words = text.split('_')
        #for word in words:
        #    # ignore \n
        #    if not word:
        #        continue
        #    elif word.isalpha() or word.isalnum():
        #        continuef
        #    else:
        if not self.isValidPara(text):
            msgBox = QMessageBox()
            msgBox.setText("Test Name contains invalid character!")
            msgBox.exec_()
            self.ui.lineEditTestName.clear()
                #break




if __name__ == '__main__':
    app= QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    mainWindow.activateWindow()
    sys.exit(app.exec_())

#if __name__ == "__main__":
#    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = Ui_MainWindow()
#    ui.setupUi(MainWindow)
#    MainWindow.show()
#    sys.exit(app.exec_())

