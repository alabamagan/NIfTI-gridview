from nifti_gridview.ngv_model import draw_grid_wrapper
import os
import re
import SimpleITK as sitk
import numpy as np
import cv2

target_keys = ['fs-T2W', 'ce-T1W', 'ce-fs-T1W']
drawing_params = {
    'data_paths':{
        'img_path': {
            'fs-T2W': 'Z:\\Shared\\2.Projects\\8.NPC_Segmentation\\0A.NIFTI_ALL\\Malignant\\T2WFS_TRA',
            'ce-T1W': 'Z:\\Shared\\2.Projects\\8.NPC_Segmentation\\0A.NIFTI_ALL\\Malignant\\CE-T1W_TRA',
            'ce-fs-T1W': 'Z:\\Shared\\2.Projects\\8.NPC_Segmentation\\0A.NIFTI_ALL\\Malignant\\CE-T1WFS_TRA'
        },
        'gt_path': {
            'fs-T2W': 'Z:\\Shared\\2.Projects\\8.NPC_Segmentation\\0B.Segmentations\\T2WFS_TRA\\00.First',
            'ce-T1W': 'Z:\\Shared\\2.Projects\\8.NPC_Segmentation\\0B.Segmentations\\CE-T1W_TRA\\00.First',
            'ce-fs-T1W': 'Z:\\Shared\\2.Projects\\8.NPC_Segmentation\\0B.Segmentations\\CE-T1WFS_TRA\\00.First',
        },
        'cnn_path': {
            'fs-T2W': 'Z:\\Shared\\2.Projects\\8.NPC_Segmentation\\98.Output\\T1vT2.temp\\T2W-FS',
            'ce-T1W': 'Z:\\Shared\\2.Projects\\8.NPC_Segmentation\\98.Output\\T1vT2.temp\\CE-T1W',
            'ce-fs-T1W': 'Z:\\Shared\\temp\\ce-fs-T1w.20201208\\Results'
        }
    },
    'draw_id': {    # Count slice with segment only.
        '968': [6],
    },
    'contour_color': [
        (0, 255, 255),
        (255, 128, 0)
    ],
    'output_dir': 'Z:\\Shared\\temp\\ce-fs-T1w.20201208\\ContourImagesForRevision'
}


def list_all_files(rootdir):
    """
    List all files with the subdir
    """
    out = []
    for r, d, f in os.walk(rootdir):
        if not len(f) == 0:
            l = [os.path.join(r, ff).replace(rootdir, '') for ff in f]
            out.extend(l)
    return out

class color(object):
    """
    For qt compatibility
    """
    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def color(self):
        return self

    def getRgb(self):
        return [self.r, self.g, self.b, self.a]

drawer = draw_grid_wrapper()

# Load images
for idx in drawing_params['draw_id']:
    # Find image in each folder
    _ims = {}
    _draw_slices = {}
    paths = drawing_params['data_paths']
    for p in paths:
        _ims[p] = {}
        for mod in target_keys:
            # Find image/segment files that has the correct study number
            f_name = list(filter(lambda x: re.match(f".*{idx}.*", x), list_all_files(paths[p][mod])))[0]
            f_path = paths[p][mod] + '\\' + f_name # join didn't work well here
            _ims[p][mod] = sitk.GetArrayFromImage(sitk.ReadImage(f_path))

    # get ground-truth slices
    gt = _ims['gt_path']['ce-fs-T1W']
    slices_w_seg = (gt.sum(axis=-1).sum(axis=-1) != 0)

    for p in paths:
        _draw_slices[p] = {}
        for mod in target_keys:
            _draw_slices[p][mod] = [_ims[p][mod][slices_w_seg][i-1] for i in drawing_params['draw_id'][idx]]

    for a, i in enumerate(drawing_params['draw_id'][idx]):
        print([_draw_slices['img_path'][mod][a] for mod in target_keys])
        target_im = np.stack([_draw_slices['img_path'][mod][a] for mod in target_keys])
        gt_im = np.stack([_draw_slices['gt_path'][mod][a] for mod in target_keys])
        cnn_im = np.stack([_draw_slices['cnn_path'][mod][a] for mod in target_keys])
        config = {
            'target_im': target_im,
            'segment': [gt_im, cnn_im],
            'segment_color': [color(*c) for c in drawing_params['contour_color']],
            'nrow': 3,
            'offset': 0,
            'margins': 3,
            'cmap': 'Default',
            'thickness': 1,
            'alpha': 1,
            'seg_only': False,
            'background': 1
        }
        drawer._config = config
        drawer.run()
        res = drawer.get_result()

        out_fname = os.path.join(drawing_params['output_dir'], f'{idx}_{i}.png')
        cv2.imwrite(out_fname, cv2.cvtColor(res, cv2.COLOR_RGB2BGR))
    del _ims, _draw_slices
