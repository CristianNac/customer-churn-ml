from pathlib import Path

import skops.io as sio

from core.transformers import ColumnSelector


SRC = Path(__file__).resolve().parents[2]/"models"/"model_lr_near_miss.skops"
DST = Path(__file__).resolve().parents[2]/"models"/"model_lr_near_miss_V2.skops"

untrusted = sio.get_untrusted_types(file=SRC)
# print("Antes", untrusted)

model = sio.load(SRC, trusted = untrusted)
sio.dump(model, DST)

print("Después", sio.get_untrusted_types(file=DST))
