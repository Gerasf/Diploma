# parking_detector/logger.py
from sqlalchemy import create_engine, text
from datetime import datetime

# Используем те же креды, что в DbHandler
ENGINE = create_engine("postgresql://user:pwd@localhost/parking_finder",
                       pool_pre_ping=True)

def write_yolo_boxes(ts: datetime, boxes):
    """
    boxes: iterable[(x1, y1, x2, y2, conf)]
    """
    with ENGINE.begin() as conn:
        conn.execute(text("""
            INSERT INTO detection_log(frame_ts, bbox_pred, conf)
            VALUES (:ts, box(point(:x1,:y1), point(:x2,:y2)), :c)
        """), [
            {"ts": ts, "x1": b[0], "y1": b[1], "x2": b[2], "y2": b[3], "c": b[4]}
            for b in boxes
        ])

def write_slot_state(ts: datetime, occupied: dict[int, bool]):
    """
    occupied: {slot_id: True/False}
    """
    with ENGINE.begin() as conn:
        conn.execute(text("""
            INSERT INTO slot_state_log(slot_id, frame_ts, occupied_pred)
            VALUES (:slot, :ts, :occ)
        """), [
            {"slot": sid, "ts": ts, "occ": occ}
            for sid, occ in occupied.items()
        ])
