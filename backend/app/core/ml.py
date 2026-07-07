import skops.io as sio

from core.transformers import ColumnSelector  # noqa: F401
from core.paths import MODEL_V2_PATH


def load_model():
    untrusted = sio.get_untrusted_types(file=MODEL_V2_PATH)

    return sio.load(MODEL_V2_PATH, trusted=untrusted)
