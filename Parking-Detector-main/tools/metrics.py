import pandas as pd, sqlalchemy as sa, argparse
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

parser = argparse.ArgumentParser()
parser.add_argument('--t0'); parser.add_argument('--t1')
args = parser.parse_args()

E = sa.create_engine("postgresql://user:pwd@localhost/parking_finder")

sql = """
SELECT l.slot_id, l.frame_ts, l.occupied_gt, s.occupied_pred
FROM   parking_labels  l
JOIN   slot_state_log s USING (slot_id, frame_ts)
WHERE  (:t0 IS NULL OR l.frame_ts >= :t0)
  AND  (:t1 IS NULL OR l.frame_ts <= :t1)
"""
df = pd.read_sql(sql, E, params={'t0': args.t0, 't1': args.t1})

print(f"Samples: {len(df)}")
print("Accuracy :",  accuracy_score(df.occupied_gt, df.occupied_pred))
print("Precision:", precision_score(df.occupied_gt, df.occupied_pred))
print("Recall   :", recall_score(df.occupied_gt, df.occupied_pred))
print("F1-score :", f1_score(df.occupied_gt, df.occupied_pred))
