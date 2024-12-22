import json
from datetime import datetime
# 速度の閾値（km/h）
SPEED_THRESHOLD = 1500
# 位置情報の精度の閾値（m）
ACCURACY_THRESHOLD = 1000
# 速度が閾値を超えた場合の停止期間
STOP_THRESHOLD = 10
# 入力ファイル名
INPUT_FILENAME = './Data/Records.json'
# 出力ファイル名
OUTPUT_FILENAME = './Data/FilteredRecords.json'

# 速度計算
def calculate_speed(lat1, lon1, lat2, lon2, time_diff):
    # 緯度・経度の差から距離を計算（概算）
    distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5 * 111  # km換算
    return (distance / (time_diff / 3600)) if time_diff > 0 else 0

# 位置情報データのフィルタリング
def filter_location_data(INPUT_FILENAME, OUTPUT_FILENAME):
    with open(INPUT_FILENAME, 'r') as infile:
        data = json.load(infile)

    filtered_locations = []
    previous_entry = None
    stop_count=0
    for entry in data['locations']:
        try:
            buff={}
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
                speed = calculate_speed(prev_lat, prev_lon, lat, lon, time_diff)
                # 速度が閾値を超えた場合は一定期間データ削除
                if speed >=SPEED_THRESHOLD:
                    stop_count= STOP_THRESHOLD
                if stop_count > 0:
                    stop_count-=1
            else:
                speed = 0

            # 条件に基づきデータをフィルタリング
            if accuracy <= ACCURACY_THRESHOLD and speed <= SPEED_THRESHOLD and stop_count == 0:
                filtered_locations.append({
                    'latitudeE7': entry['latitudeE7'],
                    'longitudeE7': entry['longitudeE7'],
                    'accuracy': accuracy,
                    'source': entry.get('source'),
                    'deviceTag': entry.get('deviceTag'),
                    'deviceDestination': entry.get('deviceDestination'),
                    'timestamp': timestamp
                })


            previous_entry = entry

        # データが不完全な場合はスキップ
        except (KeyError, ValueError):
            continue

    # フィルタリング結果を新しいJSONファイルに保存
    with open(OUTPUT_FILENAME, 'w') as outfile:
        json.dump({'locations': filtered_locations}, outfile, indent=4)

if __name__ == '__main__':
    filter_location_data(INPUT_FILENAME, OUTPUT_FILENAME)
