import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from tqdm import tqdm
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 例外処理用のlibraryをimport
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm

#urlのサイトからバイクIDを取得する関数
def id_scraping(url ='https://www.8190.jp/wish/ds/bike/search/'):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    num_do=1
    #取ってきたIDを保管するリスト
    id_list = []
    #1,2回目と最終ページだけ driver.find_element(By.XPATH,'//section[3]/div[2]/div/div[5]')が空欄になることを利用してwhile文を回す
    #1,2ページ目とそれ以外で次ページ遷移のボタンが異なるため、while文内を条件指定でボタンを決める
    while num_do <= 2 or driver.find_element(By.XPATH,'//section[3]/div[2]/div/div[5]') != '' :
        try:
            if num_do == 1 :
                bottun = driver.find_element(By.XPATH,'//section[3]/div[2]/div/div[3]')
            elif num_do == 2:
                bottun = driver.find_element(By.XPATH,'//section[3]/div[2]/div/div[4]')
            else :
                bottun = driver.find_element(By.XPATH,'//section[3]/div[2]/div/div[5]')
            #情報を取得する処理
            name_elements = driver.find_elements(by=By.CLASS_NAME,value='name')
            for i in range(len(name_elements)):
                target = name_elements[i].get_attribute('outerHTML')
                pattern = r'/wish/ds/bike/(\d+)/'
                id = re.search(pattern,target)
                id_list.append(id.group(1))
            #ボタンをクリックする処理
            bottun.click()
            #全体の表示を待つ
            # wait.until(EC.presence_of_element_located((By.XPATH,'body')))
            time.sleep(5)
            num_do +=1
        except Exception as e:
            print(e)
            break
        except :
            break
    driver.close
    return id_list

#IDからバイクの情報を取得する関数
def bike_info_scrape(id_list):
    id_list=list(set(id_list))
    columns = ['id','価格','車両名','メーカー','型式番号','モデル年','排気量','色','タイプ',
           '走行距離','保証期間','初年度登録年月','次回車検','入荷日','在庫店舗','在庫店舗電話','備考']
    df = pd.DataFrame(index=[],columns=columns)
    driver = webdriver.Chrome()
    for id in tqdm(id_list):
        time.sleep(1)
        try:
            url = 'https://www.8190.jp/wish/ds/bike/' + id
            driver.get(url)
            time.sleep(2)
            #車種
            name = driver.find_element(By.CLASS_NAME,'content').text.split('\u3000')[0]
            #備考
            sub_data = driver.find_element(By.CLASS_NAME,'content').text.split('\u3000')[1:]
            #価格
            motor_cost=driver.find_element(By.CLASS_NAME,'motor-cost').text.split('\n')[1].replace('￥','').replace(',','')
            #詳細データ
            motor_info =driver.find_element(By.CLASS_NAME,'motor-info').text.split('\n')
            #走行距離
            milage = motor_info[1].replace(',','').replace('km','')
            #保証期間
            warranty = motor_info[3].replace('年','')
            #在庫店舗
            store = motor_info[5]
            #メーカー名
            manufacture=driver.find_elements(By.CLASS_NAME,'linkBox')[1].text
            #排気量
            engine = driver.find_elements(By.CLASS_NAME,'linkBox')[2].text.replace('cc','')
            #色
            color = driver.find_elements(By.CLASS_NAME,'linkBox')[3].text
            #型式
            model_number = driver.find_elements(By.CLASS_NAME,'linkBox')[4].text
            #モデル年 
            model_year = driver.find_elements(By.CLASS_NAME,'linkBox')[5].text.replace('年','')
            #次回車検
            v_inspection =driver.find_elements(By.CLASS_NAME,'linkBox')[6].text
            #初年度登録年月
            first_register = driver.find_elements(By.CLASS_NAME,'linkBox')[7].text
            #車両タイプ(ツアラーとか)
            b_type = driver.find_elements(By.CLASS_NAME,'linkBox')[8].text
            #入荷日
            arrival_date = driver.find_elements(By.CLASS_NAME,'linkBox')[10].text
            #車台番号下4桁
            b_number = driver.find_elements(By.CLASS_NAME,'linkBox')[11].text
            #店舗電話番号
            phone_number = driver.find_elements(By.CLASS_NAME,'linkBox')[13].text
            #pd.Seriesの作成
            transaction = [id,motor_cost,name,manufacture,model_number,model_year,
                        engine,color,b_type,milage,warranty,first_register,v_inspection,
                        arrival_date,store,phone_number,sub_data]
            record = pd.Series(transaction,index=df.columns)
            df.loc[len(df)] = record
        except IndexError :
            continue
        except AttributeError :
            continue
        except UnicodeDecodeError :
            continue
        #seleniumにページが見つからなかった際に継続してくれる様のライブラリあり
        except NoSuchElementException:
            print("Element not found. Skipping to the next iteration.")
            continue
        except Exception as e:
            print(e)
            break
        except :
            break
    driver.close
    return(df)
        