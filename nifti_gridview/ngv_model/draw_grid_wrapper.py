from PySide2.QtCore import QThread, Signal, Slot, SLOT, SIGNAL
from .draw_grid import *
from ngv_model.ngv_logger import ngv_logger

class draw_grid_wrapper(QThread):
    display_msg = Signal(str)

    def __init__(self, parent=None):
        QThread.__init__(self)

        self._config = None
        self._result = None

    def set_config(self, config):
        self._config = config

    def update_config(self, config):
        self._config.update(config)

    def run(self):
        assert not self._config is None
        try:
            target_im = self._config.pop('target_im')

            self._result = draw_grid(target_im, **self._config)
            if 'segment' in self._config and 'segment_color' in self._config:
                for ss, ss_color in zip(self._config['segment'], self._config['segment_color']):
                    if ss is None:
                        continue
                    self._result = draw_grid_contour(self._result, ss, color=ss_color, **self._config)
        except AttributeError:
            ngv_logger.global_log("Error while loading with config {}, cannot load according to "
                                  "configuration.".format(self._config))
            self.display_msg.emit(self.tr("Wrong drawing configuration"))
        except Exception as e:
            ngv_logger.global_log("Encountered unknown error: {}".format(e))

    def get_result(self):
        return self._result