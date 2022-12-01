from selenium import webdriver
from selenium.webdriver.common.by import By
#from time import sleep
from redmail import gmail
import pandas as pd
import yaml
from yaml.loader import SafeLoader

# Configurations
with open('keywords.yml') as f:
    kw = yaml.load(f, Loader=SafeLoader)
latest_record_csv = 'lancers_latest_1000ids.csv'
latest_jobs = pd.read_csv(latest_record_csv)
latest_ids = latest_jobs['job_id'].tolist()

# Set up EmailSender for gmail
email = "ryo.ishimaru.kyoto@gmail.com"
gmail.user_name = email
gmail.password = 'ztbpamtijsfuffcy'

driver = webdriver.Chrome('./chromedriver')
password = "nDdstCb4Bky?P8zb"
keywords = kw['keywords']
ng_words = kw['ng_words'] #keywords to be ignored in job description

# login
try:
    driver.get('https://www.lancers.jp/user/login?ref=header_menu')
    driver.find_element(By.NAME, 'data[User][email]').send_keys(email)
    driver.find_element(By.NAME, 'data[User][password]').send_keys(password)
    driver.find_element(by=By.ID, value='form_submit').click()
    # Move to '仕事をさがす' page after login suucessfully
    # driver.get('https://crowdworks.jp/public/jobs?category=jobs&order=score&ref=mypage_nav1')

    new_jobs = {'job_id': [], 'title':[], 'url':[], 'client_name':[], 'price':[], 'keyword': []}
    for k in keywords:
        print(f'Working on {k}...')
        # driver.find_element(By.XPATH, '//div[@class="css-1rj2q6e"]/form/input').send_keys(k)
        driver.get(f'https://www.lancers.jp/work/search?keyword={k}')
    #     driver.find_element(by=By.CLASS_NAME, value='cw-input_group_button').click()
    #     job_ids = driver.find_elements(by=By.XPATH, value='//div[@class="search_results"]/ul/li')
        urls = driver.find_elements(By.CLASS_NAME, 'c-media__title')
        item_titles = driver.find_elements(By.CLASS_NAME, 'c-media__title-inner')
        client_names = driver.find_elements(By.CLASS_NAME, 'c-avatar__note')
        prices = driver.find_elements(By.CLASS_NAME, 'c-media__job-stats')
        job_status = driver.find_elements(By.CLASS_NAME, 'c-media__job-time__ttl')
        for t, u, c, p, s in zip(item_titles, urls, client_names, prices, job_status):
            job_id = str(u.get_attribute('href').split('/')[-1])
            title_name = t.text
            status = s.text
            price_info = str(p.text)
            if (job_id not in latest_ids) and (any(ext in title_name for ext in ng_words) != True)\
                and status != '募集終了' and c.text not in ['Lancers Agent', 'PROsheet', 'パーソルテクノロジースタッフ']\
                and ('コンペ' not in price_info):
                new_jobs['client_name'].append(c.text)
                new_jobs['job_id'].append(job_id)
                new_jobs['title'].append(title_name)
                new_jobs['url'].append(u.get_attribute('href'))
                new_jobs['price'].append(price_info)
                new_jobs['keyword'].append(k)
                print(title_name)
                print('---')
    #     driver.find_element(By.NAME, 'search[keywords]').clear()

    new_jobs = pd.DataFrame(new_jobs).drop_duplicates(subset=['job_id'])
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
        subject="New lancers jobs added",
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
