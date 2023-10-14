from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path
import os
import shutil
from zipfile import ZipFile

url = 'https://bd854828.xdrive.jp/index.php/s/m559pj97y9e7ZJ4?path=%2F%E5%8F%97%E6%B3%A8'
tmp_dir_name = 'tmp'
tmp_dir = Path(Path.cwd(), tmp_dir_name)

# def create_tmp_directory():
#         # print("Create temporary directory")
#         tmp_dir = Path(Path.cwd(), tmp_dir_name)
#         # Check if the directory exists before deleting
#         if tmp_dir.exists() and tmp_dir.is_dir():
#             # Delete the directory
#             # shutil.rmtree(tmp_dir)
#             print("tmp directory already exists.")
#         else:
#             print("tmp directory does not exist.")

#             tmp_dir = Path(Path.cwd(), tmp_dir_name)
#             tmp_dir.mkdir(exist_ok=True, parents=True)
#             print("Created empty temporary directory")

#             return tmp_dir

def get_drivers(tmp_dir, driver_path='./chromedriver'):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": str(tmp_dir)}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(driver_path, options=chrome_options)

    wait = WebDriverWait(driver=driver, timeout=30)

    return driver, wait

# tmp_dir = create_tmp_directory()
driver, wait = get_drivers(tmp_dir)

try:
    # driver.get(url)
    # wait.until(EC.presence_of_all_elements_located)
    # sleep(90)
    # fl = driver.find_element(By.ID, 'fileList')
    # tds = fl.find_elements(By.CLASS_NAME, 'name')

    # dl_url_list = []
    # for t in tds:
    #     dl_url = t.get_attribute('href')
    #     dl_url_list.append(dl_url)
    #     print(dl_url)
    base_url = 'https://bd854828.xdrive.jp/index.php/s/m559pj97y9e7ZJ4/download?path=%2F%E5%8F%97%E6%B3%A8&files=%E6%B3%A8%E6%96%87_'

    for idx in range(85, 153):
        print(f'Working on {idx}...')
        url = base_url + str(idx) + '.csv'
        driver.get(url)

        dl_files = [i for i in os.listdir(tmp_dir_name) if i.endswith('csv')]
        max_limit = 60*60*10
        time_past = 0
        while True:
            waiting_time = 30
            print(f'{time_past} seconds past')
            sleep(waiting_time)
            dl_files_next = [i for i in os.listdir(tmp_dir_name) if i.endswith('csv')]
            if len(dl_files_next) - len(dl_files) == 1:
                 break
            time_past += waiting_time
            if time_past > max_limit:
                raise Exception('max_limit of waiting time exceeded')


finally:
    driver.close()
    # shutil.rmtree(tmp_dir_name)