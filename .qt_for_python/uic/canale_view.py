# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'canale_view.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from pyqtgraph import PlotWidget


class Ui_facewindow(object):
    def setupUi(self, facewindow):
        if not facewindow.objectName():
            facewindow.setObjectName(u"facewindow")
        facewindow.resize(1253, 854)
        facewindow.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(u"Verdana")
        font.setPointSize(8)
        facewindow.setFont(font)
        icon = QIcon()
        icon.addFile(u"../../../../git/SiMPlE/smfsmanager/D_mica.png", QSize(), QIcon.Normal, QIcon.Off)
        facewindow.setWindowIcon(icon)
        self.centralwidget = QWidget(facewindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_8 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.grafo = PlotWidget(self.splitter)
        self.grafo.setObjectName(u"grafo")
        self.grafo.setMinimumSize(QSize(200, 200))
        self.splitter.addWidget(self.grafo)
        self.stat = PlotWidget(self.splitter)
        self.stat.setObjectName(u"stat")
        self.stat.setMinimumSize(QSize(100, 100))
        self.splitter.addWidget(self.stat)
        self.splitter_2.addWidget(self.splitter)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBox_4 = QGroupBox(self.layoutWidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        font1 = QFont()
        font1.setFamily(u"Verdana")
        font1.setPointSize(8)
        font1.setBold(True)
        self.groupBox_4.setFont(font1)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.radio_area = QRadioButton(self.groupBox_4)
        self.radio_area.setObjectName(u"radio_area")
        font2 = QFont()
        font2.setBold(False)
        self.radio_area.setFont(font2)

        self.verticalLayout_4.addWidget(self.radio_area)

        self.radio_deriv = QRadioButton(self.groupBox_4)
        self.radio_deriv.setObjectName(u"radio_deriv")
        self.radio_deriv.setFont(font2)

        self.verticalLayout_4.addWidget(self.radio_deriv)

        self.radio_view = QRadioButton(self.groupBox_4)
        self.radio_view.setObjectName(u"radio_view")
        self.radio_view.setFont(font2)
        self.radio_view.setChecked(True)

        self.verticalLayout_4.addWidget(self.radio_view)

        self.radio_smooth = QRadioButton(self.groupBox_4)
        self.radio_smooth.setObjectName(u"radio_smooth")
        self.radio_smooth.setFont(font2)

        self.verticalLayout_4.addWidget(self.radio_smooth)

        self.radio_traits = QRadioButton(self.groupBox_4)
        self.radio_traits.setObjectName(u"radio_traits")
        self.radio_traits.setFont(font2)

        self.verticalLayout_4.addWidget(self.radio_traits)


        self.verticalLayout_7.addWidget(self.groupBox_4)

        self.cvTree = QListView(self.layoutWidget)
        self.cvTree.setObjectName(u"cvTree")

        self.verticalLayout_7.addWidget(self.cvTree)

        self.verticalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_3)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_5 = QGroupBox(self.layoutWidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setFont(font1)
        self.verticalLayout = QVBoxLayout(self.groupBox_5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.bAddFile = QPushButton(self.groupBox_5)
        self.bAddFile.setObjectName(u"bAddFile")
        self.bAddFile.setFont(font2)

        self.verticalLayout.addWidget(self.bAddFile)

        self.bAddFiles = QPushButton(self.groupBox_5)
        self.bAddFiles.setObjectName(u"bAddFiles")
        self.bAddFiles.setFont(font2)

        self.verticalLayout.addWidget(self.bAddFiles)

        self.bAddDir = QPushButton(self.groupBox_5)
        self.bAddDir.setObjectName(u"bAddDir")
        self.bAddDir.setFont(font2)

        self.verticalLayout.addWidget(self.bAddDir)

        self.bReset = QPushButton(self.groupBox_5)
        self.bReset.setObjectName(u"bReset")
        self.bReset.setFont(font2)

        self.verticalLayout.addWidget(self.bReset)

        self.bDoSave = QPushButton(self.groupBox_5)
        self.bDoSave.setObjectName(u"bDoSave")
        self.bDoSave.setFont(font2)

        self.verticalLayout.addWidget(self.bDoSave)

        self.famGroup = QGroupBox(self.groupBox_5)
        self.famGroup.setObjectName(u"famGroup")
        self.famGroup.setMinimumSize(QSize(0, 0))
        self.famGroup.setFont(font1)
        self.famGroup.setCheckable(True)
        self.famGroup.setChecked(False)
        self.verticalLayout_11 = QVBoxLayout(self.famGroup)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.bAddFamily = QPushButton(self.famGroup)
        self.bAddFamily.setObjectName(u"bAddFamily")
        self.bAddFamily.setFont(font2)

        self.verticalLayout_11.addWidget(self.bAddFamily)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_24 = QLabel(self.famGroup)
        self.label_24.setObjectName(u"label_24")
        font3 = QFont()
        font3.setFamily(u"Verdana")
        font3.setPointSize(8)
        font3.setBold(False)
        self.label_24.setFont(font3)

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_24)

        self.cNumFam = QLabel(self.famGroup)
        self.cNumFam.setObjectName(u"cNumFam")
        font4 = QFont()
        font4.setFamily(u"Verdana")
        font4.setPointSize(9)
        font4.setBold(True)
        self.cNumFam.setFont(font4)
        self.cNumFam.setStyleSheet(u"font-weight: bold;")
        self.cNumFam.setAlignment(Qt.AlignCenter)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.cNumFam)

        self.label_25 = QLabel(self.famGroup)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font3)

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_25)

        self.cFamilyLoad = QSlider(self.famGroup)
        self.cFamilyLoad.setObjectName(u"cFamilyLoad")
        self.cFamilyLoad.setFont(font2)
        self.cFamilyLoad.setMinimum(1)
        self.cFamilyLoad.setMaximum(1)
        self.cFamilyLoad.setPageStep(2)
        self.cFamilyLoad.setOrientation(Qt.Horizontal)
        self.cFamilyLoad.setTickPosition(QSlider.TicksAbove)
        self.cFamilyLoad.setTickInterval(1)

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.cFamilyLoad)


        self.verticalLayout_11.addLayout(self.formLayout_4)


        self.verticalLayout.addWidget(self.famGroup)


        self.verticalLayout_6.addWidget(self.groupBox_5)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_6)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_3 = QGroupBox(self.layoutWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font1)
        self.formLayout = QFormLayout(self.groupBox_3)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")
        self.label.setFont(font3)
        self.label.setStyleSheet(u"border: none;")
        self.label.setTextFormat(Qt.AutoText)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.s_mth = QDoubleSpinBox(self.groupBox_3)
        self.s_mth.setObjectName(u"s_mth")
        self.s_mth.setFont(font3)
        self.s_mth.setMinimum(-100000.000000000000000)
        self.s_mth.setMaximum(100000.000000000000000)
        self.s_mth.setValue(2.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.s_mth)

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font3)
        self.label_2.setStyleSheet(u"border: none;")
        self.label_2.setTextFormat(Qt.AutoText)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.s_vth = QDoubleSpinBox(self.groupBox_3)
        self.s_vth.setObjectName(u"s_vth")
        self.s_vth.setFont(font3)
        self.s_vth.setMinimum(-100000.000000000000000)
        self.s_vth.setMaximum(100000.000000000000000)
        self.s_vth.setValue(10.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.s_vth)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font3)
        self.label_3.setStyleSheet(u"border: none;")
        self.label_3.setTextFormat(Qt.AutoText)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.sg_fw = QDoubleSpinBox(self.groupBox_3)
        self.sg_fw.setObjectName(u"sg_fw")
        self.sg_fw.setFont(font3)
        self.sg_fw.setMinimum(-100000.000000000000000)
        self.sg_fw.setMaximum(100000.000000000000000)
        self.sg_fw.setValue(10.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.sg_fw)

        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font3)
        self.label_4.setStyleSheet(u"border: none;")
        self.label_4.setTextFormat(Qt.AutoText)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.sg_mm = QSpinBox(self.groupBox_3)
        self.sg_mm.setObjectName(u"sg_mm")
        self.sg_mm.setFont(font3)
        self.sg_mm.setMaximum(180)
        self.sg_mm.setValue(10)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.sg_mm)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")
        font5 = QFont()
        font5.setFamily(u"Verdana")
        font5.setPointSize(8)
        font5.setBold(False)
        font5.setKerning(True)
        self.label_5.setFont(font5)
        self.label_5.setStyleSheet(u"border: none;")
        self.label_5.setFrameShape(QFrame.NoFrame)
        self.label_5.setLineWidth(1)
        self.label_5.setTextFormat(Qt.AutoText)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.plath = QDoubleSpinBox(self.groupBox_3)
        self.plath.setObjectName(u"plath")
        self.plath.setFont(font3)
        self.plath.setMinimum(-100000.000000000000000)
        self.plath.setMaximum(100000.000000000000000)
        self.plath.setValue(30.000000000000000)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.plath)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font3)
        self.label_6.setStyleSheet(u"border: none;")
        self.label_6.setLineWidth(1)
        self.label_6.setTextFormat(Qt.AutoText)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.lasth = QDoubleSpinBox(self.groupBox_3)
        self.lasth.setObjectName(u"lasth")
        self.lasth.setFont(font3)
        self.lasth.setMaximum(1000.000000000000000)
        self.lasth.setValue(5.000000000000000)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.lasth)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font3)
        self.label_7.setStyleSheet(u"border: none;")
        self.label_7.setLineWidth(1)
        self.label_7.setTextFormat(Qt.AutoText)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_7)

        self.derorder = QSpinBox(self.groupBox_3)
        self.derorder.setObjectName(u"derorder")
        self.derorder.setFont(font3)
        self.derorder.setMaximum(10)
        self.derorder.setValue(1)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.derorder)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.btn_flatten = QPushButton(self.layoutWidget)
        self.btn_flatten.setObjectName(u"btn_flatten")

        self.verticalLayout_5.addWidget(self.btn_flatten)

        self.btn_recalibrate = QPushButton(self.layoutWidget)
        self.btn_recalibrate.setObjectName(u"btn_recalibrate")

        self.verticalLayout_5.addWidget(self.btn_recalibrate)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_2 = QGroupBox(self.layoutWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font1)
        self.formLayout_2 = QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font3)
        self.label_8.setStyleSheet(u"border: none;")
        self.label_8.setTextFormat(Qt.AutoText)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.lab_N = QLabel(self.groupBox_2)
        self.lab_N.setObjectName(u"lab_N")
        self.lab_N.setFont(font4)
        self.lab_N.setStyleSheet(u"border: none; font-weight: bold;")
        self.lab_N.setTextFormat(Qt.AutoText)
        self.lab_N.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.lab_N)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font3)
        self.label_9.setStyleSheet(u"border: none;")
        self.label_9.setTextFormat(Qt.AutoText)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_9)

        self.lab_Np = QLabel(self.groupBox_2)
        self.lab_Np.setObjectName(u"lab_Np")
        self.lab_Np.setFont(font4)
        self.lab_Np.setStyleSheet(u"border: none; font-weight: bold;")
        self.lab_Np.setTextFormat(Qt.AutoText)
        self.lab_Np.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.lab_Np)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font3)
        self.label_10.setStyleSheet(u"border: none;")
        self.label_10.setTextFormat(Qt.AutoText)

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_10)

        self.lab_Nj = QLabel(self.groupBox_2)
        self.lab_Nj.setObjectName(u"lab_Nj")
        self.lab_Nj.setFont(font4)
        self.lab_Nj.setStyleSheet(u"border: none; font-weight: bold;")
        self.lab_Nj.setTextFormat(Qt.AutoText)
        self.lab_Nj.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.lab_Nj)

        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font3)
        self.label_11.setStyleSheet(u"border: none;")
        self.label_11.setTextFormat(Qt.AutoText)

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_11)

        self.lab_Nblue = QLabel(self.groupBox_2)
        self.lab_Nblue.setObjectName(u"lab_Nblue")
        self.lab_Nblue.setFont(font4)
        self.lab_Nblue.setStyleSheet(u"border: none; font-weight: bold;")
        self.lab_Nblue.setTextFormat(Qt.AutoText)
        self.lab_Nblue.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.lab_Nblue)

        self.label_18 = QLabel(self.groupBox_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font3)

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_18)

        self.reflatten = QCheckBox(self.groupBox_2)
        self.reflatten.setObjectName(u"reflatten")
        self.reflatten.setFont(font3)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.reflatten)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font3)
        self.label_13.setStyleSheet(u"border: none;")

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.label_13)

        self.lcd_Area = QLabel(self.groupBox_2)
        self.lcd_Area.setObjectName(u"lcd_Area")
        self.lcd_Area.setFont(font4)
        self.lcd_Area.setStyleSheet(u"font-weight: bold;")
        self.lcd_Area.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.lcd_Area)

        self.label_22 = QLabel(self.groupBox_2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font3)

        self.formLayout_2.setWidget(10, QFormLayout.LabelRole, self.label_22)

        self.lcd_hieght = QLabel(self.groupBox_2)
        self.lcd_hieght.setObjectName(u"lcd_hieght")
        self.lcd_hieght.setFont(font4)
        self.lcd_hieght.setStyleSheet(u"font-weight: bold;")
        self.lcd_hieght.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(10, QFormLayout.FieldRole, self.lcd_hieght)

        self.sslabel_4 = QLabel(self.groupBox_2)
        self.sslabel_4.setObjectName(u"sslabel_4")
        self.sslabel_4.setFont(font3)
        self.sslabel_4.setStyleSheet(u"border: none;")
        self.sslabel_4.setTextFormat(Qt.AutoText)

        self.formLayout_2.setWidget(13, QFormLayout.LabelRole, self.sslabel_4)

        self.cnumb = QLabel(self.groupBox_2)
        self.cnumb.setObjectName(u"cnumb")
        self.cnumb.setFont(font4)
        self.cnumb.setStyleSheet(u"border: none; font-weight: bold;")
        self.cnumb.setTextFormat(Qt.AutoText)
        self.cnumb.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(13, QFormLayout.FieldRole, self.cnumb)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font3)

        self.formLayout_2.setWidget(14, QFormLayout.LabelRole, self.label_12)

        self.cscope = QPushButton(self.groupBox_2)
        self.cscope.setObjectName(u"cscope")
        self.cscope.setFont(font2)
        self.cscope.setCheckable(True)
        self.cscope.setChecked(False)

        self.formLayout_2.setWidget(14, QFormLayout.FieldRole, self.cscope)

        self.label_23 = QLabel(self.groupBox_2)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font3)

        self.formLayout_2.setWidget(15, QFormLayout.LabelRole, self.label_23)

        self.cFamily = QSlider(self.groupBox_2)
        self.cFamily.setObjectName(u"cFamily")
        self.cFamily.setMinimum(1)
        self.cFamily.setMaximum(1)
        self.cFamily.setPageStep(2)
        self.cFamily.setOrientation(Qt.Horizontal)
        self.cFamily.setTickPosition(QSlider.TicksAbove)
        self.cFamily.setTickInterval(1)

        self.formLayout_2.setWidget(15, QFormLayout.FieldRole, self.cFamily)

        self.label_29 = QLabel(self.groupBox_2)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font2)

        self.formLayout_2.setWidget(11, QFormLayout.LabelRole, self.label_29)

        self.lcd_detX = QLabel(self.groupBox_2)
        self.lcd_detX.setObjectName(u"lcd_detX")
        font6 = QFont()
        font6.setPointSize(9)
        self.lcd_detX.setFont(font6)
        self.lcd_detX.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(11, QFormLayout.FieldRole, self.lcd_detX)

        self.label_30 = QLabel(self.groupBox_2)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font2)

        self.formLayout_2.setWidget(12, QFormLayout.LabelRole, self.label_30)

        self.lcd_detF = QLabel(self.groupBox_2)
        self.lcd_detF.setObjectName(u"lcd_detF")
        self.lcd_detF.setFont(font6)
        self.lcd_detF.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(12, QFormLayout.FieldRole, self.lcd_detF)

        self.label_31 = QLabel(self.groupBox_2)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font2)

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_31)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.arBlue = QRadioButton(self.groupBox_2)
        self.arBlue.setObjectName(u"arBlue")
        self.arBlue.setFont(font2)
        self.arBlue.setStyleSheet(u"background-color:blue; color: white;")
        self.arBlue.setChecked(False)

        self.horizontalLayout_11.addWidget(self.arBlue)

        self.arGreen = QRadioButton(self.groupBox_2)
        self.arGreen.setObjectName(u"arGreen")
        self.arGreen.setFont(font2)
        self.arGreen.setStyleSheet(u"background-color:green; color: white;")
        self.arGreen.setChecked(True)

        self.horizontalLayout_11.addWidget(self.arGreen)


        self.formLayout_2.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_11)

        self.label_32 = QLabel(self.groupBox_2)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font2)

        self.formLayout_2.setWidget(8, QFormLayout.LabelRole, self.label_32)

        self.lcd_JArea = QLabel(self.groupBox_2)
        self.lcd_JArea.setObjectName(u"lcd_JArea")
        self.lcd_JArea.setFont(font6)
        self.lcd_JArea.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.lcd_JArea)

        self.label_34 = QLabel(self.groupBox_2)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font2)

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_34)

        self.str_lim = QDoubleSpinBox(self.groupBox_2)
        self.str_lim.setObjectName(u"str_lim")
        self.str_lim.setFont(font2)
        self.str_lim.setMaximum(99999.000000000000000)
        self.str_lim.setSingleStep(2.000000000000000)
        self.str_lim.setValue(20.000000000000000)

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.str_lim)

        self.label_35 = QLabel(self.groupBox_2)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font2)

        self.formLayout_2.setWidget(9, QFormLayout.LabelRole, self.label_35)

        self.lcd_strA = QLabel(self.groupBox_2)
        self.lcd_strA.setObjectName(u"lcd_strA")
        self.lcd_strA.setFont(font6)
        self.lcd_strA.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(9, QFormLayout.FieldRole, self.lcd_strA)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.btn_popout = QPushButton(self.layoutWidget)
        self.btn_popout.setObjectName(u"btn_popout")

        self.verticalLayout_2.addWidget(self.btn_popout)

        self.cbar = QSlider(self.layoutWidget)
        self.cbar.setObjectName(u"cbar")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbar.sizePolicy().hasHeightForWidth())
        self.cbar.setSizePolicy(sizePolicy)
        self.cbar.setMinimum(0)
        self.cbar.setMaximum(0)
        self.cbar.setPageStep(10)
        self.cbar.setValue(0)
        self.cbar.setOrientation(Qt.Horizontal)
        self.cbar.setTickPosition(QSlider.TicksAbove)
        self.cbar.setTickInterval(10)

        self.verticalLayout_2.addWidget(self.cbar)

        self.verticalSpacer_5 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.layoutWidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.groupBox.setFont(font1)
        self.formLayout_3 = QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.sslabel = QLabel(self.groupBox)
        self.sslabel.setObjectName(u"sslabel")
        self.sslabel.setFont(font3)
        self.sslabel.setStyleSheet(u"border: none;")
        self.sslabel.setTextFormat(Qt.AutoText)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.sslabel)

        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font3)
        self.label_14.setStyleSheet(u"border: none;")
        self.label_14.setTextFormat(Qt.AutoText)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_14)

        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font3)
        self.label_15.setStyleSheet(u"border: none;")
        self.label_15.setTextFormat(Qt.AutoText)

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_15)

        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font3)
        self.label_16.setStyleSheet(u"border: none;")
        self.label_16.setTextFormat(Qt.AutoText)

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_16)

        self.label_17 = QLabel(self.groupBox)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font3)
        self.label_17.setStyleSheet(u"border: none;")
        self.label_17.setTextFormat(Qt.AutoText)

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_17)

        self.sslabel_2 = QLabel(self.groupBox)
        self.sslabel_2.setObjectName(u"sslabel_2")
        self.sslabel_2.setFont(font3)
        self.sslabel_2.setStyleSheet(u"border: none;")
        self.sslabel_2.setTextFormat(Qt.AutoText)

        self.formLayout_3.setWidget(5, QFormLayout.LabelRole, self.sslabel_2)

        self.sslabel_3 = QLabel(self.groupBox)
        self.sslabel_3.setObjectName(u"sslabel_3")
        self.sslabel_3.setFont(font3)
        self.sslabel_3.setStyleSheet(u"border: none;")
        self.sslabel_3.setTextFormat(Qt.AutoText)

        self.formLayout_3.setWidget(6, QFormLayout.LabelRole, self.sslabel_3)

        self.lab_Tslope = QLabel(self.groupBox)
        self.lab_Tslope.setObjectName(u"lab_Tslope")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lab_Tslope.sizePolicy().hasHeightForWidth())
        self.lab_Tslope.setSizePolicy(sizePolicy2)
        self.lab_Tslope.setFont(font4)
        self.lab_Tslope.setStyleSheet(u"border: none; font-weight: bold;")
        self.lab_Tslope.setTextFormat(Qt.AutoText)
        self.lab_Tslope.setAlignment(Qt.AlignCenter)

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.lab_Tslope)

        self.lab_pj = QLabel(self.groupBox)
        self.lab_pj.setObjectName(u"lab_pj")
        sizePolicy2.setHeightForWidth(self.lab_pj.sizePolicy().hasHeightForWidth())
        self.lab_pj.setSizePolicy(sizePolicy2)
        self.lab_pj.setFont(font4)
        self.lab_pj.setStyleSheet(u"border: none; font-weight: bold;")
        self.lab_pj.setTextFormat(Qt.AutoText)
        self.lab_pj.setAlignment(Qt.AlignCenter)

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.lab_pj)

        self.fil_io = QProgressBar(self.groupBox)
        self.fil_io.setObjectName(u"fil_io")
        self.fil_io.setMaximumSize(QSize(100, 16777215))
        self.fil_io.setMaximum(1)
        self.fil_io.setValue(1)
        self.fil_io.setTextVisible(False)

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.fil_io)

        self.lab_Tlength = QLabel(self.groupBox)
        self.lab_Tlength.setObjectName(u"lab_Tlength")
        sizePolicy2.setHeightForWidth(self.lab_Tlength.sizePolicy().hasHeightForWidth())
        self.lab_Tlength.setSizePolicy(sizePolicy2)
        self.lab_Tlength.setFont(font4)
        self.lab_Tlength.setStyleSheet(u"border: none; font-weight: bold;")
        self.lab_Tlength.setTextFormat(Qt.AutoText)
        self.lab_Tlength.setAlignment(Qt.AlignCenter)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.lab_Tlength)

        self.pjnumb = QLabel(self.groupBox)
        self.pjnumb.setObjectName(u"pjnumb")
        sizePolicy2.setHeightForWidth(self.pjnumb.sizePolicy().hasHeightForWidth())
        self.pjnumb.setSizePolicy(sizePolicy2)
        self.pjnumb.setFont(font4)
        self.pjnumb.setStyleSheet(u"border: none; font-weight: bold;")
        self.pjnumb.setTextFormat(Qt.AutoText)
        self.pjnumb.setAlignment(Qt.AlignCenter)

        self.formLayout_3.setWidget(6, QFormLayout.FieldRole, self.pjnumb)

        self.lab_Tposition = QLabel(self.groupBox)
        self.lab_Tposition.setObjectName(u"lab_Tposition")
        sizePolicy2.setHeightForWidth(self.lab_Tposition.sizePolicy().hasHeightForWidth())
        self.lab_Tposition.setSizePolicy(sizePolicy2)
        self.lab_Tposition.setFont(font4)
        self.lab_Tposition.setStyleSheet(u"border: none; font-weight: bold;")
        self.lab_Tposition.setTextFormat(Qt.AutoText)
        self.lab_Tposition.setAlignment(Qt.AlignCenter)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.lab_Tposition)

        self.lab_Tstep = QLabel(self.groupBox)
        self.lab_Tstep.setObjectName(u"lab_Tstep")
        sizePolicy2.setHeightForWidth(self.lab_Tstep.sizePolicy().hasHeightForWidth())
        self.lab_Tstep.setSizePolicy(sizePolicy2)
        self.lab_Tstep.setFont(font4)
        self.lab_Tstep.setStyleSheet(u"border: none; font-weight: bold;")
        self.lab_Tstep.setTextFormat(Qt.AutoText)
        self.lab_Tstep.setAlignment(Qt.AlignCenter)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.lab_Tstep)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.pjbar = QSlider(self.layoutWidget)
        self.pjbar.setObjectName(u"pjbar")
        sizePolicy.setHeightForWidth(self.pjbar.sizePolicy().hasHeightForWidth())
        self.pjbar.setSizePolicy(sizePolicy)
        self.pjbar.setMinimum(0)
        self.pjbar.setMaximum(0)
        self.pjbar.setPageStep(5)
        self.pjbar.setValue(0)
        self.pjbar.setOrientation(Qt.Horizontal)
        self.pjbar.setTickPosition(QSlider.TicksAbove)
        self.pjbar.setTickInterval(1)

        self.verticalLayout_3.addWidget(self.pjbar)

        self.verticalSpacer_4 = QSpacerItem(10, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.groupBox_6 = QGroupBox(self.layoutWidget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy2.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy2)
        self.groupBox_6.setFont(font1)
        self.groupBox_6.setCheckable(False)
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.whichStat = QComboBox(self.groupBox_6)
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.addItem("")
        self.whichStat.setObjectName(u"whichStat")
        sizePolicy2.setHeightForWidth(self.whichStat.sizePolicy().hasHeightForWidth())
        self.whichStat.setSizePolicy(sizePolicy2)
        self.whichStat.setMinimumSize(QSize(0, 0))
        self.whichStat.setFont(font2)

        self.verticalLayout_9.addWidget(self.whichStat)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.plotStat = QPushButton(self.groupBox_6)
        self.plotStat.setObjectName(u"plotStat")
        self.plotStat.setFont(font2)

        self.horizontalLayout_2.addWidget(self.plotStat)

        self.redoStat = QPushButton(self.groupBox_6)
        self.redoStat.setObjectName(u"redoStat")
        self.redoStat.setFont(font2)

        self.horizontalLayout_2.addWidget(self.redoStat)


        self.verticalLayout_9.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.separateFamilies = QCheckBox(self.groupBox_6)
        self.separateFamilies.setObjectName(u"separateFamilies")
        self.separateFamilies.setFont(font3)
        self.separateFamilies.setChecked(True)

        self.horizontalLayout_3.addWidget(self.separateFamilies)

        self.fit_gauss = QCheckBox(self.groupBox_6)
        self.fit_gauss.setObjectName(u"fit_gauss")
        self.fit_gauss.setFont(font3)
        self.fit_gauss.setChecked(True)

        self.horizontalLayout_3.addWidget(self.fit_gauss)

        self.fit_decay = QCheckBox(self.groupBox_6)
        self.fit_decay.setObjectName(u"fit_decay")
        self.fit_decay.setFont(font3)

        self.horizontalLayout_3.addWidget(self.fit_decay)


        self.verticalLayout_9.addLayout(self.horizontalLayout_3)

        self.filter_empty = QGroupBox(self.groupBox_6)
        self.filter_empty.setObjectName(u"filter_empty")
        self.filter_empty.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.filter_empty.sizePolicy().hasHeightForWidth())
        self.filter_empty.setSizePolicy(sizePolicy2)
        self.filter_empty.setFlat(False)
        self.filter_empty.setCheckable(True)
        self.filter_empty.setChecked(False)
        self.formLayout_5 = QFormLayout(self.filter_empty)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label_33 = QLabel(self.filter_empty)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font2)

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_33)

        self.minJump = QDoubleSpinBox(self.filter_empty)
        self.minJump.setObjectName(u"minJump")
        self.minJump.setMaximum(100000.000000000000000)
        self.minJump.setSingleStep(100.000000000000000)
        self.minJump.setValue(1000.000000000000000)

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.minJump)


        self.verticalLayout_9.addWidget(self.filter_empty)

        self.lim_custom = QGroupBox(self.groupBox_6)
        self.lim_custom.setObjectName(u"lim_custom")
        self.lim_custom.setCheckable(True)
        self.lim_custom.setChecked(False)
        self.verticalLayout_10 = QVBoxLayout(self.lim_custom)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_27 = QLabel(self.lim_custom)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font2)
        self.label_27.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_27)

        self.lim_bins = QSpinBox(self.lim_custom)
        self.lim_bins.setObjectName(u"lim_bins")
        self.lim_bins.setFont(font3)
        self.lim_bins.setMinimum(0)
        self.lim_bins.setMaximum(1000000)
        self.lim_bins.setValue(10)

        self.horizontalLayout_8.addWidget(self.lim_bins)


        self.verticalLayout_10.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lim_min_range = QSpinBox(self.lim_custom)
        self.lim_min_range.setObjectName(u"lim_min_range")
        self.lim_min_range.setFont(font3)
        self.lim_min_range.setMinimum(-20000)
        self.lim_min_range.setMaximum(20000)
        self.lim_min_range.setValue(0)

        self.horizontalLayout_7.addWidget(self.lim_min_range)

        self.label_26 = QLabel(self.lim_custom)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font2)

        self.horizontalLayout_7.addWidget(self.label_26)

        self.lim_max_range = QSpinBox(self.lim_custom)
        self.lim_max_range.setObjectName(u"lim_max_range")
        self.lim_max_range.setFont(font3)
        self.lim_max_range.setMinimum(-20000)
        self.lim_max_range.setMaximum(20000)
        self.lim_max_range.setValue(0)

        self.horizontalLayout_7.addWidget(self.lim_max_range)


        self.verticalLayout_10.addLayout(self.horizontalLayout_7)


        self.verticalLayout_9.addWidget(self.lim_custom)

        self.filters_group = QGroupBox(self.groupBox_6)
        self.filters_group.setObjectName(u"filters_group")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.filters_group.sizePolicy().hasHeightForWidth())
        self.filters_group.setSizePolicy(sizePolicy3)
        self.filters_group.setCheckable(True)
        self.filters_group.setChecked(False)
        self.verticalLayout_12 = QVBoxLayout(self.filters_group)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.lim_min_detach = QSpinBox(self.filters_group)
        self.lim_min_detach.setObjectName(u"lim_min_detach")
        self.lim_min_detach.setFont(font3)
        self.lim_min_detach.setMinimum(-99999)
        self.lim_min_detach.setMaximum(99999)
        self.lim_min_detach.setValue(0)

        self.horizontalLayout_9.addWidget(self.lim_min_detach)

        self.label_28 = QLabel(self.filters_group)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font2)

        self.horizontalLayout_9.addWidget(self.label_28)

        self.lim_max_detach = QSpinBox(self.filters_group)
        self.lim_max_detach.setObjectName(u"lim_max_detach")
        self.lim_max_detach.setFont(font3)
        self.lim_max_detach.setMinimum(-99999)
        self.lim_max_detach.setMaximum(99999)
        self.lim_max_detach.setValue(2000)

        self.horizontalLayout_9.addWidget(self.lim_max_detach)


        self.verticalLayout_12.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lim_min_ntraits = QSpinBox(self.filters_group)
        self.lim_min_ntraits.setObjectName(u"lim_min_ntraits")
        self.lim_min_ntraits.setFont(font3)
        self.lim_min_ntraits.setMinimum(1)
        self.lim_min_ntraits.setMaximum(99)
        self.lim_min_ntraits.setValue(1)

        self.horizontalLayout_4.addWidget(self.lim_min_ntraits)

        self.label_19 = QLabel(self.filters_group)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font2)

        self.horizontalLayout_4.addWidget(self.label_19)

        self.lim_max_ntraits = QSpinBox(self.filters_group)
        self.lim_max_ntraits.setObjectName(u"lim_max_ntraits")
        self.lim_max_ntraits.setFont(font3)
        self.lim_max_ntraits.setMinimum(1)
        self.lim_max_ntraits.setMaximum(999)
        self.lim_max_ntraits.setValue(999)

        self.horizontalLayout_4.addWidget(self.lim_max_ntraits)


        self.verticalLayout_12.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lim_min_xtrait = QSpinBox(self.filters_group)
        self.lim_min_xtrait.setObjectName(u"lim_min_xtrait")
        self.lim_min_xtrait.setFont(font3)
        self.lim_min_xtrait.setMinimum(-9999)
        self.lim_min_xtrait.setMaximum(99999)
        self.lim_min_xtrait.setValue(-9999)

        self.horizontalLayout_5.addWidget(self.lim_min_xtrait)

        self.label_20 = QLabel(self.filters_group)
        self.label_20.setObjectName(u"label_20")
        font7 = QFont()
        font7.setBold(False)
        font7.setItalic(True)
        self.label_20.setFont(font7)

        self.horizontalLayout_5.addWidget(self.label_20)

        self.lim_max_xtrait = QSpinBox(self.filters_group)
        self.lim_max_xtrait.setObjectName(u"lim_max_xtrait")
        self.lim_max_xtrait.setFont(font3)
        self.lim_max_xtrait.setMinimum(-9999)
        self.lim_max_xtrait.setMaximum(99999)
        self.lim_max_xtrait.setValue(99999)

        self.horizontalLayout_5.addWidget(self.lim_max_xtrait)


        self.verticalLayout_12.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lim_min_length = QSpinBox(self.filters_group)
        self.lim_min_length.setObjectName(u"lim_min_length")
        self.lim_min_length.setFont(font3)
        self.lim_min_length.setMaximum(99999)
        self.lim_min_length.setValue(0)

        self.horizontalLayout_6.addWidget(self.lim_min_length)

        self.label_21 = QLabel(self.filters_group)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font7)

        self.horizontalLayout_6.addWidget(self.label_21)

        self.lim_max_length = QSpinBox(self.filters_group)
        self.lim_max_length.setObjectName(u"lim_max_length")
        self.lim_max_length.setFont(font3)
        self.lim_max_length.setMaximum(99999)
        self.lim_max_length.setValue(99999)

        self.horizontalLayout_6.addWidget(self.lim_max_length)


        self.verticalLayout_12.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.lim_isJump = QCheckBox(self.filters_group)
        self.lim_isJump.setObjectName(u"lim_isJump")
        self.lim_isJump.setFont(font7)
        self.lim_isJump.setChecked(True)

        self.horizontalLayout_10.addWidget(self.lim_isJump)

        self.lim_isPlat = QCheckBox(self.filters_group)
        self.lim_isPlat.setObjectName(u"lim_isPlat")
        self.lim_isPlat.setFont(font7)
        self.lim_isPlat.setChecked(True)

        self.horizontalLayout_10.addWidget(self.lim_isPlat)


        self.verticalLayout_12.addLayout(self.horizontalLayout_10)


        self.verticalLayout_9.addWidget(self.filters_group)

        self.verticalSpacer_6 = QSpacerItem(20, 24, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_6)


        self.horizontalLayout.addWidget(self.groupBox_6)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.splitter_2.addWidget(self.layoutWidget)

        self.verticalLayout_8.addWidget(self.splitter_2)

        facewindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(facewindow)
        self.statusBar.setObjectName(u"statusBar")
        facewindow.setStatusBar(self.statusBar)

        self.retranslateUi(facewindow)

        QMetaObject.connectSlotsByName(facewindow)
    # setupUi

    def retranslateUi(self, facewindow):
        facewindow.setWindowTitle(QCoreApplication.translate("facewindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.grafo.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.grafo.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.grafo.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.groupBox_4.setTitle(QCoreApplication.translate("facewindow", u"View", None))
        self.radio_area.setText(QCoreApplication.translate("facewindow", u"Area", None))
        self.radio_deriv.setText(QCoreApplication.translate("facewindow", u"Derivative", None))
        self.radio_view.setText(QCoreApplication.translate("facewindow", u"Curve", None))
        self.radio_smooth.setText(QCoreApplication.translate("facewindow", u"Smooth", None))
        self.radio_traits.setText(QCoreApplication.translate("facewindow", u"Traits", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("facewindow", u"Actions", None))
        self.bAddFile.setText(QCoreApplication.translate("facewindow", u"Load one file", None))
        self.bAddFiles.setText(QCoreApplication.translate("facewindow", u"Load Files", None))
        self.bAddDir.setText(QCoreApplication.translate("facewindow", u"Load DIR", None))
        self.bReset.setText(QCoreApplication.translate("facewindow", u"Reset", None))
        self.bDoSave.setText(QCoreApplication.translate("facewindow", u"Do stats and save", None))
        self.famGroup.setTitle(QCoreApplication.translate("facewindow", u"Families", None))
        self.bAddFamily.setText(QCoreApplication.translate("facewindow", u"ADD", None))
        self.label_24.setText(QCoreApplication.translate("facewindow", u"Families", None))
        self.cNumFam.setText(QCoreApplication.translate("facewindow", u"1", None))
        self.label_25.setText(QCoreApplication.translate("facewindow", u"Family", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("facewindow", u"Segmentation", None))
        self.label.setText(QCoreApplication.translate("facewindow", u"Thresh (std)", None))
        self.label_2.setText(QCoreApplication.translate("facewindow", u"MinLen [nm]", None))
        self.label_3.setText(QCoreApplication.translate("facewindow", u"Window", None))
        self.label_4.setText(QCoreApplication.translate("facewindow", u"Slope (\u00b0)", None))
        self.label_5.setText(QCoreApplication.translate("facewindow", u"Zdist [nm]", None))
        self.label_6.setText(QCoreApplication.translate("facewindow", u"LastTH [pN]", None))
        self.label_7.setText(QCoreApplication.translate("facewindow", u"TraitsOrder", None))
        self.btn_flatten.setText(QCoreApplication.translate("facewindow", u"Flatten", None))
        self.btn_recalibrate.setText(QCoreApplication.translate("facewindow", u"Recalibrate", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("facewindow", u"Curve", None))
        self.label_8.setText(QCoreApplication.translate("facewindow", u"N-segments", None))
        self.lab_N.setText(QCoreApplication.translate("facewindow", u"0", None))
        self.label_9.setText(QCoreApplication.translate("facewindow", u"N-plateaux", None))
        self.lab_Np.setText(QCoreApplication.translate("facewindow", u"0", None))
        self.label_10.setText(QCoreApplication.translate("facewindow", u"N-jumps", None))
        self.lab_Nj.setText(QCoreApplication.translate("facewindow", u"0", None))
        self.label_11.setText(QCoreApplication.translate("facewindow", u"N-out", None))
        self.lab_Nblue.setText(QCoreApplication.translate("facewindow", u"0", None))
        self.label_18.setText(QCoreApplication.translate("facewindow", u"Area method", None))
        self.reflatten.setText(QCoreApplication.translate("facewindow", u"Reflatten", None))
        self.label_13.setText(QCoreApplication.translate("facewindow", u"Area", None))
        self.lcd_Area.setText(QCoreApplication.translate("facewindow", u"0.00 zJ", None))
        self.label_22.setText(QCoreApplication.translate("facewindow", u"Height", None))
        self.lcd_hieght.setText(QCoreApplication.translate("facewindow", u"0 nm", None))
        self.sslabel_4.setText(QCoreApplication.translate("facewindow", u"Number", None))
        self.cnumb.setText(QCoreApplication.translate("facewindow", u"1", None))
        self.label_12.setText(QCoreApplication.translate("facewindow", u"Scope", None))
        self.cscope.setText(QCoreApplication.translate("facewindow", u"General", None))
        self.label_23.setText(QCoreApplication.translate("facewindow", u"Family", None))
        self.label_29.setText(QCoreApplication.translate("facewindow", u"Detach X", None))
        self.lcd_detX.setText(QCoreApplication.translate("facewindow", u"0 nm", None))
        self.label_30.setText(QCoreApplication.translate("facewindow", u"Detach F", None))
        self.lcd_detF.setText(QCoreApplication.translate("facewindow", u"0 pN", None))
        self.label_31.setText(QCoreApplication.translate("facewindow", u"J-Area end", None))
        self.arBlue.setText(QCoreApplication.translate("facewindow", u"B", None))
        self.arGreen.setText(QCoreApplication.translate("facewindow", u"G", None))
        self.label_32.setText(QCoreApplication.translate("facewindow", u"Jump area", None))
        self.lcd_JArea.setText(QCoreApplication.translate("facewindow", u"0.00 zJ", None))
        self.label_34.setText(QCoreApplication.translate("facewindow", u"Stretch lim", None))
        self.label_35.setText(QCoreApplication.translate("facewindow", u"Stretch area", None))
        self.lcd_strA.setText(QCoreApplication.translate("facewindow", u"0.00 zJ", None))
        self.btn_popout.setText(QCoreApplication.translate("facewindow", u"POP OUT", None))
        self.groupBox.setTitle(QCoreApplication.translate("facewindow", u"Segment", None))
        self.sslabel.setText(QCoreApplication.translate("facewindow", u"Position", None))
        self.label_14.setText(QCoreApplication.translate("facewindow", u"Length", None))
        self.label_15.setText(QCoreApplication.translate("facewindow", u"Step size", None))
        self.label_16.setText(QCoreApplication.translate("facewindow", u"Slope", None))
        self.label_17.setText(QCoreApplication.translate("facewindow", u"Type", None))
        self.sslabel_2.setText(QCoreApplication.translate("facewindow", u"Accept", None))
        self.sslabel_3.setText(QCoreApplication.translate("facewindow", u"Number", None))
        self.lab_Tslope.setText(QCoreApplication.translate("facewindow", u"0.00", None))
        self.lab_pj.setText(QCoreApplication.translate("facewindow", u"Plateaux", None))
        self.lab_Tlength.setText(QCoreApplication.translate("facewindow", u"0.00", None))
        self.pjnumb.setText(QCoreApplication.translate("facewindow", u"1", None))
        self.lab_Tposition.setText(QCoreApplication.translate("facewindow", u"0.00", None))
        self.lab_Tstep.setText(QCoreApplication.translate("facewindow", u"0.00", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("facewindow", u"Statistics", None))
        self.whichStat.setItemText(0, QCoreApplication.translate("facewindow", u"ADHESION [pN]", None))
        self.whichStat.setItemText(1, QCoreApplication.translate("facewindow", u"Stretch AREA [fJ]", None))
        self.whichStat.setItemText(2, QCoreApplication.translate("facewindow", u"DETACH-X [nm]", None))
        self.whichStat.setItemText(3, QCoreApplication.translate("facewindow", u"DETACH-F [pN]", None))
        self.whichStat.setItemText(4, QCoreApplication.translate("facewindow", u"AREA [fJ]", None))
        self.whichStat.setItemText(5, QCoreApplication.translate("facewindow", u"Jump SLOPE [pN/nm]", None))
        self.whichStat.setItemText(6, QCoreApplication.translate("facewindow", u"NTRAITS", None))
        self.whichStat.setItemText(7, QCoreApplication.translate("facewindow", u"NJUMPS", None))
        self.whichStat.setItemText(8, QCoreApplication.translate("facewindow", u"NPLATEAUX", None))
        self.whichStat.setItemText(9, QCoreApplication.translate("facewindow", u"Max Step [pN]", None))
        self.whichStat.setItemText(10, QCoreApplication.translate("facewindow", u"Segments LENGTH [nm]", None))
        self.whichStat.setItemText(11, QCoreApplication.translate("facewindow", u"Segments POSITION [nm]", None))
        self.whichStat.setItemText(12, QCoreApplication.translate("facewindow", u"Segments STEP [pN]", None))
        self.whichStat.setItemText(13, QCoreApplication.translate("facewindow", u"Segments SLOPE [pN/nm]", None))

        self.plotStat.setText(QCoreApplication.translate("facewindow", u"Plot stats", None))
        self.redoStat.setText(QCoreApplication.translate("facewindow", u"Redo Stats", None))
        self.separateFamilies.setText(QCoreApplication.translate("facewindow", u"Families", None))
#if QT_CONFIG(tooltip)
        self.fit_gauss.setToolTip(QCoreApplication.translate("facewindow", u"ciao", None))
#endif // QT_CONFIG(tooltip)
        self.fit_gauss.setText(QCoreApplication.translate("facewindow", u"Gauss Fit", None))
        self.fit_decay.setText(QCoreApplication.translate("facewindow", u"Decay Fit", None))
        self.filter_empty.setTitle(QCoreApplication.translate("facewindow", u"Filter empty", None))
        self.label_33.setText(QCoreApplication.translate("facewindow", u"Min jump [pN]", None))
        self.lim_custom.setTitle(QCoreApplication.translate("facewindow", u"Customize", None))
#if QT_CONFIG(tooltip)
        self.label_27.setToolTip(QCoreApplication.translate("facewindow", u"Number of GOOD traits to be filtered", None))
#endif // QT_CONFIG(tooltip)
        self.label_27.setText(QCoreApplication.translate("facewindow", u"Bins", None))
#if QT_CONFIG(tooltip)
        self.label_26.setToolTip(QCoreApplication.translate("facewindow", u"Number of GOOD traits to be filtered", None))
#endif // QT_CONFIG(tooltip)
        self.label_26.setText(QCoreApplication.translate("facewindow", u"< Value <", None))
        self.filters_group.setTitle(QCoreApplication.translate("facewindow", u"Filters", None))
#if QT_CONFIG(tooltip)
        self.label_28.setToolTip(QCoreApplication.translate("facewindow", u"Number of GOOD traits to be filtered", None))
#endif // QT_CONFIG(tooltip)
        self.label_28.setText(QCoreApplication.translate("facewindow", u"< xDetach <", None))
#if QT_CONFIG(tooltip)
        self.label_19.setToolTip(QCoreApplication.translate("facewindow", u"Number of GOOD traits to be filtered", None))
#endif // QT_CONFIG(tooltip)
        self.label_19.setText(QCoreApplication.translate("facewindow", u"< NTraits <", None))
#if QT_CONFIG(tooltip)
        self.label_20.setToolTip(QCoreApplication.translate("facewindow", u"Position of the first point of the trait, for filtering", None))
#endif // QT_CONFIG(tooltip)
        self.label_20.setText(QCoreApplication.translate("facewindow", u"< xTrait <", None))
#if QT_CONFIG(tooltip)
        self.label_21.setToolTip(QCoreApplication.translate("facewindow", u"Lenght of the trait", None))
#endif // QT_CONFIG(tooltip)
        self.label_21.setText(QCoreApplication.translate("facewindow", u"< Length <", None))
        self.lim_isJump.setText(QCoreApplication.translate("facewindow", u"Jump", None))
        self.lim_isPlat.setText(QCoreApplication.translate("facewindow", u"Plateaux", None))
    # retranslateUi

