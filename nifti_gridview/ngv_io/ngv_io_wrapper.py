from .reader import *
from .writer import *
from PySide2.QtCore import QThread, Signal
from ngv_model import NGV_Logger

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
    display_msg = Signal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self._reader = None
        self._logger = NGV_Logger[__class__.__name__]

    def configure_reader(self, *args, **kwargs):
        self._reader = reader(*args, **kwargs)

    def read_all_targets(self):
        assert self._reader is not None, "Reader is not configured!"

        l = len(self._reader)
        for i in range(len(self._reader)):
            self._reader._read_file(i)
            self.update_progress.emit((100 * i ) // l)
            self.update_view_list.emit(list(self._reader._files.keys())[i])
        self.display_msg.emit("Ready.")

    def get_all_file_names(self):
        return self._reader.get_item_names()

    def get_all_file_ids(self):
        return self._reader.get_item_ids()

    def has_key(self, item):
        """
        Check if item exist and can be getted without actually loading it.

        Args:
            item (str): Item Key.

        Returns:
            bool
        """
        return self._reader.has_key(item)

    def __getitem__(self, item):
        if not self._reader is None:
            return self._reader.__getitem__(item)

    def __iter__(self):
        N = len(self._reader)
        for i, (key, im) in enumerate(self._reader):
            self.update_progress.emit((100 * i) // N)
            self.display_msg.emit(self.tr("Reading ") + key)
            self._logger.info("Reading {}".format(key))
            yield key, im

    def run(self):
        try:
            self.read_all_targets()
        except Exception as e:
            self.display_msg.emit(self.tr("Reader encounters error..."))
            self._logger.error("Reader encounters exception: {}".format(e))
            self._logger.log_traceback(e)


class ngv_io_writer_wrapper(QThread):
    """
    This class is the worker thread that handles writing images. Note that writing progress is updated from reader
    signal emission.
    """
    update_progress = Signal(int)
    display_msg = Signal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self._writer = None

    def configure_writer(self, *args, **kwargs):
        self._writer = writer(*args , **kwargs)

    def run(self):
        try:
            self._writer.write()
        except Exception as e:
            self._logger.error("Writer encounter exception: {}".format(e))
            self._logger.log_traceback(e)
            self.display_msg.emit(self.tr("Writer encounters error: {}".format(e)))