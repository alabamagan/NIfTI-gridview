from .reader import *
from .writer import *
from PySide2.QtCore import QThread, Signal

class ngv_io_reader_wrapper(QThread):
    """
    This class is the worker thread that handles image io.

    Args:
        parent (QObject, Optional): Parent of the object.

    Signals:
        update_progress(int)

    Attributes:
        _reader (ngv_io.reader):
            Private reader object
    """
    update_progress = Signal(int)
    update_view_list = Signal(str)
    error_msg = Signal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self._reader = None

    def configure_reader(self, *args, **kwargs):
        self._reader = reader(*args, **kwargs)

    def read_all_targets(self):
        assert self._reader is not None, "Reader is not configured!"

        l = len(self._reader)
        for i in range(len(self._reader)):
            self._reader._read_file(i)
            self.update_progress.emit((100 * i ) // l)
            self.update_view_list.emit(list(self._reader._files.keys())[i])

    def __getitem__(self, item):
        if not self._reader is None:
            return self._reader.__getitem__(item)

    def run(self):
        try:
            self.read_all_targets()
        except:
            self.error_msg(self.tr("Reader encounters error..."))

class ngv_io_writer_wrapper(QThread):
    """
    This class is the worker thread that handles writing images
    """
    update_progress = Signal(int)
    error_msg = Signal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self._writer = None

    def configure_writer(self, *args, **kwargs):
        self._writer = writer(*args , **kwargs)