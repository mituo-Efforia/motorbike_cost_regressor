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
    * スクレイピングで取得してきたデータ。
    * 店舗ごとの入力のため、バイク名の入力や色なども様々のため、データ各種データ整形を行う必要あり。
    * 
    
  * scrapeで収集したデータをdata整形で加工後parquetファイルにて保存した。
  * 各データについての説明
    * dashboard_data.parquet : main.ipynbに読み込ませるデータ。　下記の二つのデータを結合し、該当するレースのみを抽出、加工したデータ。
    (20115 rows × 39 columns)
    * horse_data_2012_2021.parquet : horse_data_2012_2021.zip内のデータを結合し、加工を施したデータ。(加工内容に関してはdata整形を参照。)
    (1390261 rows × 25 columns)
    * race_data_2012_2021.parquet : race_data_2012_2021.zip内のデータを結合し、加工を施したデータ。(加工内容に関してはdata整形を参照。)
    (488126 rows × 19 columns)
      
* 'data整形用'
  * scrapeで収集してきたデータを適切な形に変換したnotebook
  * 下記に各notebookでの加工内容概要を記載
    * race_data_concat.ipynb : 分割して取得したrace_dataを結合し、以下の加工をした。
      *  カラムの半角スペースを削除し、扱いやすさを改善。
      *  可視化様に走破タイムを秒単位に変換。
      *  馬体重、性齢などの2つの要素が入っているカラムの情報分割。
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

* 'scrape'
  *  Webサイトスクレイピング実行用のnotebook、およびその処理を関数化したpythonファイルを格納
  *  主に2つのurl群をスクレイピング
  *  下記のrace_dataスクレイピングurlからテーブルデータ部分を取得。
     horse_dataスクレイピングurlからテーブルデータを取得。
