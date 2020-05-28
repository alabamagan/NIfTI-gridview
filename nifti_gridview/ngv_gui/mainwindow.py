import sys
from PySide2.QtWidgets import QMainWindow, QWidget, QProgressBar, QHBoxLayout, QSpacerItem, QFileDialog
from PySide2.QtCore import SIGNAL, SLOT, Signal, Slot, QStringListModel
from PySide2.QtGui import QImage, QPixmap
from ._mainwindow import *
from ngv_io import ngv_io_reader_wrapper
from visualization import draw_grid_wrapper

import numpy as np
import cv2
import logging as lg

class ngv_mainwindow(QMainWindow, QWidget):
    def __init__(self,parent=None):
        super(ngv_mainwindow, self).__init__(parent)
        self.ui = Ui_ngv_mainwindow()
        self.ui.setupUi(self)

        # Add progress bar to statusbar
        self._status_bar = self.statusBar()
        self._progress_bar = QProgressBar(self.statusBar())
        self._progress_bar.setMaximumWidth(200)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setValue(100)
        self.statusBar().showMessage('Ready')
        self.statusBar().addPermanentWidget(self._progress_bar)

        self._image_cache = {}

        #TODO: Logger

        # self.ui.files_listWidget.additem
        # Manual bar
        # - Open folder
        # - Open folder for segmentations
        # - Save configurations
        # - Export images
        # self.main_menu = self.menuBar()
        # self._file_OpenFolder = self.main_menu.addMe

        # Left panel
        # - Toolbox
        # - Listview of images

        # set up UI layouts
        # self._left_panel = QStackedLayout()
        self.connect(self.ui.actionOpen_Folder, SIGNAL('triggered()'), self, SLOT('_action_openfolder()'))

        # self.status=self.statusBar()

        # Set up io object
        self.io_wrapper = ngv_io_reader_wrapper(self)
        self.connect(self.io_wrapper, SIGNAL('update_progress(int)'), self, SLOT('_update_progress(int)'))
        self.connect(self.io_wrapper, SIGNAL('error_msg(str)'), self._status_bar, SLOT('showMessage(str)'))
        self.draw_worker = draw_grid_wrapper(self)
        self.connect(self.draw_worker, SIGNAL('error_msg(str)'), self._status_bar, SLOT('showMessage(str)'))

        # Set up drawer
        self.connect(self.ui.files_listWidget, SIGNAL('itemSelectionChanged()'), self, SLOT('_update_image_data()'))


        # connect spinbox
        self.checkbox_connectionmap = {self.ui.checkBox_userange: [self.ui.spinBox_drawrange_lower,
                                                                   self.ui.spinBox_drawrange_upper],
                                       self.ui.checkBox_autonrow: [self.ui.spinBox_nrow]}
        self.connect(self.ui.checkBox_autonrow, SIGNAL('stateChanged(int)'), self, SLOT('_toggle_checkboxes()'))
        self.connect(self.ui.checkBox_userange, SIGNAL('stateChanged(int)'), self, SLOT('_toggle_checkboxes()'))
        self.connect(self.ui.checkBox_autonrow, SIGNAL('stateChanged(int)'), self, SLOT('_update_image_data()'))
        self.connect(self.ui.checkBox_userange, SIGNAL('stateChanged(int)'), self, SLOT('_update_image_data()'))
        self.connect(self.ui.spinBox_nrow, SIGNAL('valueChanged(int)'), self, SLOT('_update_image_data()'))
        self.connect(self.ui.spinBox_offset,SIGNAL('valueChanged(int)'), self, SLOT('_update_image_data()'))
        self.connect(self.ui.spinBox_drawrange_upper,SIGNAL('valueChanged(int)'), self, SLOT('_update_image_data()'))
        self.connect(self.ui.spinBox_drawrange_lower,SIGNAL('valueChanged(int)'), self, SLOT('_update_image_data()'))
        self.connect(self.ui.spinBox_padding,SIGNAL('valueChanged(int)'), self, SLOT('_update_image_data()'))


    def _toggle_checkboxes(self):
        target = self.checkbox_connectionmap[self.sender()]
        for spinbox in target:
            if spinbox.isEnabled():
                spinbox.setEnabled(False)
            else:
                spinbox.setEnabled(True)


    def _update_progress(self, val):
        self._progress_bar.setDisabled(False)
        self._progress_bar.setValue(val)
        if val == 100:
            self._status_bar.showMessage('Ready')


    def _update_file_list_view(self):
        """
        Push file names keys into the list view.
        """
        self.ui.files_listWidget.clear()
        for key in self.io_wrapper._reader._files.keys():
            self.ui.files_listWidget.addItem(key)
        self.ui.files_listWidget.sortItems()


    def _action_openfolder(self):
        """
        Read nii.gz and push items into list view widget.
        """

        fd = QFileDialog(self)
        reader_root_dir = fd.getExistingDirectory(self, self.tr("Open"),
                                                  '/home/***REMOVED***/Source/Repos/***REMOVED***_Segmentation/***REMOVED***_Segmentation',
                                                  QFileDialog.ShowDirsOnly)
        self.io_wrapper.configure_reader(reader_root_dir, True)
        self._update_file_list_view()

    def _update_image_data(self):
        """Triggered when list widget item changed. Load image into cache."""
        active_file = self.ui.files_listWidget.selectedItems()[0].text()
        target_im = self.io_wrapper[active_file]

        # Handle display range
        if  self.ui.checkBox_userange.isChecked():
            # Range check
            display_lrange = self.ui.spinBox_drawrange_lower.value()
            display_urange = self.ui.spinBox_drawrange_upper.value()
            self.ui.spinBox_drawrange_lower.setMaximum(display_urange - 2)
            self.ui.spinBox_drawrange_upper.setMinimum(display_lrange + 2)
            self.ui.spinBox_drawrange_upper.setMaximum(target_im.shape[0] - 1)
            target_im = target_im[display_lrange:display_urange + 1]
        else:
            # Resume original range if not checked
            self.ui.spinBox_drawrange_lower.blockSignals(True)
            self.ui.spinBox_drawrange_upper.blockSignals(True)
            self.ui.spinBox_drawrange_lower.setValue(0)
            self.ui.spinBox_drawrange_upper.setValue(target_im.shape[0] - 1)
            self.ui.spinBox_drawrange_lower.blockSignals(False)
            self.ui.spinBox_drawrange_upper.blockSignals(False)


        # calculate nrow if auto checked
        if self.ui.checkBox_autonrow.isChecked():
            nrow = int(np.sqrt(target_im.shape[0]))
        else:
            nrow = self.ui.spinBox_nrow.value()

        config = {
            'target_im': target_im,
            'nrow': nrow,
            'offset': self.ui.spinBox_offset.value(),
            'margins': self.ui.spinBox_padding.value()
        }
        self.draw_worker.set_config(config)
        self.draw_worker.run()

        # convert result to QT
        displayim = self.draw_worker.get_result()
        qImg = self._np_to_QPixmap(displayim)
        self._image_cache[active_file] = qImg
        self._image_cache['current'] = qImg

        # TODO: Cahce this image data somewhere, display and scale on another slot, also triggered by scaling.
        self.ui.image_label.setPixmap(qImg.scaledToHeight(self.ui.image_label.height()))

    def resizeEvent(self, *args, **kwargs):
        """Inherit and change behavior for resizing"""
        super(ngv_mainwindow, self).resizeEvent(*args, **kwargs)
        if 'current' in self._image_cache:
            pixmap = self._image_cache['current']
            self.ui.image_label.setPixmap(pixmap.scaledToHeight(self.ui.image_label.height()))

    @staticmethod
    def _np_to_QPixmap(inim):
        """Convert numpy uint8 image to QPixmap"""
        assert isinstance(inim, np.ndarray), "Incorrect input type!"
        height, width, channel = inim.shape
        bytesPerLine = 3 * width
        qImg = QPixmap(QImage(inim, width, height, bytesPerLine, QImage.Format_RGB888))
        return qImg
