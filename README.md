## Google Map のロケーション履歴を取得してマッピングするプログラム

このレポジトリをダウンロードして[Google データ エクスポート](https://takeout.google.com/)でダウンロードしたRecords.jsonをDataフォルダに配置します。

### プログラムの概要

1. `remove.py`:
   - Records.json から位置情報データをフィルタリングし、速度や精度の閾値に基づいて不要なデータを削除します。
   - フィルタリングされたデータは `FilteredRecords.json` として保存されます。

2. `jsonToHTML.py`:
   - `FilteredRecords.json` を読み込み、位置情報データを整形して Folium を使用して地図上にプロットします。
   - プロットされた地図は `map.html` として保存されます。

3. `htmlTopng.py`:
   - `map.html` を読み込み、Selenium を使用して地図を PNG 画像として保存します。

### 使用方法

1. 必要なパッケージをインストールします。

   ```sh
   pip install -r requirements.txt
   ```

# 完成図
![image](https://github.com/user-attachments/assets/eac7b683-69ea-4872-9f08-8304d6fbce4d)


## 参考にしたサイト
- [save-folium-map-as-png-image-using.html](https://nagasudhir.blogspot.com/2021/07/save-folium-map-as-png-image-using.html)
- [Googleロケーション履歴を使って整形(pandas)と地図上に表示(folium)させることを考える[初心者のPython3]](https://qiita.com/jam-goat/items/99dbdd4976544686a0ba)
