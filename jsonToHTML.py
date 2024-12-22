import pandas as pd
from datetime import datetime
import folium
import asyncio
from pyppeteer import launch

# 速度の閾値（km/h）
SPEED_THRESHOLD = 1000
# 位置情報の精度の閾値（m）
ACCURACY_THRESHOLD = 1500
# 入力ファイル名
INPUT_FILENAME = './Data/FilteredRecords.json'
# 出力ファイル名
OUTPUT_FILENAME = './Data/map.html'

def seikei():
    t = []
    l = []
    l2 = []
    df = pd.read_json(INPUT_FILENAME)
    i = 0
    min_lon, max_lon = 0, 360
    min_lat, max_lat = -90, 90
    while i <= len(df):
        try:
            time_str = df.iat[i, 0]['timestamp']
            time = datetime.fromisoformat(time_str[:-1])
            lon = float(df.iat[i, 0]['longitudeE7'])/10000000
            lat = float(df.iat[i, 0]['latitudeE7'])/10000000
            if lon < -30:
                lon = 360 +lon 
            t.append(time)
            l.append(lon)
            l2.append(lat)
        except (IndexError, KeyError):
            pass
        if i >= len(df):  
            break
        i += 1
    d2 = pd.DataFrame({'date': t, 'lat': l2, 'lon': l})
    d2['date'] = d2['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # d2.to_csv('hist.csv')
    m = folium.Map(
        location=[35.0, 135.0], 
        zoom_start=10,
        tiles="cartodbdark_matter",
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        no_wrap=False,
        )
    loc = d2[['lat', 'lon']].values.tolist()
    folium.PolyLine(
        locations=loc,
        color='#ffffff',
        weight=1,
        ).add_to(m)
    m.save(OUTPUT_FILENAME)

if __name__ == '__main__':
    seikei()
