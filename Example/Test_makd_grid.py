from ngv_model.make_grid import *
from ngv_model.draw_grid import draw_grid
import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk

if __name__ == '__main__':
    im = sitk.GetArrayFromImage(sitk.ReadImage(
        "Z:/Shared/2.Projects/8.NPC_Segmentation/0A.NIFTI_ALL/Nyul_Normed/T2WFS_TRA/769_T2_FS_TRA.nii.gz"))
    test = draw_grid(im, nrow=5)
    # test = make_grid(np.expand_dims(im, axis=1), normalize=True, nrow=5)
    print(test.shape)
    print(test.min(), test.max())

    fig, ax = plt.subplots(1, 1, figsize=(15,15))

    ax.imshow(test.squeeze())
    plt.show()
