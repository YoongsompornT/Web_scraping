import pandas as pd
import ScrapeJobth 

degree_code = '0026'   # from 0001 to 0042
page_number = 1
URL = f'https://www.jobth.com/searchresume2.php?ake={degree_code}&typejob=&gender=&degree=&city=&province=&typeexp=2&exp=&typemoney=3&money=&keyword=&page={page_number}'

search_page = ScrapeJobth.jobth_soup(URL)
search_page.get_total_pages('/html/body/center/div[3]/center/div[2]/div/font/font/b')
#posting_date = search_page.get_text_from_xpath('/html/body/center/div[3]/center/div[1]/div[2]/div[1]/div[4]')

column_names = ['gid', 'เพศ', 'สถานะ', 'สัญชาติ', 'ศาสนา', 'วันเกิด', 'อายุ', 'ส่วนสูง', 'น้ำหนัก', 'สถานะภาพทางการทหาร',
                'จังหวัดที่อยู่', 'เขตที่อยู่', 'การติดต่อที่สะดวก', 'สาขาวิชาชีพ', 'ลักษณะงานที่ต้องการ', 'ระดับเงินเดือนที่ต้องการ',
                'แก้ไขข้อมูลล่าสุด', 'เข้่าสู่ระบบล่าสุด', 'ตำแหน่งที่สนใจ', 'จบการศึกษา']
basic_df = pd.DataFrame(columns = column_names)
column_names = ['gid', 'ปีที่จบการศึกษา', 'ระดับการศึกษา', 'สถานศึกษา', 'วุฒิการศึกษา', 'สาขาวิชา', 'เกรดเฉลี่ย']
edu_df = pd.DataFrame(columns=column_names)
column_names = ['gid', 'ประสบการณ์การทำงาน', 'ปีที่เริ่มทำงาน', 'ปีสุดท้ายที่ทำงาน', 'ตำแหน่ง', 'บริษัท', 'ที่อยู่บริษัท', 'ลักษณะงานที่ทำ']
exp_df = pd.DataFrame(columns=column_names)

total_pages = search_page.total_pages
while page_number <= total_pages:
    URL = f'https://www.jobth.com/searchresume2.php?ake={degree_code}&typejob=&gender=&degree=&city=&province=&typeexp=2&exp=&typemoney=3&money=&keyword=&page={page_number}'
    search_page = ScrapeJobth.jobth_soup(URL)
    applicants = search_page.get_all_applicant_data()
    for applicant in applicants:
        basic_info, edu_info, exp_info = applicant
        basic_df.loc[len(basic_df)] = basic_info
        #basic_df = pd.concat([basic_df, pd.Series(basic_info)], axis=1)
        edu_df = pd.concat([edu_df, edu_info])
        exp_df = pd.concat([exp_df, exp_info])
    print(f'finished page {page_number}')
    page_number += 1

#final = pd.merge(basic_df, edu_df, on='gid')
#final = pd.merge(final, exp_df, on='gid')
basic_df.to_csv(f'/Users/yoongsomporn.t/Desktop/Projects/Test_WebScraping/Jobth_search/{degree_code}_basic.csv')
edu_df.to_csv(f'/Users/yoongsomporn.t/Desktop/Projects/Test_WebScraping/Jobth_search/{degree_code}_edu.csv')
exp_df.to_csv(f'/Users/yoongsomporn.t/Desktop/Projects/Test_WebScraping/Jobth_search/{degree_code}_exp.csv')

print('finished')
