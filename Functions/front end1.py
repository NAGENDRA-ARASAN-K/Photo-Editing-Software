# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fe.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage,QIcon
from tkinter.filedialog import askopenfilename,asksaveasfilename
import imutils,cv2
from PIL import Image
import pygame
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

pygame.init()


class Ui_MainWindow(object):

    def updatecrop(self,image):
        self.image=self.crop(self.image)
        self.setPhoto(self.image)

    def updatezap(self,image):
        self.image=self.zoom_and_pan(self.image)
        self.setPhoto(self.image)

    def updateflr(self,image):
        self.image=self.tmp
        self.image=self.fliplr(self.image)
        self.setPhoto(self.image)
        

    def updatefud(self,image):
        self.image=self.tmp
        self.image=self.flipud(self.image)
        self.setPhoto(self.image)

    def updatecrot(self,image):
        self.image=self.tmp
        self.image=self.clockrotate(self.image)
        self.setPhoto(self.image)

    def updateccrot(self,image):
        self.image=self.tmp
        self.image=self.counterclockrotate(self.image)
        self.setPhoto(self.image)

    def updategray(self,image):
        try:
            self.image=self.tmp
            self.image=self.grayscale(self.image)
            self.setPhoto(self.image)
        except:
            pass

    def updatehsv(self,image):
        try:
            self.image=self.tmp
            self.image=self.hsv(self.image)
            self.setPhoto(self.image)
        except:
            pass

    def updatergb(self,image):
        try:
            self.image=self.tmp
            self.image=self.rgb(self.image)
            self.setPhoto(self.image)
        except:
            pass

    def updatelab(self,image):
        try:
            self.image=self.tmp
            self.image=self.lab(self.image)
            self.setPhoto(self.image)
        except:
            pass

    def updatebac(self):
        self.tmp=self.image
        self.tmp=self.bac(self.image,self.ci,self.bri)
        self.setPhoto(self.tmp,True)

    def brindex(self,bri):
        self.bri=bri
        print(self.bri)
        self.updatebac()

    def cindex(self,ci):
        self.ci=ci
        print(self.ci)
        self.updatebac()

    def updatesaturation(self):
        self.tmp=self.image
        self.tmp=self.saturate(self.image,self.si)
        self.setPhoto(self.tmp,True)

    def sindex(self,si):
        self.si=si
        print(self.si)
        self.updatesaturation()

    def updateblur(self):
        self.tmp=self.image
        self.tmp=self.blur(self.image,self.bi)
        self.setPhoto(self.tmp,True)

    def bindex(self,bi):
        self.bi=bi
        print(self.bi)
        self.updateblur()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1662, 951)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.undoButton = QtWidgets.QToolButton(self.centralwidget)
        self.undoButton.setGeometry(QtCore.QRect(50, 820, 62, 62))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Icon/Undo Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.undoButton.setIcon(icon)
        self.undoButton.setIconSize(QtCore.QSize(62, 62))
        self.undoButton.setObjectName("undoButton")
        self.redoButton = QtWidgets.QToolButton(self.centralwidget)
        self.redoButton.setGeometry(QtCore.QRect(130, 820, 62, 62))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Icon/Redo Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.redoButton.setIcon(icon1)
        self.redoButton.setIconSize(QtCore.QSize(62, 62))
        self.redoButton.setObjectName("redoButton")
        self.cropButton = QtWidgets.QToolButton(self.centralwidget)
        self.cropButton.setGeometry(QtCore.QRect(10, 200, 102, 102))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../Icon/Crop Icon.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cropButton.setIcon(icon2)
        self.cropButton.setIconSize(QtCore.QSize(160, 80))
        self.cropButton.setObjectName("cropButton")
        self.zapButton = QtWidgets.QToolButton(self.centralwidget)
        self.zapButton.setGeometry(QtCore.QRect(130, 200, 102, 102))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../Icon/Zoom and Pan Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zapButton.setIcon(icon3)
        self.zapButton.setIconSize(QtCore.QSize(102, 102))
        self.zapButton.setObjectName("zapButton")
        self.flrButton = QtWidgets.QToolButton(self.centralwidget)
        self.flrButton.setGeometry(QtCore.QRect(10, 320, 102, 102))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../Icon/Flip.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.flrButton.setIcon(icon4)
        self.flrButton.setIconSize(QtCore.QSize(102, 102))
        self.flrButton.setObjectName("flrButton")
        self.fudButton = QtWidgets.QToolButton(self.centralwidget)
        self.fudButton.setGeometry(QtCore.QRect(130, 320, 102, 102))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../Icon/FlipUD.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fudButton.setIcon(icon5)
        self.fudButton.setIconSize(QtCore.QSize(102, 102))
        self.fudButton.setObjectName("fudButton")
        self.rotateantiButton = QtWidgets.QToolButton(self.centralwidget)
        self.rotateantiButton.setGeometry(QtCore.QRect(130, 440, 102, 102))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../Icon/rotationanti.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rotateantiButton.setIcon(icon6)
        self.rotateantiButton.setIconSize(QtCore.QSize(90, 90))
        self.rotateantiButton.setObjectName("rotateantiButton")
        self.rotateclockButton = QtWidgets.QToolButton(self.centralwidget)
        self.rotateclockButton.setGeometry(QtCore.QRect(10, 440, 102, 102))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../Icon/rotaioncl.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rotateclockButton.setIcon(icon7)
        self.rotateclockButton.setIconSize(QtCore.QSize(90, 90))
        self.rotateclockButton.setObjectName("rotateclockButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 10, 1401, 791))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 560, 231, 241))
        font = QtGui.QFont()
        font.setFamily("Poor Richard")
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.grayButton = QtWidgets.QPushButton(self.tab)
        self.grayButton.setGeometry(QtCore.QRect(30, 10, 161, 31))
        self.grayButton.setObjectName("grayButton")
        self.hsvButton = QtWidgets.QPushButton(self.tab)
        self.hsvButton.setGeometry(QtCore.QRect(30, 60, 161, 31))
        self.hsvButton.setObjectName("hsvButton")
        self.rgbButton = QtWidgets.QPushButton(self.tab)
        self.rgbButton.setGeometry(QtCore.QRect(30, 110, 161, 31))
        self.rgbButton.setObjectName("rgbButton")
        self.labButton = QtWidgets.QPushButton(self.tab)
        self.labButton.setGeometry(QtCore.QRect(30, 160, 161, 31))
        self.labButton.setObjectName("labButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.toolBox = QtWidgets.QToolBox(self.tab_2)
        self.toolBox.setGeometry(QtCore.QRect(0, 0, 221, 201))
        font = QtGui.QFont()
        font.setFamily("Poor Richard")
        font.setPointSize(11)
        self.toolBox.setFont(font)
        self.toolBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toolBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 219, 99))
        self.page.setObjectName("page")
        self.brightnessSlider = QtWidgets.QSlider(self.page)
        self.brightnessSlider.setMinimum(1)
        self.brightnessSlider.setMaximum(25)
        self.brightnessSlider.setValue(10)
        self.brightnessSlider.setGeometry(QtCore.QRect(0, 0, 211, 31))
        self.brightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        self.brightnessSlider.setObjectName("brightnessSlider")
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 219, 99))
        self.page_2.setObjectName("page_2")
        self.contrastSlider = QtWidgets.QSlider(self.page_2)
        self.contrastSlider.setMinimum(-127)
        self.contrastSlider.setMaximum(127)
        self.contrastSlider.setValue(0)
        self.contrastSlider.setGeometry(QtCore.QRect(0, 0, 211, 31))
        self.contrastSlider.setOrientation(QtCore.Qt.Horizontal)
        self.contrastSlider.setObjectName("contrastSlider")
        self.toolBox.addItem(self.page_2, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 219, 99))
        self.page_3.setObjectName("page_3")
        self.saturationSlider = QtWidgets.QSlider(self.page_3)
        self.saturationSlider.setMinimum(0)
        self.saturationSlider.setMaximum(70)
        self.saturationSlider.setValue(10)
        self.saturationSlider.setGeometry(QtCore.QRect(0, 0, 211, 31))
        self.saturationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.saturationSlider.setObjectName("saturationSlider")
        self.toolBox.addItem(self.page_3, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 219, 99))
        self.page_4.setObjectName("page_4")
        self.blurSlider = QtWidgets.QSlider(self.page_4)
        self.blurSlider.setMinimum(1)
        self.blurSlider.setMaximum(50)
        self.blurSlider.setValue(1)
        self.blurSlider.setGeometry(QtCore.QRect(0, 0, 211, 31))
        self.blurSlider.setOrientation(QtCore.Qt.Horizontal)
        self.blurSlider.setObjectName("blurSlider")
        self.toolBox.addItem(self.page_4, "")
        self.tabWidget.addTab(self.tab_2, "")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 221, 171))
        font = QtGui.QFont()
        font.setFamily("Poor Richard")
        font.setPointSize(18)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(80, 90, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.brushSlider = QtWidgets.QSlider(self.groupBox)
        self.brushSlider.setGeometry(QtCore.QRect(10, 130, 201, 31))
        self.brushSlider.setOrientation(QtCore.Qt.Horizontal)
        self.brushSlider.setObjectName("brushSlider")
        self.colourButton = QtWidgets.QPushButton(self.groupBox)
        self.colourButton.setGeometry(QtCore.QRect(50, 40, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.colourButton.setFont(font)
        self.colourButton.setObjectName("colourButton")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../Icon/brush1.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1662, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        

        self.filename=None
        self.newfilename=None
        self.tmp=None
        self.bri=1
        self.ci=10
        self.si=0
        self.bi=0
        self.undo_stack = []
        self.redo_stack = []

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Photo Editing Software"))
        MainWindow.setWindowIcon(QIcon('C:/Users/nikhi/Desktop/CS Project - V2/Icon/brush1.png'))
        self.undoButton.setText(_translate("MainWindow", "..."))
        self.undoButton.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.redoButton.setText(_translate("MainWindow", "..."))
        self.redoButton.setShortcut(_translate("MainWindow", "Ctrl+Shift+Z"))
        self.cropButton.setText(_translate("MainWindow", "..."))
        self.zapButton.setText(_translate("MainWindow", "..."))
        self.flrButton.setText(_translate("MainWindow", "..."))
        self.fudButton.setText(_translate("MainWindow", "..."))
        self.rotateantiButton.setText(_translate("MainWindow", "..."))
        self.rotateclockButton.setText(_translate("MainWindow", "..."))
        self.grayButton.setText(_translate("MainWindow", "GRAYSCALE"))
        self.hsvButton.setText(_translate("MainWindow", "HSV"))
        self.rgbButton.setText(_translate("MainWindow", "RGB"))
        self.labButton.setText(_translate("MainWindow", "LAB"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "FILTERS"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("MainWindow", "BRIGHTNESS"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("MainWindow", "CONTRAST"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("MainWindow", "SATURATION"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("MainWindow", "BLUR"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "ADJUST"))
        self.groupBox.setTitle(_translate("MainWindow", "BRUSH "))
        self.label_2.setText(_translate("MainWindow", "SIZE"))
        self.colourButton.setText(_translate("MainWindow", "COLOUR"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionSave_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
