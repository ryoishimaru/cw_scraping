from selenium import webdriver
from selenium.webdriver.common.by import By
#from time import sleep
from redmail import gmail
import pandas as pd
# import datetime

# Configurations
# now = datetime.datetime.now()
latest_record_csv = 'latest_1000ids.csv'
latest_jobs = pd.read_csv(latest_record_csv)
latest_ids = latest_jobs['job_id'].tolist()

# Set up EmailSender for gmail
email = "ryo.ishimaru.kyoto@gmail.com"
gmail.user_name = email
gmail.password = 'ztbpamtijsfuffcy'

driver = webdriver.Chrome('./chromedriver')
password = "Tw35dfgcs"
keywords = ['データ分析', 'BI', 'ダッシュボード', 'API', 'tableau', 'gcp', '機械学習', 'Python', 'データ基盤']

# login
try:
    driver.get('https://crowdworks.jp/login?ref=toppage_hedder')
    driver.find_element(By.NAME, 'username').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(by=By.CLASS_NAME, value='button-login').click()
    # Move to '仕事をさがす' page after login suucessfully
    driver.get('https://crowdworks.jp/public/jobs?category=jobs&order=score&ref=mypage_nav1')

    new_jobs = {'job_id': [], 'item_name':[], 'url':[], 'client_name':[], 'price':[]}
    for k in keywords:
        print(f'Working on {k}...')
        driver.find_element(By.NAME, 'search[keywords]').send_keys(k)
        driver.find_element(by=By.CLASS_NAME, value='cw-input_group_button').click()
        job_ids = driver.find_elements(by=By.XPATH, value='//div[@class="search_results"]/ul/li')
        urls = driver.find_elements(by=By.XPATH, value='//h3[@class="item_title"]/a')
        item_titles = driver.find_elements(By.CLASS_NAME, 'item_title')
        client_names = driver.find_elements(by=By.XPATH, value='//div[@class="client-information"]/span[@class="user-name"]')
        prices = driver.find_elements(By.CLASS_NAME, 'entry_data_row')
        for j, i, u, c, p in zip(job_ids, item_titles, urls, client_names, prices):
            job_id = int(j.get_attribute("data-job_offer_id"))
            if job_id not in latest_ids:
                new_jobs['client_name'].append(c.text)
                new_jobs['job_id'].append(job_id)
                new_jobs['item_name'].append(i.text)
                new_jobs['url'].append(u.get_attribute('href'))
                new_jobs['price'].append(str(p.text))
                print(p.text)
                print('---')
        driver.find_element(By.NAME, 'search[keywords]').clear()

    new_jobs = pd.DataFrame(new_jobs).drop_duplicates(subset=['job_id'])
    new_jobs = new_jobs[~new_jobs['price'].str.contains('募集終了')]
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
