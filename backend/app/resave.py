import skops.io as sio

from core.paths import MODEL_V1_PATH, MODEL_V2_PATH
from core.transformers import ColumnSelector  # noqa: F401

untrusted = sio.get_untrusted_types(file=MODEL_V1_PATH)
# print("Antes", untrusted)

model = sio.load(MODEL_V1_PATH, trusted = untrusted)
sio.dump(model, MODEL_V2_PATH)

print("Después", sio.get_untrusted_types(file=MODEL_V2_PATH))
