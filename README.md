![image](https://github.com/user-attachments/assets/4946c8a4-b374-4d08-8ea8-e759ebefb476)## Google Map のロケーション履歴を取得してマッピングするプログラムです
プログラムをクローンして[Google データ エクスポート](https://takeout.google.com/)でダウンロードしたRecords.jsonをDataフォルダの

forReco0.py はRecord.json から日時,座標のみを取り出してcsvに変換,htmlに出力するプログラム.

[kepler.gl](https://kepler.gl/demo) で見たいときはこのcsvを用いる.

htmlをpng に変換したいときはhtmlTopng.py を用いる.

各種パッケージや値の調整を行う.

# 完成図
![image](https://github.com/user-attachments/assets/eac7b683-69ea-4872-9f08-8304d6fbce4d)


## 参考にしたサイト
- [save-folium-map-as-png-image-using.html](https://nagasudhir.blogspot.com/2021/07/save-folium-map-as-png-image-using.html)
- [Googleロケーション履歴を使って整形(pandas)と地図上に表示(folium)させることを考える[初心者のPython3]](https://qiita.com/jam-goat/items/99dbdd4976544686a0ba)
