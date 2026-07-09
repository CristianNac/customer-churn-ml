import json

from core.paths import METRIC_PATH


def read_metrics()->dict:
    with open(METRIC_PATH) as file:
        return json.load(file)