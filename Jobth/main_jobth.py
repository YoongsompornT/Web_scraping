import json
import ScrapeJobth 

degree_code = '0028'   # from 0001 to 0042
page_number = 1
URL = f'https://www.jobth.com/searchresume2.php?ake={degree_code}&typejob=&gender=&degree=&city=&province=&typeexp=2&exp=&typemoney=3&money=&keyword=&page={page_number}'

search_page = ScrapeJobth.jobth_soup(URL)
search_page.get_total_pages('/html/body/center/div[3]/center/div[2]/div/font/font/b')
#posting_date = search_page.get_text_from_xpath('/html/body/center/div[3]/center/div[1]/div[2]/div[1]/div[4]')

#basic_column_names = ['gid', 'เพศ', 'สถานะ', 'สัญชาติ', 'ศาสนา', 'วันเกิด', 'อายุ', 'ส่วนสูง', 'น้ำหนัก', 'สถานะภาพทางการทหาร',
#                'จังหวัดที่อยู่', 'เขตที่อยู่', 'การติดต่อที่สะดวก', 'สาขาวิชาชีพ', 'ลักษณะงานที่ต้องการ', 'ระดับเงินเดือนที่ต้องการ',
#                'แก้ไขข้อมูลล่าสุด', 'เข้่าสู่ระบบล่าสุด', 'ตำแหน่งที่สนใจ', 'จบการศึกษา']
basic_column_names_en = ['gid', 'gender', 'status', 'nationality', 'religion', 'birthdate', 'age', 'height', 'weight', 'military_status',
                'province', 'district', 'contact', 'expertise_field', 'desired_jobtype', 'desired_salary',
                'last_edit', 'last_login', 'desired_position', 'graduated_year', 'speak_thai', 'read_thai', 'write_thai', 'typing_thai',
                'speak_eng', 'read_eng', 'write_eng', 'typing_eng', 'driving', 'vehicle', 'others', 'projects', 'exp_years']

#edu_column_names = ['ระดับการศึกษา', 'สถานศึกษา', 'วุฒิการศึกษา', 'สาขาวิชา', 'เกรดเฉลี่ย']
edu_column_names_en = ['education_level', 'university', 'degree', 'field', 'gpa']

#exp_column_names = ['เวลาที่เริ่มทำงาน', 'เวลาที่จบงาน', 'ตำแหน่ง', 'บริษัท', 'ที่อยู่บริษัท', 'ลักษณะงานที่ทำ']
exp_column_names_en = ['exp_start', 'exp_end', 'position', 'company', 'location', 'description']

#trn_column_names = ['ปีที่เริ่มการอบรม', 'เวลาที่จบการอบรม', 'สถาบัน', 'หลักสูตร']
trn_column_names_en = ['trn_start', 'trn_end', 'institute', 'program']

edu_list = []
exp_list = []
trn_list = []
JSONlist = []


total_pages = search_page.total_pages
while page_number <= total_pages:
    URL = f'https://www.jobth.com/searchresume2.php?ake={degree_code}&typejob=&gender=&degree=&city=&province=&typeexp=2&exp=&typemoney=3&money=&keyword=&page={page_number}'
    search_page = ScrapeJobth.jobth_soup(URL)
    applicants = search_page.get_all_applicant_data()
    for applicant in applicants:
        basic_info, edu_info, exp_info, trn_info = applicant
        output = dict(zip(basic_column_names_en, basic_info))
        for edu in edu_info:
            edu_list.append(dict(zip(edu_column_names_en, edu)))
        for exp in exp_info:
            exp_list.append(dict(zip(exp_column_names_en, exp)))
        for trn in trn_info:
            trn_list.append(dict(zip(trn_column_names_en, trn)))
        #edu_list = dict(zip(edu_column_names, edu_info))
        #exp = dict(zip(exp_column_names, exp_info))
        output['education']  = edu_list
        output['experience'] = exp_list
        output['training'] = trn_list
        edu_list = []
        exp_list = []
        trn_list = []
        JSONlist.append(output)

    print(f'finished page {page_number}')
    page_number += 1

with open(f'output_{degree_code}.json', 'w', encoding ='utf8') as o:
    json.dump(JSONlist, o, ensure_ascii=False, indent=4)

print(len(JSONlist))
print('finished')
#