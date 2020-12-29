from glob import glob

import numpy as np
import pandas as pd
from models.smoothing.utils import compute_log_loss_per_class

from configs.second_level import Config

config = Config


def main(config):
    # for path in list(glob(str(config.models_root / "*/*/predictions/*"))):
    #     if '_smoothed' in path:
    #         continue
    #
    #     path = Path(path)
    #     path_smoothed = path.with_name(path.stem + "_smoothed.csv")
    #     smooth_predictions(path, path_smoothed)

    preds = []
    weights = []

    for path in list(glob(str(config.models_root / "*/*/predictions/test_*_smoothed.csv"))):
        log_loss_per_class = np.array(compute_log_loss_per_class(path.replace('test', 'val')))
        weights.append(log_loss_per_class)
        preds.append(pd.read_csv(path)[config.pred_columns].to_numpy())

    preds = np.array(preds)

    # TODO transform weights
    weights = np.array(weights)

    # Multiply predictions by weights from validation log loss
    for i in range(len(preds)):
        preds[i] = np.multiply(weights[i], preds[i])

    # Sum predictions from many folds
    preds = np.sum(preds, axis=0)

    # Sum weights for each class
    weights = np.sum(weights, axis=0)

    # Divide weighted sum of predictions by sum of weights
    preds = np.divide(preds, weights)

    print(preds)


if __name__ == "__main__":
    main(Config())
