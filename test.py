import json
from datetime import datetime
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    """
    ハーバーサイン公式を使用して2地点間の距離を計算 (km単位)
    """
    R = 6371.0  # 地球半径 (km)
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def remove_outliers_iqr(data):
    """
    IQR法を使用して異常値を除外
    """
    latitudes=[]
    longitudes=[]
    for entry in data:
        try:
            latitudes.append(entry['latitudeE7'] / 1e7)
            longitudes.append(entry['longitudeE7'] / 1e7)
        except KeyError:
            continue

    # 緯度のIQR計算
    q1_lat, q3_lat = np.percentile(latitudes, [25, 75])
    iqr_lat = q3_lat - q1_lat
    lower_bound_lat = q1_lat - 1.5 * iqr_lat
    upper_bound_lat = q3_lat + 1.5 * iqr_lat

    # 経度のIQR計算
    q1_lon, q3_lon = np.percentile(longitudes, [25, 75])
    iqr_lon = q3_lon - q1_lon
    lower_bound_lon = q1_lon - 1.5 * iqr_lon
    upper_bound_lon = q3_lon + 1.5 * iqr_lon

# 条件を分けて記述
    filtered_data = []
    for entry in data:
        try:
            latitude = entry['latitudeE7'] / 1e7
            longitude = entry['longitudeE7'] / 1e7
            if lower_bound_lat <= latitude <= upper_bound_lat and lower_bound_lon <= longitude <= upper_bound_lon:filtered_data.append(entry)
        except KeyError:
            continue
    
    return filtered_data

def filter_location_data(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        data = json.load(infile)

    # IQR法で異常値を除外
    filtered_locations_iqr = remove_outliers_iqr(data['locations'])

    filtered_locations_final = []
    previous_entry = None

    for entry in filtered_locations_iqr:
        try:
            accuracy = entry.get('accuracy', float('inf'))
            timestamp = entry['timestamp']
            lat = entry['latitudeE7'] / 1e7
            lon = entry['longitudeE7'] / 1e7

            # 時間差と速度計算の準備
            if previous_entry:
                prev_lat = previous_entry['latitudeE7'] / 1e7
                prev_lon = previous_entry['longitudeE7'] / 1e7
                prev_time = datetime.fromisoformat(previous_entry['timestamp'][:-1])
                curr_time = datetime.fromisoformat(timestamp[:-1])
                time_diff = abs((curr_time - prev_time).total_seconds())
                speed = haversine(prev_lat, prev_lon, lat, lon) / (time_diff / 3600) if time_diff > 0 else 0
            else:
                speed = 0

            # 精度と速度に基づくフィルタリング
            if accuracy >= 30 and speed <= 100:
                filtered_locations_final.append(entry)

            previous_entry = entry

        except (KeyError, ValueError):
            continue

    # フィルタリング結果を新しいJSONファイルに保存
    with open(output_filename, 'w') as outfile:
        json.dump({'locations': filtered_locations_final}, outfile, indent=4)

if __name__ == '__main__':
    input_file = 'Records.json'   # 入力ファイル名
    output_file = 'FilteredRecords4.json'   # 出力ファイル名
    filter_location_data(input_file, output_file)
