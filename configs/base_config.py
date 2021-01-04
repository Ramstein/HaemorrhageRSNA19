import json
import multiprocessing
import os
from collections import namedtuple
from os.path import join


class BaseConfig:
    nb_folds = 5
    n_classes = 6
    csv_root_dir = None

    WORKERS = multiprocessing.cpu_count()
    STEP = 25
    CLASSES = {
        "epidural": (255, 237, 0),
        "intraparenchymal": (212, 36, 0),
        "intraventricular": (173, 102, 108),
        "subarachnoid": (0, 48, 114),
        "subdural": (74, 87, 50)
    }
    # for prepare_3d_data.py
    ShearParams = namedtuple('ShearParams', 'rad_tilt, minus_center_z')
    OUT_SIZE = (400, 400)  # only getting used for creation for prepare_3d_data.py
    BG_HU = -2000

    try:
        SageMakerTrainingRoot_dir = os.path.dirname(os.environ['SM_MODEL_DIR'])  # '/opt/ml'
    except:
        SageMakerTrainingRoot_dir = "input/data/train"

    if SageMakerTrainingRoot_dir:
        SageMakerRoot_dir = SageMakerTrainingRoot_dir
        data_root = join(SageMakerRoot_dir, 'input', 'data')
        train_dir = join(SageMakerRoot_dir, 'input', 'data', 'stage_2_train')
        test_dir = join(SageMakerRoot_dir, 'input', 'data', 'stage_2_test')
        labels_path = join(SageMakerRoot_dir, 'input', 'data', 'stage_2_train.csv')

        # Used for Dmytro's models
        checkpoints_dir = join(os.environ['SM_MODEL_DIR'], 'checkpoints')
        tensorboard_dir = join(os.environ['SM_MODEL_DIR'], 'tensorboard')
        oof_dir = join(os.environ['SM_MODEL_DIR'], 'oof')
        prediction_dir = join(os.environ['SM_MODEL_DIR'], 'prediction')

        # Used for Brainscan models
        model_outdir = join(os.environ['SM_MODEL_DIR'], 'model_out')

    else:
        SageMakerRoot_dir = "/home/ec2-user/SageMaker/Haemorrhage_dataset"
        data_root = SageMakerRoot_dir
        train_dir = join(SageMakerRoot_dir, 'stage_2_train')
        test_dir = join(SageMakerRoot_dir, 'stage_2_test')
        labels_path = join(SageMakerRoot_dir, 'stage_2_train.csv')

        # Used for Dmytro's models
        checkpoints_dir = join(SageMakerRoot_dir, 'checkpoints')
        tensorboard_dir = join(SageMakerRoot_dir, 'tensorboard')
        oof_dir = join(SageMakerRoot_dir, 'oof')
        prediction_dir = join(SageMakerRoot_dir, 'prediction')

        # Used for Brainscan models
        model_outdir = join(SageMakerRoot_dir, 'model_out')

    PATH = os.path.join(data_root, "*/*/dicom/*")

    # DF_PATHS_IN = [
    #     os.path.join(data_root, 'df.pkl'),
    #     os.path.join(data_root, 'df-stage2-test.pkl')]
    #
    # # dataframe mapping SOPInstanceUID of each dicom to path in new directory structure
    # ID_DF_PATHS_OUT = [
    #     os.path.join(data_root, 'id_to_path.pkl'),
    #     os.path.join(data_root, 'id_to_path_stage2-test.pkl')]

    DF_PATHS_IN = [os.path.join(data_root, 'df.pkl')]

    # dataframe mapping SOPInstanceUID of each dicom to path in new directory structure
    ID_DF_PATHS_OUT = [os.path.join(data_root, 'id_symlinks.pkl')]


def get_train_folds(val_folds):
    return list({0, 1, 2, 3, 4} - set(val_folds))


def get_val_folds_str(val_folds):
    return "".join([str(i) for i in val_folds])


def load(config_path):
    dct = json.load(open(config_path))
    if 'dataset_file' in dct:
        dct['train_dataset_file'] = dct['dataset_file']
        dct['val_dataset_file'] = dct['dataset_file']
        dct['test_dataset_file'] = 'test.csv'
    config = type('', (), dct)()
    return config
