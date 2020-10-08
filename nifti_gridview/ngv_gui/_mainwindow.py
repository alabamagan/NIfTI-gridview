# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_ngv_mainwindow(object):
    def setupUi(self, ngv_mainwindow):
        ngv_mainwindow.setObjectName("ngv_mainwindow")
        ngv_mainwindow.resize(965, 731)
        self.centralwidget = QtWidgets.QWidget(ngv_mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(200, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(250, 16777215))
        self.tabWidget.setObjectName("tabWidget")
        self.files_tab = QtWidgets.QWidget()
        self.files_tab.setObjectName("files_tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.files_tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.files_listWidget = QtWidgets.QListWidget(self.files_tab)
        self.files_listWidget.setObjectName("files_listWidget")
        self.verticalLayout.addWidget(self.files_listWidget)
        self.tabWidget.addTab(self.files_tab, "")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolBox = QtWidgets.QToolBox(self.widget)
        self.toolBox.setObjectName("toolBox")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 197, 257))
        self.page_3.setObjectName("page_3")
        self.layoutWidget = QtWidgets.QWidget(self.page_3)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 10, 203, 238))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.spinBox_nrow = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_nrow.setEnabled(False)
        self.spinBox_nrow.setMinimum(1)
        self.spinBox_nrow.setProperty("value", 5)
        self.spinBox_nrow.setObjectName("spinBox_nrow")
        self.gridLayout.addWidget(self.spinBox_nrow, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.checkBox_autonrow = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_autonrow.setChecked(True)
        self.checkBox_autonrow.setObjectName("checkBox_autonrow")
        self.gridLayout.addWidget(self.checkBox_autonrow, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.checkBox_highres = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_highres.setObjectName("checkBox_highres")
        self.gridLayout.addWidget(self.checkBox_highres, 6, 0, 1, 1)
        self.spinBox_padding = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_padding.setProperty("value", 1)
        self.spinBox_padding.setObjectName("spinBox_padding")
        self.gridLayout.addWidget(self.spinBox_padding, 2, 1, 1, 1)
        self.spinBox_offset = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_offset.setObjectName("spinBox_offset")
        self.gridLayout.addWidget(self.spinBox_offset, 0, 1, 1, 1)
        self.checkBox_userange = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_userange.setObjectName("checkBox_userange")
        self.gridLayout.addWidget(self.checkBox_userange, 5, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBox_drawrange_upper = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_drawrange_upper.setEnabled(False)
        self.spinBox_drawrange_upper.setMinimum(2)
        self.spinBox_drawrange_upper.setMaximum(999)
        self.spinBox_drawrange_upper.setObjectName("spinBox_drawrange_upper")
        self.gridLayout.addWidget(self.spinBox_drawrange_upper, 4, 2, 1, 1)
        self.spinBox_drawrange_lower = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_drawrange_lower.setEnabled(False)
        self.spinBox_drawrange_lower.setObjectName("spinBox_drawrange_lower")
        self.gridLayout.addWidget(self.spinBox_drawrange_lower, 4, 1, 1, 1)
        self.doubleSpinBox_line_thickness = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_line_thickness.setMaximum(5.0)
        self.doubleSpinBox_line_thickness.setProperty("value", 2.0)
        self.doubleSpinBox_line_thickness.setObjectName("doubleSpinBox_line_thickness")
        self.gridLayout.addWidget(self.doubleSpinBox_line_thickness, 3, 1, 1, 1)
        self.label_line_thickness = QtWidgets.QLabel(self.layoutWidget)
        self.label_line_thickness.setObjectName("label_line_thickness")
        self.gridLayout.addWidget(self.label_line_thickness, 3, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 84, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.toolBox.addItem(self.page_3, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 197, 286))
        self.page_4.setObjectName("page_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.page_4)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 1, 1, 1)
        self.comboBox_cmap = QtWidgets.QComboBox(self.page_4)
        self.comboBox_cmap.setObjectName("comboBox_cmap")
        self.gridLayout_2.addWidget(self.comboBox_cmap, 0, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.checkBox_show_slides_with_seg = QtWidgets.QCheckBox(self.page_4)
        self.checkBox_show_slides_with_seg.setEnabled(False)
        self.checkBox_show_slides_with_seg.setObjectName("checkBox_show_slides_with_seg")
        self.verticalLayout_3.addWidget(self.checkBox_show_slides_with_seg)
        self.line = QtWidgets.QFrame(self.page_4)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.label_6 = QtWidgets.QLabel(self.page_4)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.tableWidget_segmentations = QtWidgets.QTableWidget(self.page_4)
        self.tableWidget_segmentations.setColumnCount(2)
        self.tableWidget_segmentations.setObjectName("tableWidget_segmentations")
        self.tableWidget_segmentations.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_segmentations.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_segmentations.setHorizontalHeaderItem(1, item)
        self.tableWidget_segmentations.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_segmentations.horizontalHeader().setDefaultSectionSize(40)
        self.tableWidget_segmentations.horizontalHeader().setMinimumSectionSize(25)
        self.tableWidget_segmentations.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.tableWidget_segmentations)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_alpha = QtWidgets.QLabel(self.page_4)
        self.label_alpha.setObjectName("label_alpha")
        self.gridLayout_3.addWidget(self.label_alpha, 0, 0, 1, 1)
        self.doubleSpinBox_alpha = QtWidgets.QDoubleSpinBox(self.page_4)
        self.doubleSpinBox_alpha.setMaximum(1.0)
        self.doubleSpinBox_alpha.setSingleStep(0.1)
        self.doubleSpinBox_alpha.setProperty("value", 0.8)
        self.doubleSpinBox_alpha.setObjectName("doubleSpinBox_alpha")
        self.gridLayout_3.addWidget(self.doubleSpinBox_alpha, 0, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 208, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.toolBox.addItem(self.page_4, "")
        self.verticalLayout_2.addWidget(self.toolBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 308, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.tabWidget.addTab(self.widget, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setMinimumSize(QtCore.QSize(720, 0))
        self.image_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.image_label.setText("")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.horizontalLayout.addWidget(self.image_label)
        ngv_mainwindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ngv_mainwindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 965, 21))
        self.menubar.setObjectName("menubar")
        self.menuFiles = QtWidgets.QMenu(self.menubar)
        self.menuFiles.setObjectName("menuFiles")
        ngv_mainwindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ngv_mainwindow)
        self.statusbar.setObjectName("statusbar")
        ngv_mainwindow.setStatusBar(self.statusbar)
        self.actionOpen_Folder = QtWidgets.QAction(ngv_mainwindow)
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")
        self.actionOpen_Segmentation_Folder = QtWidgets.QAction(ngv_mainwindow)
        self.actionOpen_Segmentation_Folder.setEnabled(False)
        self.actionOpen_Segmentation_Folder.setObjectName("actionOpen_Segmentation_Folder")
        self.actionSave_Configuration = QtWidgets.QAction(ngv_mainwindow)
        self.actionSave_Configuration.setEnabled(False)
        self.actionSave_Configuration.setObjectName("actionSave_Configuration")
        self.actionExport_Images = QtWidgets.QAction(ngv_mainwindow)
        self.actionExport_Images.setObjectName("actionExport_Images")
        self.menuFiles.addAction(self.actionOpen_Folder)
        self.menuFiles.addAction(self.actionOpen_Segmentation_Folder)
        self.menuFiles.addAction(self.actionSave_Configuration)
        self.menuFiles.addAction(self.actionExport_Images)
        self.menubar.addAction(self.menuFiles.menuAction())

        self.retranslateUi(ngv_mainwindow)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ngv_mainwindow)

    def retranslateUi(self, ngv_mainwindow):
        _translate = QtCore.QCoreApplication.translate
        ngv_mainwindow.setWindowTitle(_translate("ngv_mainwindow", "NIfTI-gridvew"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.files_tab), _translate("ngv_mainwindow", "Files"))
        self.label_3.setText(_translate("ngv_mainwindow", "Padding:"))
        self.label_5.setText(_translate("ngv_mainwindow", "Draw Range:"))
        self.checkBox_autonrow.setText(_translate("ngv_mainwindow", "Auto"))
        self.label.setText(_translate("ngv_mainwindow", "Offset:"))
        self.checkBox_highres.setText(_translate("ngv_mainwindow", "High Res"))
        self.checkBox_userange.setText(_translate("ngv_mainwindow", "Use Range"))
        self.label_2.setText(_translate("ngv_mainwindow", "Nrow:"))
        self.label_line_thickness.setText(_translate("ngv_mainwindow", "Line thickness:"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("ngv_mainwindow", "General Options"))
        self.label_4.setText(_translate("ngv_mainwindow", "Colormap: "))
        self.checkBox_show_slides_with_seg.setText(_translate("ngv_mainwindow", "Show slices with segment only."))
        self.label_6.setText(_translate("ngv_mainwindow", "Segmentation:"))
        item = self.tableWidget_segmentations.horizontalHeaderItem(0)
        item.setText(_translate("ngv_mainwindow", "Color"))
        item = self.tableWidget_segmentations.horizontalHeaderItem(1)
        item.setText(_translate("ngv_mainwindow", "Segmentation"))
        self.label_alpha.setText(_translate("ngv_mainwindow", "Contour Alpha"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("ngv_mainwindow", "Image Options"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("ngv_mainwindow", "Toolbox"))
        self.menuFiles.setTitle(_translate("ngv_mainwindow", "Files"))
        self.actionOpen_Folder.setText(_translate("ngv_mainwindow", "Open Folder"))
        self.actionOpen_Segmentation_Folder.setText(_translate("ngv_mainwindow", "Open Segmentation Folder"))
        self.actionSave_Configuration.setText(_translate("ngv_mainwindow", "Save Configuration"))
        self.actionExport_Images.setText(_translate("ngv_mainwindow", "Export Images..."))
