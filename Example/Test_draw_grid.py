from nifti_gridview import *
from ngv_io import *
from ngv_model import draw_grid_wrapper

def main():
    rootdir = '/home/***REMOVED***/Source/Repos/***REMOVED***_Segmentation/***REMOVED***_Segmentation/44.Benign_Malignant_Cropped_Largest'
    r = ngv_io_reader_wrapper(None)
    r.configure_reader(rootdir)

    c = {
        'nrow': 5,
        'offset': 1
    }
    d = draw_grid_wrapper()
    d.set_config(c)

    w = ngv_io_writer_wrapper(None)
    w.configure_writer(r, d, '/home/***REMOVED***/FTP/temp/NIfTI-gridview')
    w.run()


if __name__ == '__main__':
    main()