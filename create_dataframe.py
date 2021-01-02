"""
Script parsing dicom metadata and creating dataframe used later to create directory structure.
"""
import os
import pickle
from collections import defaultdict
from multiprocessing import Process

import pandas
import pydicom
from tqdm import tqdm

from configs.base_config import BaseConfig

# path under which new directory structure will be created
tags = ['SOPInstanceUID',
        'Modality',
        'PatientID',
        'StudyInstanceUID',
        'SeriesInstanceUID',
        'StudyID',
        'ImagePositionPatient',
        'ImageOrientationPatient',
        'SamplesPerPixel',
        'PhotometricInterpretation',
        'Rows',
        'Columns',
        'PixelSpacing',
        'BitsAllocated',
        'BitsStored',
        'HighBit',
        'PixelRepresentation',
        'WindowCenter',
        'WindowWidth',
        'RescaleIntercept',
        'RescaleSlope']
d = defaultdict(list)


def read_dicom(path):
    return pydicom.dcmread(path, stop_before_pixels=True)


def main():
    jobs = [('train', BaseConfig.train_dir)]
    # jobs = [('test', BaseConfig.test_dir)]
    for subset, subset_dir in jobs:
        for root, dirs, files in os.walk(subset_dir):
            processes = []

            print(f"Creating Multiprocessing processes for {subset} having data in {subset_dir}")
            for file in tqdm(files):
                p = Process(target=ExtractDicomMetadata, args=(subset, root, file,))
                processes.append(p)
                p.start()
            print(f"Executing processes for {subset} having data in {subset_dir}")
            for process in tqdm(processes):
                process.join()

    df = pandas.DataFrame(d)

    # Save the data frame
    DF_PATH_OUT = os.path.join(BaseConfig.data_root, 'df_train.pkl')
    # DF_PATH_OUT = os.path.join(BaseConfig.data_root, 'df.pkl') # final on merging df_test and df_train.pkl
    os.makedirs(os.path.dirname(DF_PATH_OUT), exist_ok=True)
    with open(DF_PATH_OUT, 'wb') as f:
        pickle.dump(df, f)


def ExtractDicomMetadata(subset, root, file):
    try:
        dcm = read_dicom(os.path.join(root, file))
        for tag in tags:
            try:
                d[tag].append(dcm[tag].value)
            except KeyError:
                d[tag].append(None)
        d['path'].append(os.path.join(root, file))
        d['subset'].append(subset)
    except Exception as e:
        print(e)
        print(os.path.join(root, file))


if __name__ == '__main__':
    main()
