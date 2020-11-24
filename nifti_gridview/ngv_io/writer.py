import numpy as np
import os
import cv2
import gc
from ngv_model import draw_grid_wrapper, NGV_Logger

class writer(object):
    def __init__(self, data_loader, seg_loaders, draw_worker, outdir, **kwargs):
        assert isinstance(draw_worker, draw_grid_wrapper), "Incorrect type."

        self._data_loader = data_loader
        self._seg_loaders = seg_loaders
        self._outdir = outdir
        self._draw_worker = draw_worker
        self._high_res = kwargs['high_res'] if 'high_res' in kwargs else False
        self._keys_to_write = kwargs['keys_to_write'] if 'keys_to_write' in kwargs else None


    def write(self):
        # check output dir avaialble
        if not os.path.isdir(self._outdir):
            os.makedirs(self._outdir, 0o755, exist_ok=True)

        extension = '.png' if self._high_res else '.jpg'

        for key, img in self._data_loader:
            # Skip files if its not in keys-to-write if it exists
            if not self._keys_to_write is None:
                if not key in self._keys_to_write:
                    continue

            tmp_config = {
                'target_im': img,
                'segment': []
            }
            for s_loader in self._seg_loaders:
                tmp_config['segment'].append(s_loader[key])

            self._draw_worker.update_config(tmp_config)
            self._draw_worker.run()

            tmp_img = self._draw_worker.get_result()
            # if tmp_img.dtype == np.dtype('double') or tmp_img.dtype == np.dtype('float'):
            #     tmp_img = writer._float_im_to_RGB(tmp_img)

            out_fnmae = os.path.join(self._outdir, key.replace('.nii', '').replace('.gz','') + extension)
            cv2.imwrite(out_fnmae, cv2.cvtColor(tmp_img, cv2.COLOR_RGB2BGR))
            del tmp_config['segment'], tmp_config['target_im'], tmp_config, tmp_img, img
            gc.collect()
        pass

    @staticmethod
    def _float_im_to_RGB(image):
        if not isinstance(image, np.ndarray):
            image = np.array(image)

        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        return image



