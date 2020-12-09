# -*- coding: utf-8 -*-

import os, sys, time
import shutil
import copy
import cv2 as cv
import numpy as np
import random
# embedding pyqt5 with matplotlib requires special announcement
from PIL import Image

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QDesktopWidget
from GUI import Ui_MainWindow

# add self designed process algorithm and parameter measurement
from Algorithm import ProcessAlgorithm
from Evaluation import EvaluationParameter

class VideoWindow(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.screen=QApplication.primaryScreen()
        self.setupUi(self)
        self.InitFrame("./icons/default_bg.jpeg")
        self.InitHistogram1('./icons/log_map.png')
        self.InitHistogram2('./icons/log_map.png')
        self.show()

        self.cwd = os.getcwd()
        self.tlx=0
        self.tly=0
        self.brx=0
        self.bry=0
        # set some status variable of the video
        self.flag = 1 # "1" means the status of pause
        self.loaded = 0 #0 means that the video is not loaded, self.lrcap is empty
        self.first_frame_label = 0 #0 means that the video is loaded and not at the beginning frame

        # define the parameters of the video
        self.delay_time = 0
        self.total_frames = 0
        self.load_success = False #initial status of the video
        self.current_frame_id = 0

        # define events of opening files
        # setup a timer to play the video
        # the time is related to the video's fps
        self.FrameTrigger = QTimer(self)
        # define the playorpause button
        self.btn_helper.clicked.connect(self.HelpDialogShow)
        self.btn_sr.clicked.connect(self.loadImages)

        # files
        self.files = {
            'input': None,
            'pr': None,
            'gs': None,
            'dt': None,
            'ccc': None,
            'awb': None
            #'shade': None
        }
        self.folder_path = None
        self.sld_division.valueChanged.connect(self.change_division_value)
        self.load_success = False

        # algorithms
        self.btn_wb.toggled.connect(lambda: self.change_algorithm())
        self.btn_t.toggled.connect(lambda: self.change_algorithm())
        self.btn_f.toggled.connect(lambda: self.change_algorithm())
        self.btn_d.toggled.connect(lambda: self.change_algorithm())
        self.btn_c.toggled.connect(lambda: self.change_algorithm())
        #self.btn_s.toggled.connect(lambda: self.change_algorithm())

    
    def loadImages(self):
        self.folder_path = QFileDialog.getExistingDirectory(
            self, 
            "Select a folder...", 
            "./"
        )
        if self.folder_path != "":
            files = os.listdir(self.folder_path)
            for item in files:
                img_path = os.path.join(self.folder_path, item)
                img = cv.imread(img_path)
                if '_awb' in item:
                    self.files['awb'] = img
                elif '_pr' in item:
                    self.files['pr'] = img
                elif '_gs' in item:
                    self.files['gs'] = img
                elif '_dt' in item:
                    self.files['dt'] = img
                #elif '_S.png' in item:
                #    self.files['shade'] = img
                elif '_ccc' in item:
                    self.files['ccc'] = img
                elif '_input' in item:
                    print("initial the frame")
                    #self.InitFrame(img_path)
                    self.files['input'] = img
                    final_path = img_path
                    print(final_path)
            #self.InitFrame(final_path)
            self.load_success = True
            return 1
        else:
            self.NoFileWarming()
            return -1

    def HelpDialogShow(self):
        dialog = QDialog()
        btn = QPushButton("OK", dialog)
        btn.move(50, 50)
        dialog.setWindowTitle("Helper")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def NoFileWarming(self):
        Nofile_dialog = QMessageBox.warning(
            self, 
            "Warning",
            "No files are selected, click yes to retry.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        if (Nofile_dialog == QMessageBox.Yes):
            self.loadImages()
        else:
            return

    def InitFrame(self, DefaultPicture):
        self.FrameDisplayAera_1.setPixmap(QPixmap(DefaultPicture))
        self.FrameDisplayAera_1.setScaledContents(True)
        #self.FrameDisplayAera_2.setPixmap(QPixmap(DefaultPicture))
        #self.FrameDisplayAera_2.setScaledContents(True)

    def InitHistogram1(self, DefaultPicture):
        self.Log_Map_1.setPixmap(QPixmap(DefaultPicture))
        self.Log_Map_1.setScaledContents(True)

    def InitHistogram2(self, DefaultPicture):
        self.Log_Map_2.setPixmap(QPixmap(DefaultPicture))
        self.Log_Map_2.setScaledContents(True)

    def show_lr_hr(self, framelr):
        framehr = self.files['input']
        #framelr = self.algorithmOption()
        ratio = self.division/100.
        h,w,c = framehr.shape
        #print('...................HR: ', framehr.shape)
        #print("self.height:{};self.width:{}".format(self.height, self.width))
        #print("height:{};width:{}".format(h, w))
        #newframehr = cv.resize(framehr, (w,h))
        #newframelr = cv.resize(framelr, (w,h))
        newframehr = framehr.copy()
        newframelr = framelr.copy()
        newframe = copy.deepcopy(newframehr)
        newframe[:, 0:int(w*ratio), :] = newframelr[:, 0:int(w*ratio), :]
        newframe[:, int(w*ratio):w, :] = newframehr[:, int(w*ratio):w, :]
        newframe[:, int(w*ratio):(int(w*ratio)+2), 0] = 255
        newframe[:, int(w*ratio):(int(w*ratio)+2), 1] = 0
        newframe[:, int(w*ratio):(int(w*ratio)+2), 2] = 0 
        # the following code is to add a margin of the original frames
        r1 = self.width / self.height
        r2 = w / h
        #print("r1:",r1)
        #print("r2:",r2)
        '''
        if r1>r2:
            margin = int((h*self.width/self.height - w)/2)-1
            print("margin_value:", margin)
            #newframe = cv.copyMakeBorder(newframe,margin,margin,0,0,cv.BORDER_CONSTANT,value=[0,0,0])
            newframe = cv.copyMakeBorder(newframe,0,0,margin,margin,cv.BORDER_CONSTANT,value=[0,0,0])
        else:
            margin = int((w*self.height/self.width - h)/2)-1
            print("margin_value:", margin)
            #newframe = cv.copyMakeBorder(newframe,0,0,margin,margin,cv.BORDER_CONSTANT,value=[0,0,0])
            newframe = cv.copyMakeBorder(newframe,margin,margin,0,0,cv.BORDER_CONSTANT,value=[0,0,0])
        '''
        return newframe

    def change_division_value(self):
        self.division = self.sld_division.value()
        self.lab_division.setText("Splitting Ratio (Processed : Input):\t" + str(self.division) + ":" + str(100-self.division))
        # the frame is always static, not video
        processed_frame = self.algorithmOption()
        newframe = self.show_lr_hr(processed_frame)
        cv.imwrite('./checkpoint.png', newframe)
        # play the video via read the next frame
        self.InitFrame('./checkpoint.png')
    
    def algorithmOption(self):
        # Judge the algorithm checkboxes' state and select the image
        if self.btn_wb.isChecked()==True:
            self.InitHistogram1(os.path.join(self.folder_path, 'log0.jpg'))
            self.InitHistogram2(os.path.join(self.folder_path, 'log1.jpg'))
            return self.files['awb']
        elif self.btn_t.isChecked()==True:
            self.InitHistogram1(os.path.join(self.folder_path, 'log0.jpg'))
            self.InitHistogram2(os.path.join(self.folder_path, 'log2.jpg'))
            return self.files['ccc']
        elif self.btn_f.isChecked()==True:
            self.InitHistogram1(os.path.join(self.folder_path, 'log0.jpg'))
            self.InitHistogram2(os.path.join(self.folder_path, 'log3.jpg'))
            return self.files['pr']
        elif self.btn_d.isChecked()==True:
            self.InitHistogram1(os.path.join(self.folder_path, 'log0.jpg'))
            self.InitHistogram2(os.path.join(self.folder_path, 'log4.jpg'))
            return self.files['gs']
        elif self.btn_c.isChecked()==True:
            self.InitHistogram1(os.path.join(self.folder_path, 'log0.jpg'))
            self.InitHistogram2(os.path.join(self.folder_path, 'log5.jpg'))
            return self.files['dt']
        #elif self.btn_s.isChecked()==True:
        #    return self.files['shade']
    
    def change_algorithm(self):
        frame = self.algorithmOption()
        newframe = self.show_lr_hr(frame)
        cv.imwrite('./checkpoint.png', newframe)
        # play the video via read the next frame
        self.InitFrame('./checkpoint.png')

def main():
    app = QApplication(sys.argv)
    VideoWindowDemo = VideoWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()