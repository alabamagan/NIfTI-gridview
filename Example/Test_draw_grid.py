from nifti_gridview import *

def main():
    rootdir = '/home/***REMOVED***/Source/Repos/***REMOVED***_Segmentation/***REMOVED***_Segmentation/44.Benign_Malignant_Cropped_Largest'
    r = reader(rootdir)

    out_ims = {}
    for name in r._images:
        out_ims[name] = draw_grid(r._images[name], nrow=5)

    w = writer(out_ims, '/home/***REMOVED***/FTP/temp/T1vT2_image_grid')
    w.write()


if __name__ == '__main__':
    main()