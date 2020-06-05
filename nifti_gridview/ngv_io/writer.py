import numpy as np
import os
import cv2

from visualization import draw_grid_wrapper

class writer(object):
    def __init__(self, data_loader, draw_worker, outdir, **kwargs):
        assert isinstance(draw_worker, draw_grid_wrapper), "Incorrect type.and"

        self._data_loader = data_loader
        self._outdir = outdir
        self._draw_worker = draw_worker


    def write(self):
        # check output dir avaialble
        if not os.path.isdir(self._outdir):
            os.makedirs(self._outdir, 0o755, exist_ok=True)

        for key, img in self._data_loader:
            tmp_config = {
                'target_im': img,
            }
            self._draw_worker.update_config(tmp_config)
            self._draw_worker.run()

            tmp_img = self._draw_worker.get_result()
            if tmp_img.dtype == np.dtype('double') or tmp_img.dtype == np.dtype('float'):
                tmp_img = writer._float_im_to_RGB(tmp_img)

            out_fnmae = os.path.join(self._outdir, key.replace('.nii', '').replace('.gz','') + '.png')
            cv2.imwrite(out_fnmae, tmp_img)
        pass

    @staticmethod
    def _float_im_to_RGB(image):
        if not isinstance(image, np.ndarray):
            image = np.array(image)

        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        return image



