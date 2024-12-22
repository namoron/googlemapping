import json
import numpy as np
from sklearn.ensemble import IsolationForest

# JSONファイル読み込み
with open('./Records.json', 'r') as f:
    data = json.load(f)

# 緯度経度データ抽出
coordinates = np.array([[(point['longitudeE7']/10000000), (point['latitudeE7']/10000000)] for point in data['locations']])

# 外れ値検出 (Isolation Forest)
clf = IsolationForest(contamination=0.05)  # 外れ値割合5%
outlier_pred = clf.fit_predict(coordinates)

# 外れ値除去
cleaned_data = coordinates[outlier_pred == 1]

print("Cleaned Data:", cleaned_data)
