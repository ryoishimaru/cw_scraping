from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from redmail import gmail
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# Configurations
with open('keywords.yml') as f:
    kw = yaml.load(f, Loader=SafeLoader)
latest_record_csv = 'cw_latest_1000ids.csv'
latest_jobs = pd.read_csv(latest_record_csv, dtype={'job_id':str})
latest_ids = latest_jobs['job_id'].tolist()

# Set up EmailSender for gmail
email = "ryo.ishimaru.kyoto@gmail.com"
gmail.user_name = email
gmail.password = 'ztbpamtijsfuffcy'

# Chrome WebDriverのオプションを設定
options = Options()
options.add_argument('--headless')
# chromedriverのパスを指定せずにChromeドライバーのインスタンスを作成
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver = webdriver.Chrome('./chromedriver')
# 最大の読み込み時間を設定。最大30秒待機できるようにする。
wait = WebDriverWait(driver=driver, timeout=30)

password = "Tw35dfgcs"
keywords = kw['keywords']
ng_words = kw['ng_words'] #keywords to be ignored in job description

job_search_url = 'https://crowdworks.jp/public/jobs/search?keep_search_criteria=true&order=score&hide_expired=true&search%5Bkeywords%5D='

# login
try:
    new_jobs = {'job_id': [], 'title':[], 'url':[], 'client_name':[], 'price':[], 'keyword': []}
    for k in keywords:
        print(f'Searching new jobs for {k}...')
        driver.get(f'{job_search_url}{k}')

        titles = driver.find_elements(by=By.CLASS_NAME, value='iCeus.TVMAc')
        status_days = driver.find_elements(by=By.CLASS_NAME, value='bZKIt')
        client_names = driver.find_elements(by=By.CLASS_NAME, value='uxHdW')
        job_boxes = driver.find_elements(by=By.CLASS_NAME, value='mLant')

        # print(len(titles))
        # print(len(status_days))
        # print(len(client_names))
        # print(len(job_boxes))

        for title, status, client_name, job_box in zip(titles, status_days, client_names, job_boxes):
            # Priceの情報はクラス名が時間単価か固定報酬かタスクか、などの契約形態により変わるためクラス名を指定する。タスクだったら無視
            try:
                price_info = job_box.find_element(by=By.CLASS_NAME, value='AIu_G').text
            except NoSuchElementException:
                try:
                    price_info = job_box.find_element(by=By.CLASS_NAME, value='zTNhw').text
                except NoSuchElementException:
                    continue

            title_block = title.find_element(by=By.TAG_NAME, value='a') #仕事名が格納されているブロック。hrefでURLのハイパーリンクも指定されている。
            url = title_block.get_attribute('href')
            job_id = url.split('/')[-1]

            if job_id in latest_ids:
                continue

            title = title.text
            if any(ext in title for ext in ng_words) == True:
                # print(f'{title} has NG words so skip...')
                continue

            client_name = client_name.text
            if client_name in ['skillupai', 'skillup-next', 'Crewto', 'Walk To See', 'tsuide2023', 'AxrossRecipe', '北村 渉', 'ASTU']:
                continue

            status = status.text
            if '募集終了' in status:
                continue

            new_jobs['client_name'].append(client_name)
            new_jobs['job_id'].append(job_id)
            new_jobs['title'].append(title)
            new_jobs['url'].append(url)
            new_jobs['price'].append(price_info)
            new_jobs['keyword'].append(k)

            print(title)
            print('---')

        driver.find_element(By.NAME, 'search[keywords]').clear()

    new_jobs = pd.DataFrame(new_jobs).drop_duplicates(subset=['job_id'])
    new_jobs = new_jobs.reset_index(drop=True)
    print(f'{len(new_jobs)} new jobs detected.')

    all_jobs = pd.concat([latest_jobs, new_jobs]).drop_duplicates(subset=['job_id'])
    if len(all_jobs) > 1000:
        all_jobs = all_jobs.iloc[-1000:, :]
    all_jobs.to_csv(latest_record_csv, index=False)
    print('New jobs added to latest1000ids.csv')

finally:
    driver.close()

if len(new_jobs) > 0:
    gmail.send(
        subject="New cw jobs added",
        sender=email,
        receivers=[email],
        html="""
        <p>{{ job_num }} new jobs added:</p>
        {{ job_table }}
        """,
        body_tables={
            'job_table': new_jobs
        },
        body_params={
            'job_num': len(new_jobs)
        }
    )
