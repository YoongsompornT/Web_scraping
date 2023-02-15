from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def driver_find_element_xpath(driver, xpath):
    try:
        result = driver.find_element(By.XPATH, xpath)
        return result.text
    except:
        result = "-"
        return result

def driver_find_elements_xpath(driver, xpath):
    try:
        results = driver.find_elements(By.XPATH, xpath)
        result = ', '.join([result.text for result in results])
        return result
    except:
        result = "-"
        return result

def initiate_chrome(url, headless = False):
    if headless:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('/Users/yoongsomporn.t/Desktop/Projects/Test_WebScraping/chromedriver', chrome_options = chrome_options)
    else:
        driver = webdriver.Chrome('/Users/yoongsomporn.t/Desktop/Projects/Test_WebScraping/chromedriver')
        
    driver.get(url)
    driver.maximize_window()
    
    return driver

def change_page(driver, page_number):
    current_page = driver.find_element(By.ID, 'cPage')
    current_page.clear()
    current_page.send_keys(page_number)
    current_page.send_keys(Keys.RETURN)

def wait_search_result_to_load(driver, page_number):
    try:    
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fixTable"]/tbody/tr[1]')))
    except  TimeoutException:
        print(f"refreshing at page {page_number} on {datetime.now()}")
        driver.refresh()
        wait_search_result_to_load(driver, page_number)

def get_data_and_link_from_search_result(driver, i, page_number):
    try:
        # get link for each company page
        company = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fixTable"]/tbody/tr[{}]/td[4]/a'.format(i))))
        company_link = company.get_attribute('href')
                
        # store data from search result page
        company_name = company.text
        company_order = driver_find_element_xpath(driver, '//*[@id="fixTable"]/tbody/tr[{}]/td[2]/a'.format(i))
        company_id = driver_find_element_xpath(driver, '//*[@id="fixTable"]/tbody/tr[{}]/td[3]/a'.format(i))
        company_tsic = driver_find_element_xpath(driver, '//*[@id="fixTable"]/tbody/tr[{}]/td[7]/a'.format(i))
        company_tsic_typename = driver_find_element_xpath(driver, '//*[@id="fixTable"]/tbody/tr[{}]/td[8]/a'.format(i))
        
        # create return list for data
        return_list = [company_order, company_id, company_name, company_tsic, company_tsic_typename]

    except TimeoutException:
        print(f"refreshing at page {page_number} on {datetime.now()}")
        driver.refresh()
        company_link, company_tsic, return_list = get_data_and_link_from_search_result(driver, i, page_number)

    return company_link, company_tsic, return_list

def get_data_from_company_page(driver, i, page_number):
    try:
        # store data from each company page
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div')))
        company_current_objective  = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[4]')
        company_tsic_at_registration = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[3]/div[2]/div[1]/div/div[2]')
        company_objective_at_registration = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[3]/div[2]/div[1]/div/div[4]')
        company_type = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[2]')
        company_registration_date = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[6]')
        company_registration_fund = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[8]')
        company_id_old = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[10]')
        company_business = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[12]')
        company_size = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[14]')
        company_years_with_submission = driver_find_elements_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[16]/span')
        company_location = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[18]')
        company_website = driver_find_element_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[1]/div/div/div/div[20]')
        company_directors = driver_find_elements_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[2]/div/div/ol/li')
        company_sign_directors = driver_find_elements_xpath(driver, '//*[@id="companyProfileTab1"]/div[2]/div[1]/div[3]/div[1]/div/p')

        # create return list for data
        return_list = [company_current_objective, company_tsic_at_registration, company_objective_at_registration, 
                                    company_type, company_registration_date, company_registration_fund, company_id_old, 
                                    company_business, company_size, company_years_with_submission, company_location, 
                                    company_website, company_directors, company_sign_directors]

    except TimeoutException:
        print(f"refreshing at page {page_number} on {datetime.now()}")
        driver.refresh()
        return_list = get_data_from_company_page(driver, i, page_number)

    return return_list
