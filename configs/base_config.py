import json
from os.path import join


class BaseConfig:
    nb_folds = 5

    # SageMakerTrainingRoot_dir = "/opt/ml/code/"  # Here /code/==/IntelCervicalCancer/ '/opt/ml/input/data'

    # SageMakerTrainingRoot_dir = '/opt/ml/input/data'  # Here /code/==/IntelCervicalCancer/
    SageMakerTrainingRoot_dir = ""

    if SageMakerTrainingRoot_dir:
        SageMakerRoot_dir = SageMakerTrainingRoot_dir
    else:
        SageMakerRoot_dir = "/home/ec2-user/SageMaker/Haemorrhage_dataset"

    data_root = join(SageMakerRoot_dir, 'Haemorrhage_dataset/')
    train_dir = join(SageMakerRoot_dir, 'stage_2_train')
    test_dir = join(SageMakerRoot_dir, 'stage_2_test')
    # test2_dir = join(SageMakerRoot_dir, 'stage_2_test_images')
    labels_path = join(SageMakerRoot_dir, 'stage_2_train.csv')

    # Used for Dmytro's models
    checkpoints_dir = join(SageMakerRoot_dir, 'output/checkpoints')
    tensorboard_dir = join(SageMakerRoot_dir, 'output/tensorboard')
    oof_dir = join(SageMakerRoot_dir, 'output/oof')
    prediction_dir = join(SageMakerRoot_dir, 'output/prediction')

    # Used for Brainscan models
    model_outdir = join(SageMakerRoot_dir, 'model_out/')
    # model_outdir = join(SageMakerRoot_dir, 'output/prediction')

    n_classes = 6
    csv_root_dir = None


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
