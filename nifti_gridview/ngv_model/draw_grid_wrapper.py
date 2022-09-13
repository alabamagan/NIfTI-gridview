from PySide2.QtCore import QThread, Signal, Slot, SLOT, SIGNAL
from .draw_grid import *
from ngv_model.ngv_logger import NGV_Logger

class draw_grid_wrapper(QThread):
    display_msg = Signal(str)

    def __init__(self, parent=None):
        QThread.__init__(self)

        self._config = None
        self._result = None
        self._logger = NGV_Logger[__class__.__name__]

    def set_config(self, config):
        self._config = config

    def update_config(self, config):
        self._config.update(config)

    def run(self):
        assert not self._config is None
        try:
            # Options to draw only slices with segmentations.
            if self._config['seg_only'] and 'segment' in self._config:
                _sl = None
                for sl in self._config['segment']:
                    if sl is None:
                        continue
                    else:
                        _sl = sl
                        break
                try:
                    first_seg = _sl
                    slices_to_show = (first_seg.sum(axis=-1).sum(axis=-1) != 0)
                except:
                    slices_to_show = slice(None)
                    self._logger.warning("Segmentation not found.")
            else:
                slices_to_show = slice(None)

            target_im = self._config.pop('target_im')

            # TODO: Make this into tunable items
            # crop target im
            
            #should be already set in mainwindow.py
            #display_size = [200,200]
            #self._config['crop'] = {'center':[215, 256], 'size': display_size}

            try:
                self._result = draw_grid(target_im[slices_to_show], **self._config)
            except Exception as e:
                self._logger.exception("Draw grid encounter error.")

            if 'segment' in self._config and 'segment_color' in self._config:
                in_segs = []
                in_colors = []
                for ss, ss_color in zip(self._config['segment'], self._config['segment_color']):
                    if ss is None:
                        continue
                    in_segs.append(ss[slices_to_show])
                    in_colors.append(ss_color)
                self._result = draw_grid_contour(self._result, in_segs, color=in_colors, **self._config)
            del target_im

        except AttributeError:
            self._logger.log_traceback("Error while loading with config {}, cannot load according to "
                                  "configuration.".format(self._config))
            self.display_msg.emit(self.tr("Wrong drawing configuration"))
        except Exception as e:
            self._logger.log_traceback("Encountered unknown error: {}".format(e))
            self.display_msg.emit(self.tr("Unknown error."))

    def get_result(self):
        return self._result

    def stop(self):
        # collect and release allocated resources
        del self._config, self._result
        self.terminate()
