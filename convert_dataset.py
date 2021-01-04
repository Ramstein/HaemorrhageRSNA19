""" Convert the data set from .dcm format to the following directories:
    * "vis/" - Label visualization in .png format.
    * "npy/" - Original pixel array transformed using RescaleSlope and RescaleIntercept
                parameters, without windowing, stored in .npy format. The most efficient
                way to load data during training.
"""

import glob
import os
import traceback
from multiprocessing import Pool

import cv2
import numpy as np
import pydicom
from tqdm import tqdm

from configs.base_config import BaseConfig
from data.utils import load_labels
from preprocessing.pydicom_loader import PydicomLoader

loader = PydicomLoader()
labels = load_labels()


def convert_sample(path):
    try:
        img = loader.load(path)
        img = ((img.astype(np.float32) / np.iinfo(np.uint16).max) * 255).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        img_orig_hu = loader.load(path, convert_hu=False)

        draw_labels(path, img)
        save_image(path, img, img_orig_hu)

    except:
        traceback.print_exc()


def draw_labels(path, img):
    counter = 0
    scan_id = pydicom.dcmread(path).SOPInstanceUID

    # Draw labels in train subset only
    if 'train' in path:
        for c in BaseConfig.CLASSES.keys():
            if labels.loc[scan_id][c]:
                cv2.circle(img, (BaseConfig.STEP, BaseConfig.STEP // 2 + counter * BaseConfig.STEP),
                           BaseConfig.STEP // 2, BaseConfig.CLASSES[c], -1)
                cv2.putText(img, c, (2 * BaseConfig.STEP, BaseConfig.STEP // 2 + counter * BaseConfig.STEP),
                            cv2.FONT_HERSHEY_SIMPLEX, .5, BaseConfig.CLASSES[c])
                counter += 1

    # if any(labels.loc[scan_id]):
    #     cv2.imshow('img', img)
    #     cv2.waitKey()


def save_image(path, img, img_orig_hu):
    global dst_link
    dst_path = path.replace("dicom", "vis").replace('.dcm', '.jpg')
    dst_path_orig_hu = path.replace("dicom", "npy").replace('.dcm', '.npy')
    is_brainscan_server = "/kolos/m2/ct" in path

    if is_brainscan_server:
        dst_link = dst_path
        dst_path = dst_link.replace('m2', 'storage')
        os.makedirs(os.path.dirname(dst_link), exist_ok=True)

    for path in [dst_path, dst_path_orig_hu]:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    cv2.imwrite(dst_path, img)
    np.save(dst_path_orig_hu, img_orig_hu)

    # Store data visualisation files on a slower disk array
    if is_brainscan_server:
        if os.path.exists(path):
            os.remove(path)

        os.symlink(dst_path, dst_link)


def main():
    paths = list(glob.glob(BaseConfig.PATH))

    with Pool(BaseConfig.WORKERS) as p:
        r = list(tqdm(p.imap(convert_sample, paths), total=len(paths)))

    # one broken sample, copied train/ID_9180c688de/npy/036.npy to 037.npy
    # convert_sample('/mnt/data_fast/rsna/train/ID_9180c688de/dicom/037.dcm')


if __name__ == "__main__":
    main()
