from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import DBD_page as DBD

# main website
url = "https://datawarehouse.dbd.go.th/index"

# list of column names
column_names = ['ลำดับ', 'เลขทะเบียนนิติบุคคล', 'ชื่อนิติบุคคล', 'TSIC_CODE', 'ประเภทธุรกิจ', 'วัตถุประสงค์', 'ประเภทธุรกิจตอนจดทะเบียน',
                'วัตถุประสงค์ตอนจดทะเบียน', 'ประเภทนิติบุคคล', 'วันที่จดทะเบียนจัดตั้ง', 'ทุนจดทะเบียน', 'เลขทะเบียนเดิม',
                 'กลุ่มธุรกิจ', 'ขนาดธุรกิจ', 'ปีที่ส่งงบการเงิน', 'ที่ตั้งสำนักงานใหญ่', 'Website', 'รายชื่อกรรมการ', 'กรรมการลงชื่อผูกพัน']
df = pd.DataFrame(columns = column_names)
not_empty_df = False

# set initial item number (refer to the last created file)
next_item = 25

# initialize Chrome driver
driver = DBD.initiate_chrome(url, headless = False)

# close modal warning
mdw_close_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "btnWarning")))
mdw_close_button.click()

# find the search box
search_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "key-word")))
search_box.clear()
search_box.send_keys(Keys.RETURN)

# find advanced filter
time.sleep(3)
advanced_filter = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-filter-advanced")))
advanced_filter.click()

# fill in the filter
current_status = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filterForm1"]/div[2]/div/div/input')))

current_status = driver.find_element(By.XPATH, '//*[@id="filterForm1"]/div[2]/div/div/input')
current_status.clear()
current_status.send_keys(Keys.ARROW_DOWN)
current_status.send_keys(Keys.RETURN)
current_status.send_keys(Keys.ARROW_DOWN)
current_status.send_keys(Keys.RETURN)
current_status.send_keys(Keys.ARROW_DOWN)
current_status.send_keys(Keys.RETURN)

# search again with filter
filter_search = driver.find_element(By.ID, "filterBtn")
filter_search.click()

# close filter
filter_close_button = driver.find_element(By.XPATH, "/html/body/div[3]/button")
filter_close_button.click()

# sort by tsic
sorter = Select(driver.find_element(By.ID, "sortBy"))
sorter.select_by_value("submitObjCode")

# wait for the page to load and find the total page number
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fixTable"]/tbody/tr[1]')))
total_pages = int(driver.find_element(By.ID, "sTotalPage").text.replace(',', ''))

# calculate page number and item number from the next_item
page_number = (next_item // 10) + 1
item_number = next_item  % 10
initial_page = True
DBD.change_page(driver, page_number)

# loop through the pages
while page_number <= total_pages:
    DBD.wait_search_result_to_load(driver)

    # open each company page in new tab
    for i in range(1, 11):
        # skip items before the initial item
        if initial_page and i < item_number:
            continue
        
        # stop the condition above after finding the initial item
        initial_page = False

        # get data and link from search page
        company_link, company_tsic, data_from_search_result = DBD.get_data_and_link_from_search_result(driver, i)

        # open the new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(company_link)
        time.sleep(1)

        # get data from company page
        data_from_company_page = DBD.get_data_from_company_page(driver, i)

        # if no dataframe or new tsic
        if not_empty_df and df.iloc[-1, 3] != company_tsic:
            df.to_csv('/Users/yoongsomporn.t/Desktop/Projects/Test_WebScraping/DBD_by_tsic/TSIC{}.csv'.format(df.iloc[-1, 3]))
            df = pd.DataFrame(columns = column_names)
            not_empty_df = False

        # add row to dataframe
        df.loc[len(df.index)] = data_from_search_result + data_from_company_page
        not_empty_df = True

        # close the new tab
        driver.execute_script("window.close('');")
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

    # change page
    page_number += 1
    DBD.change_page(driver, page_number)

# make index start from 1
df.index += 1

# save file
df.to_csv('/Users/yoongsomporn.t/Desktop/Projects/Test_WebScraping/DBD_by_tsic/TSIC{}.csv'.format(df.iloc[-1, 3]))

# quit the driver
time.sleep(5)
driver.quit()