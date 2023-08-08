# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Vibration_analyzer(object):
    def setupUi(self, Vibration_analyzer):
        Vibration_analyzer.setObjectName("Vibration_analyzer")
        Vibration_analyzer.resize(800, 612)
        self.centralwidget = QtWidgets.QWidget(Vibration_analyzer)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(220, 50, 561, 481))
        self.graphicsView.setObjectName("graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox_port = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_port.setGeometry(QtCore.QRect(20, 40, 191, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_port.setFont(font)
        self.comboBox_port.setObjectName("comboBox_port")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.comboBox_baudrate = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_baudrate.setGeometry(QtCore.QRect(110, 80, 101, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_baudrate.setFont(font)
        self.comboBox_baudrate.setObjectName("comboBox_baudrate")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(20, 120, 191, 41))
        self.pushButton_start.setObjectName("pushButton_start")
        self.pushButton_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop.setGeometry(QtCore.QRect(20, 170, 191, 41))
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 230, 201, 311))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 210, 201, 20))
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(250, 20, 191, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(450, 20, 241, 20))
        self.label_5.setObjectName("label_5")
        self.lineEdit_peak_freq = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_peak_freq.setGeometry(QtCore.QRect(700, 20, 81, 25))
        self.lineEdit_peak_freq.setObjectName("lineEdit_peak_freq")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 550, 801, 20))
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.pushButton_refresh_port = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_refresh_port.setGeometry(QtCore.QRect(130, 10, 81, 29))
        self.pushButton_refresh_port.setObjectName("pushButton_refresh_port")
        Vibration_analyzer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Vibration_analyzer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp_H = QtWidgets.QMenu(self.menubar)
        self.menuHelp_H.setObjectName("menuHelp_H")
        Vibration_analyzer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Vibration_analyzer)
        self.statusbar.setObjectName("statusbar")
        Vibration_analyzer.setStatusBar(self.statusbar)
        self.actionAbout_Hardware_Connection = QtWidgets.QAction(Vibration_analyzer)
        self.actionAbout_Hardware_Connection.setObjectName("actionAbout_Hardware_Connection")
        self.menuHelp_H.addAction(self.actionAbout_Hardware_Connection)
        self.menubar.addAction(self.menuHelp_H.menuAction())

        self.retranslateUi(Vibration_analyzer)
        QtCore.QMetaObject.connectSlotsByName(Vibration_analyzer)

    def retranslateUi(self, Vibration_analyzer):
        _translate = QtCore.QCoreApplication.translate
        Vibration_analyzer.setWindowTitle(_translate("Vibration_analyzer", "Vibration Analyzer - Real time FFT spectrum of vibration"))
        self.label.setText(_translate("Vibration_analyzer", "COM Port"))
        self.label_2.setText(_translate("Vibration_analyzer", "Baud rate"))
        self.comboBox_baudrate.setCurrentText(_translate("Vibration_analyzer", "4800"))
        self.comboBox_baudrate.setItemText(0, _translate("Vibration_analyzer", "4800"))
        self.comboBox_baudrate.setItemText(1, _translate("Vibration_analyzer", "9600"))
        self.comboBox_baudrate.setItemText(2, _translate("Vibration_analyzer", "19200"))
        self.comboBox_baudrate.setItemText(3, _translate("Vibration_analyzer", "38400"))
        self.comboBox_baudrate.setItemText(4, _translate("Vibration_analyzer", "57600"))
        self.comboBox_baudrate.setItemText(5, _translate("Vibration_analyzer", "115200"))
        self.pushButton_start.setText(_translate("Vibration_analyzer", "Start "))
        self.pushButton_stop.setText(_translate("Vibration_analyzer", "Stop"))
        self.label_3.setText(_translate("Vibration_analyzer", "Specifications:\n"
"\n"
"* Spectral resolution:\n"
"1.95 Hz\n"
"\n"
"* Samples used:\n"
"256\n"
"\n"
"* Acquisition rate:\n"
"500 Hz\n"
"\n"
" * Nyquist frequency:\n"
"250 Hz"))
        self.label_4.setText(_translate("Vibration_analyzer", "Real time spectrum:"))
        self.label_5.setText(_translate("Vibration_analyzer", "Real time Peak-Frequency (Hz):"))
        self.pushButton_refresh_port.setText(_translate("Vibration_analyzer", "Refresh"))
        self.menuHelp_H.setTitle(_translate("Vibration_analyzer", "Help(H)"))
        self.actionAbout_Hardware_Connection.setText(_translate("Vibration_analyzer", "About Hardware Connection"))
