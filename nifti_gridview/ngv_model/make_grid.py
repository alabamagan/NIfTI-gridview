from typing import Union, Optional, List, Tuple, Text, BinaryIO
import numpy as np
import math
irange = range

def make_grid(
        tensor: Union[np.ndarray, List[np.ndarray]],
        nrow: int = 8,
        padding: int = 2,
        normalize: bool = False,
        range: Optional[Tuple[int, int]] = None,
        scale_each: bool = False,
        pad_value: int = 0,
) -> np.ndarray:
    """Make a grid of images.
    This is essentially a port numpy version from torchvision.make_grid. See Examples.

    Args:
        tensor (Tensor or list): 4D mini-batch Tensor of shape (B x C x H x W)
            or a list of images all of the same size.
        nrow (int, optional): Number of images displayed in each row of the grid.
            The final grid size is ``(B / nrow, nrow)``. Default: ``8``.
        padding (int, optional): amount of padding. Default: ``2``.
        normalize (bool, optional): If True, shift the image to the range (0, 1),
            by the min and max values specified by :attr:`range`. Default: ``False``.
        range (tuple, optional): tuple (min, max) where min and max are numbers,
            then these numbers are used to normalize the image. By default, min and max
            are computed from the tensor.
        scale_each (bool, optional): If ``True``, scale each image in the batch of
            images separately rather than the (min, max) over all images. Default: ``False``.
        pad_value (float, optional): Value for the padded pixels. Default: ``0``.

    Example:
        See this notebook `here <https://gist.github.com/anonymous/bf16430f7750c023141c562f3e9f2a91>`_

    """
    if not (isinstance(tensor, np.ndarray) or
            (isinstance(tensor, list) and all(isinstance(t, np.ndarray) for t in tensor))):
        raise TypeError('tensor or list of tensors expected, got {}'.format(type(tensor)))

    # if list of tensors, convert to a 4D mini-batch Tensor
    if isinstance(tensor, list):
        tensor = np.stack(tensor, axis=0)

    if tensor.ndim == 2:  # single image H x W
        tensor = np.expand_dims(tensor, axis=0)
    if tensor.ndim == 3:  # single image
        if tensor.shape[0] == 1:  # if single-channel, convert to 3-channel
            tensor = np.concatenate((tensor, tensor, tensor), axis=0)
        tensor = np.expand_dims(tensor, axis=0)

    if tensor.ndim == 4 and tensor.shape[0] == 1:  # single-channel images
        tensor = np.concatenate((tensor, tensor, tensor), axis=1)

    if normalize is True:
        tensor = tensor.copy()  # avoid modifying tensor in-place
        if range is not None:
            assert isinstance(range, tuple), \
                "range has to be a tuple (min, max) if specified. min and max are numbers"

        def norm_ip(img, min, max):
            # Copy by reference
            img[:] = np.clip(img, min, max)
            img[:] = (img - min)/(max - min + 1e-8)


        def norm_range(t, range):
            if range is not None:
                return norm_ip(t, range[0], range[1])
            else:
                return norm_ip(t, float(t.min()), float(t.max()))

        if scale_each is True:
            for t in tensor:  # loop over mini-batch dimension
                norm_range(t, range)
        else:
            norm_range(tensor, range)

    if tensor.shape[0] == 1:
        return tensor.squeeze(0)

    # make the mini-batch of images into a grid
    nmaps = tensor.shape[0]
    xmaps = min(nrow, nmaps)
    ymaps = int(math.ceil(float(nmaps) / xmaps))
    height, width = int(tensor.shape[2] + padding), int(tensor.shape[3] + padding)
    num_channels = tensor.shape[1]
    grid = np.ones([num_channels, height * ymaps + padding, width * xmaps + padding]) * pad_value
    k = 0
    for y in irange(ymaps):
        for x in irange(xmaps):
            if k >= nmaps:
                break
            # Tensor.copy_() is a valid method but seems to be missing from the stubs
            # https://pytorch.org/docs/stable/tensors.html#torch.Tensor.copy_
            s = [slice(None)] * grid.ndim
            s[1] = slice(y * height + padding, (y + 1) * height)
            s[2] = slice(x * width + padding, (x + 1) * width)

            grid[tuple(s)] = tensor[k].copy()
            k = k + 1
    return grid