import json


class BaseConfig:
    nb_folds = 5

    train_dir = '/home/ec2-user/SageMaker/rsna_dataset/rsna19/stage_2_train'
    test_dir = '/home/ec2-user/SageMaker/rsna_dataset/rsna19/stage_2_test'
    # test2_dir = '/home/ec2-user/SageMaker/rsna_dataset/rsna19/stage_2_test_images'
    labels_path = "/home/ec2-user/SageMaker/rsna_dataset/rsna19/stage_2_train.csv"

    data_root = "/home/ec2-user/SageMaker/rsna_dataset/rsna19/"

    # Used for Dmytro's models
    checkpoints_dir = "/home/ec2-user/SageMaker/output/checkpoints"
    tensorboard_dir = "/home/ec2-user/SageMaker/output/tensorboard"
    oof_dir = "/home/ec2-user/SageMaker/output/oof"
    prediction_dir = "/home/ec2-user/SageMaker/output/prediction"

    # Used for Brainscan models
    model_outdir = '/home/ec2-user/SageMaker/model_out/'
    # model_outdir = "/home/ec2-user/SageMaker/output/prediction"

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
