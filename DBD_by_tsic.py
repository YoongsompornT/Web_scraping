from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def initiate_chrome(headless = False):
    if headless:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('/Users/yoongsomporn.t/Desktop/Projects/Test_WebScraping/chromedriver', chrome_options = chrome_options)
    else:
        driver = webdriver.Chrome('/Users/yoongsomporn.t/Desktop/Projects/Test_WebScraping/chromedriver')
        driver.get(url)
        driver.maximize_window()
    
    return driver

def change_page(page_number):
    current_page = driver.find_element(By.ID, 'cPage')
    current_page.clear()
    current_page.send_keys(page_number)
    current_page.send_keys(Keys.RETURN)

def get_data_and_link_from_search_result(driver, i):
    try:
        # get link for each company page
        company = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fixTable"]/tbody/tr[{}]/td[4]/a'.format(i))))
        company_link = company.get_attribute('href')
                
        # store data from search result page
        company_name = company.text
        company_order = driver.find_element(By.XPATH, '//*[@id="fixTable"]/tbody/tr[{}]/td[2]/a'.format(i)).text
        company_id = driver.find_element(By.XPATH, '//*[@id="fixTable"]/tbody/tr[{}]/td[3]/a'.format(i)).text
        company_tsic = driver.find_element(By.XPATH, '//*[@id="fixTable"]/tbody/tr[{}]/td[7]/a'.format(i)).text
        company_tsic_typename = driver.find_element(By.XPATH, '//*[@id="fixTable"]/tbody/tr[{}]/td[8]/a'.format(i)).text
        
        # create return list for data
        return_list = [company_order, company_id, company_name, company_tsic, company_tsic_typename]

    except TimeoutException:
        driver.refresh()
        company_link, company_tsic, return_list = get_data_and_link_from_search_result(driver, i)

    return company_link, company_tsic, return_list

def get_data_from_company_page(driver, i):
    try:
        # store data from each company page
        company_current_objective  = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[4]'))).text
        company_tsic_at_registration = driver.find_element(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[3]/div[2]/div[1]/div/div[2]').text
        company_objective_at_registration = driver.find_element(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[3]/div[2]/div[1]/div/div[4]').text
        company_type = driver.find_element(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[2]').text
        company_registration_date = driver.find_element(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[6]').text
        company_registration_fund = driver.find_element(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[8]').text
        company_id_old = driver.find_element(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[10]').text
        company_business = driver.find_element(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[12]').text
        company_size = driver.find_element(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[14]').text
        list_company_years_with_submission = driver.find_elements(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[16]/span')
        company_years_with_submission = ', '.join([year.text for year in list_company_years_with_submission])
        company_location = driver.find_element(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[18]').text
        company_website = driver.find_element(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[20]').text
        list_company_directors = driver.find_elements(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[2]/div/div/ol/li')
        company_directors = ', '.join([year.text for year in list_company_directors])
        list_company_sign_directors = driver.find_elements(By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[3]/div[1]/div/p')
        company_sign_directors = ', '.join([year.text for year in list_company_sign_directors])

        # create return list for data
        return_list = [company_current_objective, company_tsic_at_registration, company_objective_at_registration, 
                                    company_type, company_registration_date, company_registration_fund, company_id_old, 
                                    company_business, company_size, company_years_with_submission, company_location, 
                                    company_website, company_directors, company_sign_directors]

    except TimeoutException:
        driver.refresh()
        return_list = get_data_from_company_page(driver, i)

    return return_list

# main website
url = "https://datawarehouse.dbd.go.th/index"

# list of column names
column_names = ['ลำดับ', 'เลขทะเบียนนิติบุคคล', 'ชื่อนิติบุคคล', 'TSIC_CODE', 'ประเภทธุรกิจ', 'วัตถุประสงค์', 'ประเภทธุรกิจตอนจดทะเบียน',
                'วัตถุประสงค์ตอนจดทะเบียน', 'ประเภทนิติบุคคล', 'วันที่จดทะเบียนจัดตั้ง', 'ทุนจดทะเบียน', 'เลขทะเบียนเดิม',
                 'กลุ่มธุรกิจ', 'ขนาดธุรกิจ', 'ปีที่ส่งงบการเงิน', 'ที่ตั้งสำนักงานใหญ่', 'Website', 'รายชื่อกรรมการ', 'กรรมการลงชื่อผูกพัน']
df = pd.DataFrame(columns = column_names)
not_empty_df = False

# set initial item number (refer to the last created file)
next_item = 1

# initialize Chrome driver
driver = initiate_chrome()

# close modal warning
mdw_close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btnWarning")))
mdw_close_button.click()

# find the search box
search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "key-word")))
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
time.sleep(1)
sorter = Select(driver.find_element(By.ID, "sortBy"))
sorter.select_by_value("submitObjCode")

# wait for the page to load and find the total page number
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fixTable"]/tbody/tr[1]')))
total_pages = int(driver.find_element(By.ID, "sTotalPage").text.replace(',', ''))

# calculate page number and item number from the next_item
page_number = (next_item // 10) + 1
item_number = next_item  % 10
initial_page = True
change_page(page_number)

# loop through the pages
while page_number <= total_pages:
    # wait for the list to be loaded
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fixTable"]/tbody/tr[1]')))
        time.sleep(5)

        # open each company page in new tab
        for i in range(1, 11):
            # skip items before the initial item
            if initial_page and i < item_number:
                continue
            
            # stop the condition above after finding the initial item
            initial_page = False

            # get data and link from search page
            company_link, company_tsic, data_from_search_result = get_data_and_link_from_search_result(driver, i)

            # open the new tab
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(company_link)
            time.sleep(1)

            # get data from company page
            data_from_company_page = get_data_from_company_page(driver, i)

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
        change_page(page_number)
    except:
        driver.refresh()

# make index start from 1
df.index += 1

# save file
df.to_csv('/Users/yoongsomporn.t/Desktop/Projects/Test_WebScraping/DBD_by_tsic/TSIC{}.csv'.format(df.iloc[-1, 3]))

# quit the driver
time.sleep(5)
driver.quit()