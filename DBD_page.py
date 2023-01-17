from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

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

def wait_search_result_to_load(driver):
    try:    
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fixTable"]/tbody/tr[1]')))
    except  TimeoutException:
        driver.refresh
        wait_search_result_to_load(driver)

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
