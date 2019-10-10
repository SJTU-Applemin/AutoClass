import sys
import re
from functools import partial

from PySide2.QtCore import QCoreApplication, Slot, Qt, QRegExp
from PySide2.QtWidgets import *
from PySide2.QtGui import QColor, QKeySequence, QValidator, QRegExpValidator

from PySide2 import QtCore, QtGui, QtWidgets
from MainWindow import Ui_MainWindow
from generate import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.Content = ClassContent()
        #self.testName = ''
        #self.InputPara = []
        #self.OutputPara = []
        self.basic_type = {'int', 'bool', 'dword', 'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t', 'char'}



        self.ui.pushButtonGenerate.clicked.connect(self.check_read_generate)
        self.ui.lineEditTestName.textChanged.connect(partial(self.changebg,'TestName'))
        self.ui.lineEditInputPara.textChanged.connect(partial(self.changebg,'InputPara'))
        self.ui.lineEditOutputPara.textChanged.connect(partial(self.changebg,'OutputPara'))


        self.ui.lineEditTestName.editingFinished.connect(self.checkTestName)
        self.ui.lineEditInputPara.editingFinished.connect(partial(self.fillLine,'InputPara'))
        self.ui.lineEditOutputPara.editingFinished.connect(partial(self.fillLine,'OutputPara'))

    @Slot()
    def changebg(self,name,text):
        if name == 'TestName':
            self.ui.lineEditTestName.setStyleSheet('QLineEdit {background-color: rgb(255, 255, 0);}')
        if name == 'InputPara':
            self.ui.lineEditInputPara.setStyleSheet('QLineEdit {background-color: rgb(255, 255, 0);}')
        if name == 'OutputPara':
            self.ui.lineEditOutputPara.setStyleSheet('QLineEdit {background-color: rgb(255, 255, 0);}')

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
            self.Content.clear()
            self.readInfoFromUi()
            self.Content.generate()
            

    def readInfoFromUi(self):

        self.Content.TestName=self.ui.lineEditTestName.text().strip() + 'Test'

        inputPara = self.ui.lineEditInputPara.text().strip()
        inputPara = inputPara.split(',')
        for input in inputPara:
            if not input:
                continue
            self.Content.InputPara.append(input.strip())

        outputPara = self.ui.lineEditOutputPara.text().strip()
        outputPara = outputPara.split(',')
        for output in outputPara:
            if not output:
                continue
            self.Content.OutputPara.append(output.strip())

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
            if input.startswith('const'):
                input = input[len('const'):].strip()
            if input.startswith('volatile'):
                input = input[len('volatile'):].strip()
            if input.startswith('restrict'):
                input = input[len('restrict'):].strip()
            input = input.strip().split(' ')
            para = input[-1]
            if not self.isValidPara(para):
                msgBox.setText("Please input valid Input Para!\n e.g. \" int num, char ch \"")
                msgBox.exec_()
                return False

        outputPara = self.ui.lineEditOutputPara.text().strip()
        outputPara = outputPara.split(',')
        for output in outputPara:
            if not output:
                continue
            if output.startswith('const'):
                output = output[len('const'):].strip()
            if output.startswith('volatile'):
                output = output[len('volatile'):].strip()
            if output.startswith('restrict'):
                output = output[len('restrict'):].strip()
            output = output.strip().split(' ')
            para = output[-1]
            if not self.isValidPara(para):
                msgBox.setText("Please input valid Output Para!\n e.g \" int num, char ch\".")
                msgBox.exec_()
                return False
        return True




    @Slot()
    def checkTestName(self):
        # remove white space at start and end
        text = self.ui.lineEditTestName.text().strip()
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

