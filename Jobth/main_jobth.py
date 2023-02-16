import json
import ScrapeJobth 

degree_code = '0026'   # from 0001 to 0042
page_number = 1
URL = f'https://www.jobth.com/searchresume2.php?ake={degree_code}&typejob=&gender=&degree=&city=&province=&typeexp=2&exp=&typemoney=3&money=&keyword=&page={page_number}'

search_page = ScrapeJobth.jobth_soup(URL)
search_page.get_total_pages('/html/body/center/div[3]/center/div[2]/div/font/font/b')
#posting_date = search_page.get_text_from_xpath('/html/body/center/div[3]/center/div[1]/div[2]/div[1]/div[4]')

basic_column_names = ['gid', 'เพศ', 'สถานะ', 'สัญชาติ', 'ศาสนา', 'วันเกิด', 'อายุ', 'ส่วนสูง', 'น้ำหนัก', 'สถานะภาพทางการทหาร',
                'จังหวัดที่อยู่', 'เขตที่อยู่', 'การติดต่อที่สะดวก', 'สาขาวิชาชีพ', 'ลักษณะงานที่ต้องการ', 'ระดับเงินเดือนที่ต้องการ',
                'แก้ไขข้อมูลล่าสุด', 'เข้่าสู่ระบบล่าสุด', 'ตำแหน่งที่สนใจ', 'จบการศึกษา']
edu_column_names = ['gid', 'ปีที่จบการศึกษา', 'ระดับการศึกษา', 'สถานศึกษา', 'วุฒิการศึกษา', 'สาขาวิชา', 'เกรดเฉลี่ย']
exp_column_names = ['gid', 'ประสบการณ์การทำงาน', 'ปีที่เริ่มทำงาน', 'ปีสุดท้ายที่ทำงาน', 'ตำแหน่ง', 'บริษัท', 'ที่อยู่บริษัท', 'ลักษณะงานที่ทำ']

edu_list = []
exp_list = []
JSONlist = []


total_pages = 5#search_page.total_pages
while page_number <= total_pages:
    URL = f'https://www.jobth.com/searchresume2.php?ake={degree_code}&typejob=&gender=&degree=&city=&province=&typeexp=2&exp=&typemoney=3&money=&keyword=&page={page_number}'
    search_page = ScrapeJobth.jobth_soup(URL)
    applicants = search_page.get_all_applicant_data()
    for applicant in applicants:
        basic_info, edu_info, exp_info = applicant
        output = dict(zip(basic_column_names, basic_info))
        for edu in edu_info:
            edu_list.append(dict(zip(edu_column_names, edu)))
        for exp in exp_info:
            exp_list.append(dict(zip(exp_column_names, exp)))
        #edu_list = dict(zip(edu_column_names, edu_info))
        #exp = dict(zip(exp_column_names, exp_info))
        output['การศึกษา']  = edu_list
        output['ประสบการณ์ทำงาน'] = exp_list
        edu_list = []
        exp_list = []

    JSONlist.append(output)
    print(f'finished page {page_number}')
    page_number += 1

with open('output.json', 'w', encoding ='utf8') as o:
    json.dump(JSONlist, o, ensure_ascii=False, indent=4)


print('finished')
#