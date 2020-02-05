"""
This utility file helps downloading the data for the L2RPN 2019.

Data are stored as a github "release" accessible at the url:

`https://github.com/BDonnot/Grid2Op/releases/download/data_l2rpn_2019/data_l2rpn_2019.tar.bz2`

Once downloaded, the dataset is uncompressed. It is composed of the exact same files provided for the first edition of
the 2019 L2RPN challenge. There are 1004 chronics of 4 weeks corresponding to january for the fictive grid used
for this competition.

This script works on MacOs, Linux and windows.
"""
import os
import argparse
import io
import sys
from tqdm import tqdm
import re

import tarfile

import pdb
try:
    import urllib.request
except Exception as e:
    raise RuntimeError("Impossible to find library urllib. Please install it.")

URL = "https://github.com/BDonnot/Grid2Op/releases/download/data_l2rpn_2019/data_l2rpn_2019.tar.bz2"
DEFAULT_PATH_DATA = "data"


class DownloadProgressBar(tqdm):
    """
    This class is here to show the progress bar when downloading this dataset
    """
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    """
    This function download the file located at 'url' and save it to 'output_path'
    Parameters
    ----------
    url: ``str``
        The url of the file to download

    output_path: ``str``
        The path where the data will be stored.
    """
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch the evaluation of the Grid2Op ("Grid To Operate") code.')
    parser.add_argument('--path_save', default=DEFAULT_PATH_DATA, type=str,
                        help='The path where the data will be downloaded.')
    args = parser.parse_args()
    path_data = args.path_save

    if not os.path.exists(path_data):
        print("Creating path \"{}\" where l2rpn2019 data will be downloaded".format(path_data))
        os.mkdir(path_data)
    output_path = os.path.abspath(os.path.join(path_data, "data_l2rpn_2019.tar.bz2"))

    # download the data (with progress bar)
    print("downloading the training data, this may take a while.")
    download_url(URL, output_path)

    tar = tarfile.open(output_path, "r:bz2")
    print("Extract the tar archive in {}".format(path_data))
    tar.extractall(path_data)
    tar.close()
    file_location = os.path.split(os.path.abspath(__file__))[0]
    output_path_str = re.sub("\\\\", "\\\\\\\\", output_path)
    with open(os.path.join(file_location, "data_location.py"), "w") as f:
        f.write("# This file has been automatically generated by 'download_training_data.py' do not modify it, "
                "nor remove it.\n# If you want to download the training data again, run "
                "'python l2rpn2019_utils/download_training_data.py'\n\n\n"
                "L2RPN_TRAINING_SET = '{}'\n".format(output_path_str))