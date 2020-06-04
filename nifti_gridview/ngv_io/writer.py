import numpy as np
import os
import cv2

class writer(object):
    def __init__(self, configs_list, draw_worker):
        self.data = data
        self.outdir = outdir

    def write(self):
        assert isinstance(self.data, dict), "Input data must be in format of dictionary: {'outname': data}"

        # check output dir avaialble
        if not os.path.isdir(self.outdir):
            os.makedirs(self.outdir, 0o755, exist_ok=True)

        for i, outname in enumerate(self.data):
            data_arr = self.data[outname]
            if not isinstance(data_arr, np.ndarray):
                data_arr = np.array(data_arr)

            if data_arr.dtype == np.dtype('double') or data_arr.dtype == np.dtype('float'):
                data_arr = writer._float_im_to_RGB(data_arr)

            outdir = os.path.join(self.outdir, outname.replace('.nii', '').replace('.gz','') + '.png')
            cv2.imwrite(outdir, data_arr)

        pass

    @staticmethod
    def _float_im_to_RGB(image):
        if not isinstance(image, np.ndarray):
            image = np.array(image)

        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        return image



