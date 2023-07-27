from selenium import webdriver
from selenium.webdriver.common.by import By
#from time import sleep
from redmail import gmail
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from time import sleep

# Configurations
with open('keywords.yml') as f:
    kw = yaml.load(f, Loader=SafeLoader)
latest_record_csv = 'coconala_latest_1000ids.csv'
latest_jobs = pd.read_csv(latest_record_csv)
latest_ids = latest_jobs['job_id'].tolist()

# Set up EmailSender for gmail
email = "ryo.ishimaru.kyoto@gmail.com"
# password = "$YmcnR$S?yteH38x"
gmail.user_name = email
gmail.password = 'ztbpamtijsfuffcy'

driver = webdriver.Chrome('./chromedriver')
keywords = kw['keywords']
ng_words = kw['ng_words'] #keywords to be ignored in job description

try:

    # test block
    # for title, client, price in zip(job_titles, clients, prices):
    #   print(f'job title: {title.text}')
    #   url = title.find_element(By.TAG_NAME, "a").get_attribute("href")
    #   print(f'url: {url}')
    #   print(f'client: {client.text}')
    #   print(f'price: {price.text}')
    # sleep(50)

    new_jobs = {'job_id': [], 'title':[], 'url':[], 'client_name':[], 'price':[], 'keyword': []}
    for k in keywords:
        print(f'Working on {k}...')
        driver.get(f'https://coconala.com/requests?keyword={k}&recruiting=true')
        job_titles = driver.find_elements(By.CLASS_NAME, 'c-itemInfo_title')
        #urls = job_titles.find_elements(By.TAG_NAME, "a")# .get_attribute("href")
        clients = driver.find_elements(By.CLASS_NAME, 'c-itemInfoUser_name')
        #status = driver.find_elements(By.CLASS_NAME, 'c-itemTileLine')
        prices = driver.find_elements(By.CLASS_NAME, 'd-requestPrice_emphasis')

        for title, client, price in zip(job_titles, clients, prices):
            url = title.find_element(By.TAG_NAME, "a").get_attribute("href")
            job_id = int(url.split('/')[-1])
            title_name = title.text
            price_info = str(price.text)
            client_name = client.text
            if (job_id not in latest_ids) and (any(ext in title_name for ext in ng_words) != True)\
                and client_name not in ['']:
                new_jobs['client_name'].append(client_name)
                new_jobs['job_id'].append(job_id)
                new_jobs['title'].append(title_name)
                new_jobs['url'].append(url)
                new_jobs['price'].append(price_info)
                new_jobs['keyword'].append(k)
                print(title_name)
                print('---')

    new_jobs = pd.DataFrame(new_jobs).drop_duplicates(subset=['job_id'])
    print(f'{len(new_jobs)} new jobs detected.')

    all_jobs = pd.concat([latest_jobs, new_jobs]).drop_duplicates(subset=['job_id'])
    if len(all_jobs) > 1000:
        all_jobs = all_jobs.iloc[-1000:, :]
    all_jobs.to_csv(latest_record_csv, index=False)
    print('New jobs added to coconala_latest_1000ids.csv')

finally:
    driver.close()

if len(new_jobs) > 0:
    gmail.send(
        subject="New coconala jobs added",
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
