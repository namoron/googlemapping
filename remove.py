import json
from datetime import datetime
# 速度の閾値（km/h）
SPEED_THRESHOLD = 1500
# 位置情報の精度の閾値（m）
ACCURACY_THRESHOLD = 1000

# 速度計算
def calculate_speed(lat1, lon1, lat2, lon2, time_diff):
    # 緯度・経度の差から距離を計算（概算）
    distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5 * 111  # km換算
    return (distance / (time_diff / 3600)) if time_diff > 0 else 0

# 位置情報データのフィルタリング
def filter_location_data(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        data = json.load(infile)

    filtered_locations = []
    previous_entry = None
    i=0
    j=0
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
                    stop_count= 10
                if stop_count > 0:
                    stop_count-=1
            else:
                speed = 0

            # 条件に基づきデータをフィルタリング
            if accuracy <= ACCURACY_THRESHOLD and speed <=SPEED_THRESHOLD  and stop_count <= 1 :
                j+=1
                buff['latitudeE7']=entry['latitudeE7']
                buff['longitudeE7']=entry['longitudeE7']
                buff['accuracy']=accuracy
                buff['source']=entry.get('source', None)
                buff['deviceTag']=entry.get('deviceTag', None)
                buff['deviceDestination']=entry.get('deviceDestination', None)
                buff['timestamp']=timestamp
                filtered_locations.append(buff)

            previous_entry = entry
            i+=1

        # データが不完全な場合はスキップ
        except (KeyError, ValueError):
            continue

    # フィルタリング結果を新しいJSONファイルに保存
    with open(output_filename, 'w') as outfile:
        json.dump({'locations': filtered_locations}, outfile, indent=4)

if __name__ == '__main__':
    input_file = 'Records.json'   # 入力ファイル名
    output_file = 'FilteredRecords2.json'   # 出力ファイル名
    filter_location_data(input_file, output_file)
