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
latest_record_csv = 'coconala_latest_1000ids.csv'
latest_jobs = pd.read_csv(latest_record_csv)
latest_ids = latest_jobs['job_id'].tolist()

# Set up EmailSender for gmail
email = "ryo.ishimaru.kyoto@gmail.com"
gmail.user_name = email
gmail.password = 'ztbpamtijsfuffcy'

driver = webdriver.Chrome('./chromedriver')
password = "$YmcnR$S?yteH38x"
keywords = kw['keywords']
ng_words = kw['ng_words'] #keywords to be ignored in job description

# login
# try:
driver.get('https://coconala.com/login?redirect_to=https%3A%2F%2Fcoconala.com%2F')
driver.find_element(By.NAME, 'data[User][login_email]').send_keys(email)
driver.find_element(By.NAME, 'data[User][login_password]').send_keys(password)
driver.find_element(by=By.CLASS_NAME, value='frontButton').click()
driver.find_element(by=By.CLASS_NAME, value='c-trigger').click()

# Move to '仕事をさがす' page after login suucessfully


    # new_jobs = {'job_id': [], 'title':[], 'url':[], 'client_name':[], 'price':[], 'keyword': []}
    # for k in keywords:
    #     print(f'Working on {k}...')
    #     driver.find_element(by=By.CLASS_NAME, value='c-searchKeyword').send_keys(k)
    #     driver.find_element(by=By.CLASS_NAME, value='button').click()
    #     break
#         job_ids = driver.find_elements(by=By.XPATH, value='//div[@class="search_results"]/ul/li')
#         urls = driver.find_elements(by=By.XPATH, value='//h3[@class="item_title"]/a')
#         item_titles = driver.find_elements(By.CLASS_NAME, 'item_title')
#         client_names = driver.find_elements(by=By.XPATH, value='//div[@class="client-information"]/span[@class="user-name"]')
#         prices = driver.find_elements(By.CLASS_NAME, 'entry_data_row')
#         for j, t, u, c, p in zip(job_ids, item_titles, urls, client_names, prices):
#             job_id = int(j.get_attribute("data-job_offer_id"))
#             title_name = t.text
#             price_info = str(p.text)
#             client_name = c.text
#             if (job_id not in latest_ids) and (any(ext in title_name for ext in ng_words) != True) and ('タスク' not in price_info) and (client_name not in ['skillupai']):
#                 new_jobs['client_name'].append(client_name)
#                 new_jobs['job_id'].append(job_id)
#                 new_jobs['title'].append(title_name)
#                 new_jobs['url'].append(u.get_attribute('href'))
#                 new_jobs['price'].append(price_info)
#                 new_jobs['keyword'].append(k)
#                 print(title_name)
#                 print('---')
#         driver.find_element(By.NAME, 'search[keywords]').clear()

#     new_jobs = pd.DataFrame(new_jobs).drop_duplicates(subset=['job_id'])
#     if len(new_jobs) > 0:
#         new_jobs = new_jobs[~new_jobs['price'].str.contains('募集終了')]
#     print(f'{len(new_jobs)} new jobs detected.')

#     all_jobs = pd.concat([latest_jobs, new_jobs]).drop_duplicates(subset=['job_id'])
#     if len(all_jobs) > 1000:
#         all_jobs = all_jobs.iloc[-1000:, :]
#     all_jobs.to_csv(latest_record_csv, index=False)
#     print('New jobs added to latest1000ids.csv')

# finally:
#     driver.close()

# if len(new_jobs) > 0:
#     gmail.send(
#         subject="New cw jobs added",
#         sender=email,
#         receivers=[email],
#         html="""
#         <p>{{ job_num }} new jobs added:</p>
#         {{ job_table }}
#         """,
#         body_tables={
#             'job_table': new_jobs
#         },
#         body_params={
#             'job_num': len(new_jobs)
#         }
#     )
