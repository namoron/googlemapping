## Google Map のロケーション履歴を取得してマッピングするプログラムです
プログラムをクローンして[Google データ エクスポート](https://takeout.google.com/)でダウンロードしたRecords.jsonをDataフォルダの

forReco0.py はRecord.json から日時,座標のみを取り出してcsvに変換,htmlに出力するプログラム.

[kepler.gl](https://kepler.gl/demo) で見たいときはこのcsvを用いる.

htmlをpng に変換したいときはhtmlTopng.py を用いる.

各種パッケージや値の調整を行う.

# 完成図
![](https://github.com/namoron/googlemapping/assets/105638744/4e4be066-fb01-4f78-90c5-c60a5508e780)

## 参考にしたサイト
- [save-folium-map-as-png-image-using.html](https://nagasudhir.blogspot.com/2021/07/save-folium-map-as-png-image-using.html)
- [Googleロケーション履歴を使って整形(pandas)と地図上に表示(folium)させることを考える[初心者のPython3]](https://qiita.com/jam-goat/items/99dbdd4976544686a0ba)
