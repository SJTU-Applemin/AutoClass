# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MainWindow.ui',
# licensing of '.\MainWindow.ui' applies.
#
# Created: Thu Sep 26 10:36:57 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(744, 555)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(30)
        sizePolicy.setVerticalStretch(38)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(500, 1))
        self.tabWidget.setMaximumSize(QtCore.QSize(501, 16777215))
        self.tabWidget.setObjectName("tabWidget")
        self.main = QtWidgets.QWidget()
        self.main.setObjectName("main")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.main)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(10)
        self.gridLayout.setContentsMargins(10, -1, 10, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.main)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lineEditTestName = QtWidgets.QLineEdit(self.main)
        self.lineEditTestName.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEditTestName.setObjectName("lineEditTestName")
        self.gridLayout.addWidget(self.lineEditTestName, 0, 1, 1, 1)
        self.lineEditInputPara = QtWidgets.QLineEdit(self.main)
        self.lineEditInputPara.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEditInputPara.setObjectName("lineEditInputPara")
        self.gridLayout.addWidget(self.lineEditInputPara, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.main)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.lineEditOutputPara = QtWidgets.QLineEdit(self.main)
        self.lineEditOutputPara.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEditOutputPara.setObjectName("lineEditOutputPara")
        self.gridLayout.addWidget(self.lineEditOutputPara, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.main)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.pushButtonGenerate = QtWidgets.QPushButton(self.main)
        self.pushButtonGenerate.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonGenerate.sizePolicy().hasHeightForWidth())
        self.pushButtonGenerate.setSizePolicy(sizePolicy)
        self.pushButtonGenerate.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButtonGenerate.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButtonGenerate.setObjectName("pushButtonGenerate")
        self.gridLayout.addWidget(self.pushButtonGenerate, 4, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.tabWidget.addTab(self.main, "")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.tabWidget.addTab(self.widget, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 744, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Input para", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Output para", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Testname", None, -1))
        self.pushButtonGenerate.setText(QtWidgets.QApplication.translate("MainWindow", "generate", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main), QtWidgets.QApplication.translate("MainWindow", "Tab 1", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), QtWidgets.QApplication.translate("MainWindow", "Tab 2", None, -1))


#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = Ui_MainWindow()
#    ui.setupUi(MainWindow)
#    MainWindow.show()
#    sys.exit(app.exec_())
