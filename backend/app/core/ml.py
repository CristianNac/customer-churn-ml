import skops.io as sio

from core.paths import MODEL_V2_PATH
from core.transformers import ColumnSelector  # noqa: F401


def load_model():
    untrusted = sio.get_untrusted_types(file=MODEL_V2_PATH)

    return sio.load(MODEL_V2_PATH, trusted=untrusted)

