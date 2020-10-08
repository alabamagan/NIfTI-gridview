from .make_grid import make_grid
import numpy as np
import cv2

colormaps = {
    'Default': None,
    'Parula': cv2.COLORMAP_PARULA,
    'Autumn': cv2.COLORMAP_AUTUMN,
    'Bone': cv2.COLORMAP_BONE,
    'Jet': cv2.COLORMAP_JET,
    'Rainbow': cv2.COLORMAP_RAINBOW,
    'Ocean': cv2.COLORMAP_OCEAN,
    'Summer': cv2.COLORMAP_SUMMER,
    'Spring': cv2.COLORMAP_SPRING,
    'Cool': cv2.COLORMAP_COOL ,
    'HSV': cv2.COLORMAP_HSV,
    'Pink': cv2.COLORMAP_PINK,
    'Hot': cv2.COLORMAP_HOT
}

def draw_grid(image, crop=None, nrow=None, offset=None, background=0, margins=1, cmap=None, **kwargs):
    """
    This is the wrapper function for make_grid that supports some extra tweaking.

    Args:
        image (np.ndarray):
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
        cmap (str, Optional):
            Colormap for image drawing, see dicitonary `cmap` for a list of available colormap. Default
            to `None`.
        **kwargs:
            Not suppose to have any use.

    Returns:
        torch.Tensor
    """
    if not offset is None:
        if not offset >= 0:
            raise ArithmeticError("Offset cannot be negative")


    # Offset the image by padding zeros
    if not offset is None:
        image = image.squeeze()
        image = np.pad(image, [(0, 0), (0, 0), (offset, 0)], constant_values=0)

    # Handle dimensions
    if image.ndim == 3:
        image = np.expand_dims(image, axis=1)

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
    im_grid = (im_grid * 255.).transpose(1, 2, 0).astype('uint8').copy()

    if not (cmap is None or cmap == 'Default'):
        im_grid = cv2.applyColorMap(im_grid[:,:,0], colormaps[cmap])

    if im_grid.shape[2] == 1:
        im_grid = np.concatenate([im_grid] * 3, axis=2)
    # elif im_grid.shape[2] == 1:
    #     im_grid = cv2.applyColorMap(im_grid[:,:,0], cv2.COLORMAP_BONE)
    # elif im_grid.squeeze().ndim == 2:
    #     im_grid = cv2.applyColorMap(im_grid, cv2.COLORMAP_BONE)
    # im_grid = (im_grid).permute(1, 2, 0).numpy().astype('float').copy()
    return im_grid

def draw_grid_contour(im_grid, seg, crop=None, nrow=None, offset=None, background=0, margins=1, color=None,
                      thickness=2, alpha=0.5, **kwargs):
    """
    This is the wrapper function for make_grid that supports some extra tweaking.

    Args:
        im_grid (np.ndarray):
            Input 3D image, should have a dimension of 3 with configuration Z x W x H.
        seg (np.ndarray):
            Input 3D segmentation, should have a dimension of 3 with configuration Z x W x H.
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
        color (iter, Optional):
            Color of the output contour.
        alpha (float, Optional):
            Alpha channel. Default to 0.5.
        **kwargs:
            Not suppose to have any use.

    Returns:
        torch.Tensor
    """
    assert offset >= 0 or offset is None, "In correct offset setting!"


    if isinstance(seg, np.ndarray):
        seg = seg.astype('uint8')

    # Offset the image by padding zeros
    if not offset is None and offset != 0:
        seg = seg.squeeze()
        seg = np.pad(seg, [(0, 0), (0, 0), (offset, 0)], constant_values=0)

    # Handle dimensions
    if seg.ndim == 3:
        seg = np.expand_dims(seg, axis=1)

    # compute number of image per row if now provided
    if nrow is None:
        nrow = np.int(np.ceil(np.sqrt(len(seg))))


    # Crop the image along the x, y direction, ignore z direction.
    if not crop is None:
        # Find center of mass for segmentation
        seg_shape = seg.shape

        center = crop['center']
        size = crop['size']
        lower_bound = [np.max([0, int(c - s // 2)]) for c, s in zip(center, size)]
        upper_bound = [np.min([l + s, m]) for l, s, m in zip(lower_bound, size, seg_shape[1:])]

        # Crop
        seg = seg[:,:, lower_bound[0]:upper_bound[0], lower_bound[1]:upper_bound[1]]

    if nrow is None:
        nrow = int(np.round(np.sqrt(seg.shape[0])))

    # return image as RGB with range 0 to 255
    seg_grid = make_grid(seg, nrow=nrow, padding=margins, normalize=False, pad_value=background)
    seg_grid = seg_grid[0].astype('uint8').copy()

    # Find Contours
    try:
        _a, contours, _b = cv2.findContours(seg_grid, mode=cv2.RETR_EXTERNAL,
                                            method=cv2.CHAIN_APPROX_SIMPLE)
    except:
        contours, _b = cv2.findContours(seg_grid, mode=cv2.RETR_EXTERNAL,
                                        method=cv2.CHAIN_APPROX_SIMPLE)

    # Draw contour on image grid
    try:
        _temp = np.zeros_like(im_grid)
        cv2.drawContours(_temp, contours, -1, list(color.color().getRgb()[:3]) + [1],
                         thickness=thickness, lineType=cv2.LINE_AA)
        im_grid = cv2.addWeighted(im_grid, 1, _temp, alpha, 0)
        del _temp

    except Exception as e:
        print(e)
        # ngv_logger.global_log("Error during draw contours.")
        # ngv_logger.global_log(e)
    return im_grid