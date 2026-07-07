from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]

METRIC_PATH = APP_DIR/"metric_results"/"metrics_best_model.json"
MODEL_V1_PATH = APP_DIR/"models"/"model_lr_near_miss.skops"
MODEL_V2_PATH = APP_DIR/"models"/"model_lr_near_miss_V2.skops"