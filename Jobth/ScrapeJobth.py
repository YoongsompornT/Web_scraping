from bs4 import BeautifulSoup
from lxml import etree
import requests
import pandas as pd

class jobth_soup():
    def __init__(self, url):
        self.url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.etobj = etree.HTML(str(self.soup))
        self.total_pages = -1
        self.total_posts = -1

    def get_text_from_xpath(self, xpath):
        return self.etobj.xpath(xpath)[0].text

    def get_total_pages(self, xpath):
        self.total_posts = int(self.etobj.xpath(xpath)[0].text.replace(r',', ''))
        self.total_pages = self.total_posts // 10 + 1

    def get_applicant_soup(self, xpath):
        href = self.etobj.xpath(xpath)[0].get('href')
        id = href.partition("gid=")[2]
        url = f"https://www.jobth.com/%E0%B8%AB%E0%B8%B2%E0%B8%9E%E0%B8%99%E0%B8%B1%E0%B8%81%E0%B8%87%E0%B8%B2%E0%B8%99/{id}/?m=dtr&gid={id}"
        applicant = applicant_soup(url, id)
        return applicant
    
    def get_all_applicant_data(self):
        applicants_list = []
        posts = len(self.etobj.xpath('/html/body/center/div[3]/center/div[1]/div[2]/div'))
        for i in range(1, posts+1):
            applicant = self.get_applicant_soup(f'/html/body/center/div[3]/center/div[1]/div[2]/div[{i}]/div[5]/a[1]')
            basic_info = applicant.get_all_data()
            exp_info = applicant.get_all_block_data('/html/body/center/div[3]/center/div[3]/div/div[2]/div[3]/div[2]',1)
            edu_info = applicant.get_all_block_data('/html/body/center/div[3]/center/div[3]/div/div[2]/div[2]/div[2]',0)
            applicants_list.append([basic_info, edu_info, exp_info])
        return applicants_list

class applicant_soup():
    def __init__(self, url, id):
        self.url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.etobj = etree.HTML(str(self.soup))
        self.id = id
    
    def get_data(self, xpath, multitext=False):
        try:
            data = self.etobj.xpath(xpath)[0]
            data_text = list(data.itertext())
            #return data_text.partition("|")[0], data_text.partition("|")[2] # return label, data
            if multitext:
                return data_text
            return data_text[-1]
        except:
            return ""

    def get_block_data(self, xpath, type=0):
        return_list = []
        try:
            data = self.etobj.xpath(xpath)
            data_text = list(data[0].itertext())
            if not type:
                edu_level = data_text[2]
                uni = data_text[3]
                return_list.extend([edu_level, uni])
            else:
                start = data_text[0].partition("\xa0\xa0ถึง\xa0\xa0")[0]
                end = data_text[0].partition("\xa0\xa0ถึง\xa0\xa0")[2]
                return_list.extend([start, end])
                data = data[:4] + data[5:]
                
            for da in data[1:]:
                da_text = list(da.itertext())
                return_list.append(da_text[1])
        except:
            pass
            #raise Exception(f"Error at gid={self.id}")
        return return_list

    def get_all_block_data(self, xpath, type=0):
        xpath = xpath + '/div'
        return_list = []
        try:
            blocks = self.etobj.xpath(xpath)
            if not type:
                NotBlock_data = self.get_data(xpath + '[1]')
                #column_names = ['gid', 'ปีที่จบการศึกษา', 'ระดับการศึกษา', 'สถานศึกษา', 'วุฒิการศึกษา', 'สาขาวิชา', 'เกรดเฉลี่ย']
            else:
                NotBlock_data = self.get_data(xpath + '[1]')
                NotBlock_data = NotBlock_data[:NotBlock_data.find('ปี')-1]
                #column_names = ['gid', 'ประสบการณ์การทำงาน', 'ปีที่เริ่มทำงาน', 'ปีสุดท้ายที่ทำงาน', 'ตำแหน่ง', 'บริษัท', 'ที่อยู่บริษัท', 'ลักษณะงานที่ทำ']
            for i in range(2,len(blocks)+1):
                Block_data = self.get_block_data(xpath + f'[{i}]/div', type)
                data = [self.id] + [NotBlock_data] + Block_data
                return_list.append(data)
        except:
            pass
            #raise Exception(f"Error at gid={self.id}")
        return return_list

    def get_all_data(self):
        gender_status = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[1]/div[2]/div[2]')
        gender = gender_status[:gender_status.find('(')]
        marital_status = gender_status[gender_status.find('(')+1:gender_status.find(')')]
        
        nationality = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[1]/div[2]/div[3]')
        
        religion = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[1]/div[2]/div[4]')

        birth_age = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[1]/div[2]/div[5]')
        birth = birth_age[:birth_age.find('\xa0')]
        age = int((age_temp:=birth_age.partition('อายุ')[2])[1:age_temp.find('ปี')])
        
        height_weight = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[1]/div[2]/div[6]')
        try:
            height = float(height_weight[:height_weight.find('Cm')-1])
        except:
            height = '-'
        try:
            weight = float(height_weight[height_weight.find('ก')+1:height_weight.find('Kg')-1])
        except:
            weight = '-'

        military = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[1]/div[2]/div[7]')

        residence = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[2]/div[2]/div[2]', multitext=True)
        province = residence[-2]
        city_with_parenthesis = residence[-1]
        city = city_with_parenthesis[city_with_parenthesis.find('(')+1:city_with_parenthesis.find(')')]

        contact_method = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[2]/div[2]/div[6]')

        degree = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[3]/div[2]/div[1]')
        
        job_type = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[3]/div[2]/div[2]')

        salary = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[3]/div[2]/div[4]')

        last_edit = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[3]/div[2]/div[5]')
        last_login = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[1]/div[3]/div[2]/div[6]')

        job_title = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[2]/div[1]/div[2]/div')

        graduation_status = self.get_data('/html/body/center/div[3]/center/div[3]/div/div[2]/div[2]/div[2]/div[1]')

        return_list = [self.id, gender, marital_status, nationality, religion, birth, age, height, weight, military, province,
                    city, contact_method, degree, job_type, salary, last_edit, last_login, job_title, graduation_status]
        
        return return_list