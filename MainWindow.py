﻿# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MainWindow.ui',
# licensing of '.\MainWindow.ui' applies.
#
# Created: Mon Oct 21 11:19:04 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(744, 555)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(30)
        sizePolicy.setVerticalStretch(38)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(500, 1))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tabWidget.setObjectName("tabWidget")
        self.main = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main.sizePolicy().hasHeightForWidth())
        self.main.setSizePolicy(sizePolicy)
        self.main.setObjectName("main")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.main)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(10)
        self.gridLayout.setContentsMargins(10, -1, 10, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditFile = QtWidgets.QLineEdit(self.main)
        self.lineEditFile.setObjectName("lineEditFile")
        self.gridLayout.addWidget(self.lineEditFile, 0, 1, 1, 1)
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
        self.gridLayout.addWidget(self.pushButtonGenerate, 8, 1, 1, 1)
        self.comboBoxFunction = QtWidgets.QComboBox(self.main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFunction.sizePolicy().hasHeightForWidth())
        self.comboBoxFunction.setSizePolicy(sizePolicy)
        self.comboBoxFunction.setObjectName("comboBoxFunction")
        self.gridLayout.addWidget(self.comboBoxFunction, 2, 1, 1, 1)
        self.lineEditTestName = QtWidgets.QLineEdit(self.main)
        self.lineEditTestName.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEditTestName.setObjectName("lineEditTestName")
        self.gridLayout.addWidget(self.lineEditTestName, 3, 1, 1, 1)
        self.lineEditOutputPara = QtWidgets.QLineEdit(self.main)
        self.lineEditOutputPara.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEditOutputPara.setObjectName("lineEditOutputPara")
        self.gridLayout.addWidget(self.lineEditOutputPara, 6, 1, 1, 1)
        self.comboBoxClass = QtWidgets.QComboBox(self.main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxClass.sizePolicy().hasHeightForWidth())
        self.comboBoxClass.setSizePolicy(sizePolicy)
        self.comboBoxClass.setObjectName("comboBoxClass")
        self.gridLayout.addWidget(self.comboBoxClass, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.main)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.lineEditInputPara = QtWidgets.QLineEdit(self.main)
        self.lineEditInputPara.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEditInputPara.setObjectName("lineEditInputPara")
        self.gridLayout.addWidget(self.lineEditInputPara, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.main)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.main)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.main)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.main)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.pushButtonSelectFile = QtWidgets.QPushButton(self.main)
        self.pushButtonSelectFile.setObjectName("pushButtonSelectFile")
        self.gridLayout.addWidget(self.pushButtonSelectFile, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.main)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.main)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)
        self.comboBoxReturnValue = QtWidgets.QComboBox(self.main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxReturnValue.sizePolicy().hasHeightForWidth())
        self.comboBoxReturnValue.setSizePolicy(sizePolicy)
        self.comboBoxReturnValue.setObjectName("comboBoxReturnValue")
        self.gridLayout.addWidget(self.comboBoxReturnValue, 7, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 5)
        self.gridLayout.setColumnStretch(2, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.tabWidget.addTab(self.main, "")
        self.widget = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.tabWidget.addTab(self.widget, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 10)
        self.gridLayout_2.setColumnStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 744, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.pushButtonGenerate.setText(QtWidgets.QApplication.translate("MainWindow", "generate", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Testname", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Input para", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Output para", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("MainWindow", "File Location", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("MainWindow", "Test Class", None, -1))
        self.pushButtonSelectFile.setText(QtWidgets.QApplication.translate("MainWindow", "Select File", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "Test Function", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("MainWindow", "Return Value", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main), QtWidgets.QApplication.translate("MainWindow", "Tab 1", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), QtWidgets.QApplication.translate("MainWindow", "Tab 2", None, -1))

