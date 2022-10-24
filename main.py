from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
#import pandas as pd

#latest_ids = pd.read_csv('latest_1000ids.csv').values.tolist()

driver = webdriver.Chrome('./chromedriver')

email = "ryo.ishimaru.kyoto@gmail.com"
password = "Tw35dfgcs"
keywords = ['データ分析', 'BI', 'ダッシュボード', 'API', 'tableau', 'gcp', '機械学習']

# login
try:
    driver.get('https://crowdworks.jp/login?ref=toppage_hedder')
    driver.find_element(By.NAME, 'username').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(by=By.CLASS_NAME, value='button-login').click()
    # Move to '仕事をさがす' page after login suucessfully
    driver.get('https://crowdworks.jp/public/jobs?category=jobs&order=score&ref=mypage_nav1')
    driver.find_element(By.NAME, 'search[keywords]').send_keys(keywords[0])
    driver.find_element(by=By.CLASS_NAME, value='cw-input_group_button').click()
    #sleep(3)
    # for i in item_titles:
    #     print(i.text)
    job_ids = driver.find_elements(by=By.XPATH, value='//div[@class="search_results"]/ul/li')
    urls = driver.find_elements(by=By.XPATH, value='//h3[@class="item_title"]/a')
    item_titles = driver.find_elements(By.CLASS_NAME, 'item_title')
    for j, i, u in zip(job_ids, item_titles, urls):
        job_id = j.get_attribute("data-job_offer_id")
        #if job_id not in latest_ids:
        item_name = i.text
        url = u.get_attribute('href')

        print(f'job_id: {job_id}, item_name:{item_name}, url:{url}')


finally:
    driver.close()

#print(username_textbox)

