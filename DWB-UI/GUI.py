# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random

# Create plot based on matplotlib, which can embed to pyqt5

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        screen = QDesktopWidget().screenGeometry()
        MainWindow.resize(screen.width()*6/7, screen.height()*2/3)
        size = self.geometry()
        self.width = self.width()
        width = self.width
        self.height = self.height()
        height = self.height

        self.GroupBox = QGroupBox("Algorithms", self)
        self.btn_wb = QRadioButton("Deep White Balancing\n(Log-chrominance)", self)
        self.btn_t = QRadioButton("Conv Color Constancy\n(Log-chrominance)", self)
        self.btn_f = QRadioButton("Perfect Reflection\n(RGB Color Space)", self)
        self.btn_d = QRadioButton("Gray Space Assumption\n(RGB Color Space))", self)
        self.btn_c = QRadioButton("Dynamic Threshold\n(YCrCb Color Space)", self)
        #self.btn_s = QRadioButton("Shade WB", self)
        # default, choose the white balance algorithm
        self.btn_wb.setChecked(True)
        self.check_layout = QVBoxLayout()
        self.init_check_layout()
        self.GroupBox.setGeometry(QtCore.QRect(width/80, height*35/100, width/6, height*1/2))

        #set six buttons of processing algorithm
        self.btn_sr = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sr.setGeometry(QtCore.QRect(width/100, height/6, (width)/6, height/15))
        self.btn_sr.setObjectName("sr")

        self.title = QLabel("Slide to View\nWhite Balancing", self)     
        self.title.setStyleSheet("QLabel{color:rgb(76,90,173);font-size:20px;font-weight:normal;font-family:Arial;}")
        self.title.setGeometry(QtCore.QRect(width/50, height/30, width/6, height/10))

        self.btn_helper = QtWidgets.QPushButton(self.centralwidget)
        self.btn_helper.setGeometry(QtCore.QRect(width/100, height*6/24, (width)/6, height/15))
        self.btn_helper.setObjectName("helper")

        # define the area to display original & processed video
        self.FrameDisplayAera_1 = QLabel(self)
        self.FrameDisplayAera_1.setGeometry(QtCore.QRect(width/5, height/30, 0.55*width, height*80/100))
        self.FrameDisplayAera_1.setObjectName("FrameDisplayAera_1")

        self.map_size = 0.19*width
        self.Log_Map_1 = QLabel(self)
        self.Log_Map_1.setGeometry(QtCore.QRect(width*77/100, height/30, self.map_size, self.map_size))
        self.Log_Map_1.setObjectName("FrameDisplayAera_1")

        self.Log_Map_2 = QLabel(self)
        self.Log_Map_2.setGeometry(QtCore.QRect(width*77/100, height*45/100, self.map_size, self.map_size))
        self.Log_Map_2.setObjectName("FrameDisplayAera_1")

        #self.log_c_tag = QtWidgets.QLabel(self.centralwidget)
        #self.log_c_tag.setGeometry(QtCore.QRect(width*77/100, height*10/11, width/5, height/10))
        #self.log_c_tag.setObjectName("log_c_tag")

        self.log_c_tag = QLabel("Log Chrominance Comparison\n(The output is under the input)", self)     
        self.log_c_tag.setStyleSheet("QLabel{color:rgb(0,0,0);font-size:15px;font-weight:normal;font-family:Arial;}")
        self.log_c_tag.setGeometry(QtCore.QRect(width*77/100, height*85/100, width/6, height/10))

        # slider to set the seperation line
        self.sld_division = QtWidgets.QSlider(self.centralwidget)
        self.sld_division.setGeometry(QtCore.QRect(width/5, height*7/8, 0.55*width, height/60))
        self.sld_division.setMaximum(100)
        self.sld_division.setOrientation(QtCore.Qt.Horizontal)
        self.sld_division.setObjectName("sld_division")

        self.lab_division = QtWidgets.QLabel(self.centralwidget)
        self.lab_division.setGeometry(QtCore.QRect(width*40/100, height*10/11, width/2, height/35))
        self.lab_division.setObjectName("lab_video")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 568, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        print("width\t",width)
        print("height\t",height)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    
    def retranslateUi(self, MainWindow):
        names = ["Select Images", "Help"]
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_sr.setText(_translate("MainWindow",names[0]))
        self.btn_helper.setText(_translate("MainWindow",names[1]))
        #self.btn_hei.setText(_translate("MainWindow",names[2]))
        #self.btn_color.setText(_translate("MainWindow",names[3]))
        #self.btn_fps.setText(_translate("MainWindow",names[4]))
        #self.btn_repair.setText(_translate("MainWindow",names[5]))
        self.lab_division.setText(_translate("MainWindow", "Splitting Ratio (Processed : Input):\t30:70"))
        #self.lab_division.setText(_translate("MainWindow", "Log Chrominance Map Comparison\n (Input up and output down)"))
        self.sld_division.setValue(30)


    def init_check_layout(self):
        self.check_layout.addWidget(self.btn_wb)
        self.check_layout.addWidget(self.btn_t)
        self.check_layout.addWidget(self.btn_f)
        self.check_layout.addWidget(self.btn_d)
        self.check_layout.addWidget(self.btn_c)
        #self.check_layout.addWidget(self.btn_s)
        #self.check_layout.addWidget(self.check_add_frame)
        self.GroupBox.setLayout(self.check_layout)