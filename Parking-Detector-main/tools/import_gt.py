import glob, pandas as pd, sqlalchemy as sa
from datetime import datetime

ENGINE = sa.create_engine("postgresql://user:pwd@localhost/parking_finder")

rows = []
for txt in glob.glob("labels/*.txt"):          # YOLO export
    # кадр_00042.jpg → таймстамп = 42 сек
    sec = int(txt.split('_')[-1].split('.')[0])
    ts = datetime(2024, 5, 28, 12, 0, sec)     # подставьте реальное начало видео
    for l in open(txt):
        cls, x, y, w, h, slot, occ = map(float, l.split())
        rows.append((int(slot), ts, bool(int(occ))))

pd.DataFrame(rows, columns=['slot_id','frame_ts','occupied_gt'])\
  .to_sql('parking_labels', ENGINE, if_exists='append', index=False)
