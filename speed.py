import pandas as pd
from datetime import datetime
import folium


def seikei():
    t = []
    l = []
    l2 = []
    df = pd.read_json('./FilteredRecords.json')
    min_lon, max_lon = -180, 180
    min_lat, max_lat = -90, 90

    # 初期設定
    time_old = datetime.fromisoformat(df.iat[0, 0]['timestamp'][:-1])
    distance = 0
    skipcount = 0

    for i in range(len(df)):
        try:
            accuracy = float(df.iat[i, 0]['accuracy'])
            time_str = df.iat[i, 0]['timestamp']
            time_new = datetime.fromisoformat(time_str[:-1])
            time_diff = abs((time_new - time_old).total_seconds())  # 秒単位で計算
            # print("time_new:", time_new)
            # 緯度・経度の計算
            lat_new = float(df.iat[i, 0]['latitudeE7']) / 10000000
            lon_new = float(df.iat[i, 0]['longitudeE7']) / 10000000

            if i > 0:  # 最初のループでは距離を計算しない
                lat_old = float(df.iat[i - 1, 0]['latitudeE7']) / 10000000
                lon_old = float(df.iat[i - 1, 0]['longitudeE7']) / 10000000

                # 距離計算（概算）
                distance = ((lat_new - lat_old) ** 2 + (lon_new - lon_old) ** 2) ** 0.5 * 111  # km換算

                # 時速計算
                speed = (distance / (time_diff / 3600)) if time_diff > 0 else 0

                if speed > 100:  # 時速300km/h以上は除外
                    skipcount += 1
                    continue

            if accuracy < 30:  # 精度が30未満の場合のみ記録
                t.append(time_new)
                l.append(lon_new)
                l2.append(lat_new)

            time_old = time_new
            i += 1
        except (IndexError, KeyError, ValueError):
            pass
        if i >=  len(df):
            print("skipcount", skipcount)
            break

    # データフレーム作成と保存
    d2 = pd.DataFrame({'date': t, 'lat': l2, 'lon': l})
    d2['date'] = d2['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    d2.to_csv('hist.csv', index=False)

    # 地図作成
    m = folium.Map(
        location=[35.0, 135.0], 
        zoom_start=10,
        tiles="cartodbdark_matter",
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,)
    loc = d2[['lat', 'lon']].values.tolist()
    
    loc = d2[['lat', 'lon']].values.tolist()

    folium.PolyLine(
        locations=loc,
        color='#ffffff',
        weight=1,
    ).add_to(m)

    m.save('map.html')


if __name__ == '__main__':
    seikei()
