import SimpleITK as sitk
import os
import re
from ngv_model import ngv_logger

class reader(object):
    """
    This is the main reader class for this package. Uses `SimpleITK` to read the images.

    Args:
        rootdir (str):
            Directory to read the images from designated paths.
        recurisve (bool, Optional):
            Flag to read nifti files recursively. Default to False.
        fname_filter (dict, Optional):
            Dictionary in format of {'[regex_globber]': [list of ids], 'regex_matcher': None}. For
            regex globbers, the regex will glob ids from filenames and include only ids that are present
            in the `[list of ids]` as strings. If the value is `None`, the regex will be treated as a
            matcher and filter away all the files with names that don't match.
        dtype (str or type, Optional):
            Type of data to cast the data into.
        id_globber (str, Optional):
            Regex string for globbing IDs from files to align datasets. Default to "([0-9]{3,5})"

    """
    def __init__(self, rootdir, recursive=False, fname_filters=None, dtype='float',
                 id_globber="(^[a-zA-Z0-9]+)", **kwargs):
        # super(reader, self).__init__()

        self.rootdir = rootdir
        self.recursive = recursive
        self.fname_filter = fname_filters
        self.dtype = dtype
        self.id_globber = id_globber

        self._ids = {}
        self._files = {}
        self._images = {}
        self._iter = None

        self._parse_rootdir()

    def _parse_rootdir(self):
        """
        Loader uses file name as keeys
        """
        assert os.path.isdir(self.rootdir), "Cannot open root dir from {}!".format(self.rootdir)

        # Read files
        if self.recursive:
            for root, dirs, files in os.walk(self.rootdir):
                if len(files) > 0:
                    for f in files:
                        if f.endswith('.nii') or f.endswith('.nii.gz'):
                            self._files[f] = os.path.join(root, f)
                else:
                    pass
        else:
            for f in os.listdir(self.rootdir):
                if f.endswith('.nii') or f.endswith('.nii.gz'):
                    self._files[f] = os.path.join(self.rootdir, f)

        # Confirm files are loaded
        assert len(self._files) != 0, "No files are founded!"

        # Filter files, filter should be in format {'regex_globber': [list of ids], 'regex_wildcards': None}
        if not self.fname_filter is None:
            assert isinstance(self.fname_filter, dict), "Incorrect fnmame_filter format: {}".format(type(
                self.fname_filter))
            for regex in self.fname_filter:
                keys_to_pop = []
                if self.fname_filter[regex] is None:
                    for f in self._files:
                        if re.match(regex, f) is None:
                            keys_to_pop.append(f)
                elif isinstance(self.fname_filter[regex], list):
                    for f in self._files:
                        mo = re.search(regex, f)
                        if not mo is None:
                            if not mo.group(0) in self.fname_filter[regex]:
                                keys_to_pop.append(f)

                # remove filtered files
                for keys in keys_to_pop:
                    self._files.pop(keys)

        # Globe ids
        for fname in self._files:
            mo = re.search(self.id_globber, fname)
            if not mo is None:
                self._ids[fname[mo.start():mo.end()]] = fname


    def _read_files(self):
        for i, f in enumerate(self._files):
            self._images[f] = sitk.GetArrayFromImage(sitk.ReadImage(self._files[f])).astype(self.dtype)

    def _read_file(self, i):
        key = list(self._files.keys())[i]
        self._images[key] = sitk.GetArrayFromImage(sitk.ReadImage(self._files[key])).astype(self.dtype)

    def get_item_by_id(self, item):
        if not item in self._ids:
            return None
        else:
            return self[self._ids[item]]

    def __getitem__(self, item):
        if not item in self._images:
            try:
                self._images[item] = sitk.GetArrayFromImage(sitk.ReadImage(self._files[item]))
            except:
                try:
                    id = re.search(self.id_globber, item).group()
                    return self[self._ids[id]]
                except Exception as e:
                    if id is not None:
                        ngv_logger.global_log("Cannot read item with ID: {}".format(id), 30)
                    ngv_logger.global_log("Reader encounter exception: {}".format(e))
                    pass
                ngv_logger.global_log("Cannot read item with key: {}.".format(item), 30)
                return 0
        return self._images[item]

    def __len__(self):
        return len(self._files)

    def __iter__(self):
        for key in self._files.keys():
            yield key, self[key]
