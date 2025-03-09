# Google Map のロケーション履歴を取得してマッピングするプログラム
## 使い方
1. このレポジトリをダウンロード

2. [Google データ エクスポート](https://takeout.google.com/)でダウンロードしたRecords.jsonをDataフォルダにいれる

3. 各種パッケージをインストール

4. `remove.py`を実行して、不要な位置情報データを削除する

5. `jsonToHTML.py`を実行して、地図上にプロットし、HTML ファイルとして保存する


[kepler.gl](https://kepler.gl/demo) などで見たいときはoutput.csvを用いる.

## 完成図
![image](https://github.com/user-attachments/assets/eac7b683-69ea-4872-9f08-8304d6fbce4d)


## スクリプトの説明

### `remove.py`
`remove.py` は、Google データ エクスポートから取得した `Records.json` ファイルをフィルタリングし、速度と精度の閾値に基づいて不要な位置情報データを削除します。フィルタリングされたデータは `FilteredRecords.json` として保存されます。

- 入力ファイル: `./Data/Records.json`
- 出力ファイル: `./Data/FilteredRecords.json`

### `jsonToHTML.py`
`jsonToHTML.py` は、フィルタリングされた位置情報データを読み込み、Folium を使用して地図上にプロットし、HTML ファイルとして保存します。

- 入力ファイル: `./Data/FilteredRecords.json`
- 出力ファイル: `./Data/map.html`

## 参考にしたサイト
- [Googleロケーション履歴を使って整形(pandas)と地図上に表示(folium)させることを考える[初心者のPython3]](https://qiita.com/jam-goat/items/99dbdd4976544686a0ba)
