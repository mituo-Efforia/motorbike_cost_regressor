# motorbike_cost_regressor
バイク王在庫データより中古バイクの価格予想モデルを作成したリポジトリです。

## 🏍️: 概要  
* 中古バイクの価格予想モデル。
* 手法:randomforest_regressor(詳細についてはモデル作成用)
  比較としてlightgbmによる回帰を行ったが、randomforestの方が精度が高かったため、上記モデルを使用。
* 比較指標:MAPE
* 使用データ:
  * 20231115時点バイク王在庫データ(元データの詳細についてはscrapeの説明に記載)
  * train_data:4481 rows × 12 columns
  * test_data:1119 rows × 12 columns



## 📚: リポジトリの構成  

* 'モデル作成用'
  機械学習モデル作成用のフォルダ
  * randomforest
    * 評価指標:高額商品の価格の商品の価格予想ということもあり、評価指標としてはMAPEを使用した。(RMSEでは視覚的に判断しにくいため。)
    * 精度:
      訓練データMAPE 0.07119455889801628(7.11%)
      テストデータMAPE 0.14617753687942753(14.6%)
      訓練データ決定係数 0.9853985841648546
      テストデータ決定係数 0.8024717462908885

    * 特徴量:
      * model_year
      * color(このままでは使用できないためdummyencodingを実施)
      * mileage 
      * gurantee_period
      * brand(このままでは使用できないためdummyencodingを実施)
      * type(このままでは使用できないためdummyencodingを実施)
      * displacement
        カテゴリー変数の扱いについて:RandomForestもlightgbmもノンパラメトリック手法のため、Rabelencodingでも良かったのだが、評価結果がこちらの方が良かったため、こちらを採用。

    * モデルチューニング:Oputunaとcrossvalidationを使用して実施。(最適化指標としてはMAPEを使用)
  
  * lightgbm
    * 精度:
      訓練データMAPE 0.0775194534610013 (7.75%)
      テストデータMAPE 0.1590659126331084 (15.9%)
      訓練データ決定係数 0.9886350866681443
      テストデータ決定係数 0.7724904063586567
  
    * 評価指標、特徴量　、　モデルチューニング:RandomForestと同様
  
      
* 'data'
  * 元データ
    * 20231115分割:スクレイピング時に途切れてしまうことがあり、分けて取得。
    * bike_info_20231115.csv:スクレイピングで取得してきたデータ。(6107 rows × 13 columns)
      店舗ごとの入力のため、バイク名の入力や色なども様々のため、データ各種データ整形を行う必要あり。
    * data_crf_ktm_reshape.csv:スクレイピングしたデータを一部整形し、どうしても手入力が必要なため、一時保存したファイル
    * bike_info_with_tenpo.csv:スクレイピングしたデータを整形したデータ。この段階では正規化などはしていない。
      
  * 整形後データ
    元データのbike_info_with.tenpo.csvを元に第3正規化までしたファイル
    * bike_info.csv:バイクの個体情報(色、年式、走行距離)などの情報が入ったデータ
    * modelnumber.csv:バイクの型式番号をkeyに排気量やタイプなどの情報が入ったデータ
    * tenpo_data.csv:店舗idをkeyに店舗の住所などの情報が入ったデータ
   
  * アップロード用データ
    bigqueryにアップロードするように整形後データを加工したデータ(カラム名を日本語から英語に変更した。)
    * bike_info.csv:バイクの個体情報(色、年式、走行距離)などの情報が入ったデータ
    * modelnumber.csv:バイクの型式番号をkeyに排気量やタイプなどの情報が入ったデータ
    * tenpo_data.csv:店舗idをkeyに店舗の住所などの情報が入ったデータ

  * 機械学習用データ
    アップロードデータをtrain_dataとtest_dataに分割し、保管しているファイル。
    
      
* 'データ整形用'
  * scrapeで収集してきたデータを正規化、機械学習への利用を可能にするために変換したnotebook
  * 下記に各notebookでの加工内容概要を記載
    * データ整形用(型式、名称).ipynb : bike_info_20231115.csvに下記の整形を実施。
      実施内容多数のため概要のみ記載(詳細はnotebookをご参照ください。)
      *  不要カラムの削除
      *  全角文字(数字、記号、カタカナ)を半角に変換
      *  各カラムから不要な文字列、記号を削除
    * データ整形用(color).ipynb :
      * 店舗によるデータ入力のため、色の入力もまちまちだったので、下記の色にまとめた。
        黒、青、赤、黄、緑、オレンジ、茶、ピンク、紫、白、銀
    * カラム名変更
      * bigqueryにアップロード時に日本語カラムが文字化けしてしまうことを知らなかったため、英語名に変換した。
        
    * horse_data_concat.ipynb : 分割して取得したhorse_dataを結合し、以下の加工をした。
      *  カラムの半角スペースを削除し、扱いやすさを改善。
      *  映像列など欠損値しかないカラムの削除
      *  芝2000の様な距離と馬場素材が入っているカラムを
         と2000の様にsurfaceと距離で情報分割。
    * dashboard_data_reshape.ipynb : 上記2データを加工して結合し、dashborard様に更に加工をしたデータ。
      * horse_dataから両方に重複するカラムの削除
      * horse_dataの方のrace_idに海外レースのidがstr型のためintに変換
      * horse_idとrace_idをkeyに結合
      * ソートに必要な開催年、レースレベル列の作成。
    * parquet_convert : 各データがcsvだと大きすぎてアップロードができなかったため、変換した。

* '分析用'
  *　 EDA
  * 下記に各notebookでの加工内容概要を記載
    * データ整形用(型式、名称).ipynb : bike_info_20231115.csvに下記の整形を実施。
      実施内容多数のため概要のみ記載(詳細はnotebookをご参照ください。)
      *  不要カラムの削除
      *  全角文字(数字、記号、カタカナ)を半角に変換
      *  各カラムから不要な文字列、記号を削除
    * データ整形用(color).ipynb :
      * 店舗によるデータ入力のため、色の入力もまちまちだったので、下記の色にまとめた。
        黒、青、赤、黄、緑、オレンジ、茶、ピンク、紫、白、銀

* 'scrape'
  *  Webサイトスクレイピング実行用のnotebook、およびその処理を関数化したpythonファイルを格納
  *  主に2つのurl群をスクレイピング
  *  下記のrace_dataスクレイピングurlからテーブルデータ部分を取得。
     horse_dataスクレイピングurlからテーブルデータを取得。
