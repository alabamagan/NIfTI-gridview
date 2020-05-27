from torchvision.utils import make_grid
from torch import tensor, nn
import numpy as np

def draw_grid(image, crop=None, nrow=None, offset=None, background=0, margins=1, **kwargs):
    """
    This is the wrapper function for make_grid that supports some extra tweaking.

    Args:
        image (np.ndarray or torch.Tensor):
            Input 3D image, should have a dimension of 3 with configuration Z x W x H.
        crop (dict, Optional):
            If provided with key `{'center': [w, h] 'size': [sw, sh] or int }`, the image is cropped
            first before making the grid. Default to None.
        nrow (int, Optional):
            Passed to function `make_grid`. Automatically calculated if its None to be the square
            root of total number of input slices in `image`. Default to None.
        offset (int, Optional):
            Offset the input along Z-direction by inserting empty slices. Default to None.
        background (float, Optional)
            Background pixel value for offset and margins option. Default to 0.
        margins (int, Optional):
            Pass to `make_grid` padding option. Default to 1.
        **kwargs:
            Not suppose to have any use.

    Returns:
        torch.Tensor
    """
    assert offset >= 0 or offset is None, "In correct offset setting!"


    if isinstance(image, np.ndarray):
        image = tensor(image)

    # Offset the image by padding zeros
    if not offset is None:
        image = image.squeeze()
        image = nn.ConstantPad3d((0, 0, 0, 0, offset, 0), 0)(image)

    # Handle dimensions
    if image.dim() == 3:
        image = image.unsqueeze(1)

    # compute number of image per row if now provided
    if nrow is None:
        nrow = np.int(np.ceil(np.sqrt(len(image))))


    # Crop the image along the x, y direction, ignore z direction.
    if not crop is None:
        # Find center of mass for segmentation
        im_shape = image.shape

        center = crop['center']
        size = crop['size']
        lower_bound = [np.max([0, int(c - s // 2)]) for c, s in zip(center, size)]
        upper_bound = [np.min([l + s, m]) for l, s, m in zip(lower_bound, size, im_shape[1:])]

        # Crop
        image = image[:,:, lower_bound[0]:upper_bound[0], lower_bound[1]:upper_bound[1]]

    if nrow is None:
        nrow = int(np.round(np.sqrt(image.shape[0])))

    # return image as RGB with range 0 to 255
    im_grid = make_grid(image, nrow=nrow, padding=margins, normalize=True, pad_value=background)
    im_grid = (im_grid * 255.).permute(1, 2, 0).numpy().astype('uint8').copy()
    # im_grid = (im_grid).permute(1, 2, 0).numpy().astype('float').copy()
    return im_grid