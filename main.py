from requests import get, post
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

import re
import time

# Define color codes
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"

debug = True

def generate_return(status:int=0,output:str="",ref:dict={},error:str="") -> dict:
    return {
        "status":status,
        "output":output,
        "ref":ref,
        "error":error
    }

def get_execution_time(start):
    exeuction_time =  time.time() - start
    print(f"{BLUE}Total Execution Time: {RESET}{time.time() - start:.2f} s")

def terrorist_search(firstname:str,lastname:str) -> dict:
    if(debug):
        start_time = time.time()

    if(firstname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify firstname")
    
    if(lastname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify lastname")
    
    main_site = "https://aps.amlo.go.th"
    url =f"{main_site}/aps/public/dplth/search?un_name={firstname}+{lastname}"
    try:
        result = get(url)
        if(result.status_code != 200):
            if(debug):
                get_execution_time(start_time)
            return generate_return(-1,"",{},f"{url} return status {result.status_code}")
        
    except ConnectionError:
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},f"Unable to connect to {main_site}")

    result = BeautifulSoup(result.text,"html.parser").find("tbody").find("tr")
    if(result == None):
        if(debug):
            get_execution_time(start_time)
        return generate_return(0,f"{firstname+" "+lastname} is not found in Thai terrorist list.",{},"")
    
    source = result.find("a")["href"]

    # Handle document get request exception later
    document = get(source)
    document = BeautifulSoup(document.text,"html.parser").findAll("td")
    register_id = document[0].text.strip()
    birth_date = document[3].text.strip()
    address1 = document[6].text.strip()
    address2 = document[7].text.strip()

    ref = {
        "register_id":register_id,
        "birth_date":birth_date,
        "address1":address1,
        "address2":address2,
        "source":source
    }
    if(debug):
        get_execution_time(start_time)
    return generate_return(1,f"{firstname+" "+lastname} is found in Thailand terrorist database",ref,"")

def company_tax_register(firstname:str,lastname:str) -> dict:
    if(debug):
        start_time = time.time()

    if(firstname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify firstname")
    
    if(lastname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify lastname")
    
    main_site = "https://vsreg.rd.go.th"
    url = f"{main_site}/VATINFOWSWeb/jsp/VATInfoWSServlet"
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
    form_data = {
        "operation":"searchByFname",
        "goto_page":"",
        "tin":"on",
        "fname":firstname.encode("tis-620"),
        "lname":lastname.encode("tis-620")
    }


    try:
        result = post(url,data=form_data,headers=headers)
        if(result.status_code != 200):
            if(debug):
                get_execution_time(start_time)
            return generate_return(-1,"",{},f"{url} return status {result.status_code}")
        
    except ConnectionError:
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},f"Unable to connect to {main_site}")

    result = BeautifulSoup(result.text,"html.parser").find("tbody").find("tr", class_="text-center trMenu0")
    if(result == None):
        if(debug):
            get_execution_time(start_time)
        return generate_return(0,f"{firstname+" "+lastname} is not found in Thailand company registration list.",{},"")
    
    register_id = result.findAll("td")[1].text
    company_name = result.find('td', align='left')
    company_address = result.find('td', align='left', class_="table_wrap")
    
    if(company_name == None):
        company_name = ""
    
    else:
        company_name = company_name.text.split("/ ")[1]

    if(company_address == None):
        company_address = ""

    else:
        company_address = company_address.text.strip()

    ref = {
        "register_id":register_id,
        "address":company_name+" "+company_address,
        "source":url
    }
    if(debug):
        get_execution_time(start_time)

    return generate_return(1,f"{firstname+" "+lastname} is found in Thailand company registration list.",ref,"")

def teaching_certificate(firstname:str,lastname:str) -> dict:
    if(debug):
        start_time = time.time()
        size = 0

    if(firstname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify firstname")
    
    if(lastname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify lastname")
    
    main_site = "https://www.ksp.or.th"
    url = main_site + "/service/license_search_teach_ajax.php"
    try:
        result = post(url, stream=True)
        if(result.status_code != 200):
            if(debug):
                get_execution_time(start_time)
            return generate_return(-1,"",{},f"{url} return status {result.status_code}")
          
    except ConnectionError:
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},f"Unable to connect to {main_site}")
    
    found =  False
    for chunk in result.iter_content(chunk_size=1024):
        size += 1024
        soup = BeautifulSoup(chunk.decode("tis-620"), 'html.parser')
        soup = soup.findAll("tr")
        for tr in soup:
            tds = tr.findAll("td")
            for td in tds:
                if f"{firstname} {lastname}" in td.get_text():
                    found = True
                    break
                
            if(found):
                
                break
        if(found):
            break

    if(found):
        tds = tr.findAll("td")
        national_id = tds[0].text.strip()
        register_id = tds[2].text.strip()
        source = url
        ref = {
            "national_id":national_id,
            "register_id":register_id,
            "source":source
        }
        if(debug):
            get_execution_time(start_time)
            print(f"{BLUE}Total Chunk Usage:{RESET} {size/1024:.2f} KB")
        return generate_return(1,f"{firstname+" "+lastname} is found in teaching certification list.",ref,"")
        
    else:
        if(debug):
            get_execution_time(start_time)
            print(f"{BLUE}Total Chunk Usage:{RESET} {size/1024:.2f} KB")
        return generate_return(0,f"{firstname+" "+lastname} is not found in teaching certification list.",{},"")

def vet_search(firstname:str,lastname:str) -> dict:
    if(debug):
        start_time = time.time()

    if(firstname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify firstname")
    
    if(lastname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify lastname")
    
    main_site = "http://209.15.98.88"
    url = f"{main_site}/vet_member/search.member.service.php"
    # headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
    form_data1 = {
        "txtSearch":firstname,
        "btnSearch":"",
    }

    form_data2 = {
        "txtSearch":firstname,
        "btnSearch2":"",
    }

    try:
        result1 = post(url,data=form_data1)
        result2 =  post(url,data=form_data2)
        if(result1.status_code != 200):
            if(debug):
                get_execution_time(start_time)
            return generate_return(-1,"",{},f"{url} return status {result1.status_code}")
        if(result2.status_code != 200):
            if(debug):
                get_execution_time(start_time)
            return generate_return(-1,"",{},f"{url} return status {result2.status_code}")
        
    except ConnectionError:
        return generate_return(-1,"",{},f"Unable to connect to {main_site}")

    result1 = BeautifulSoup(result1.content.decode("utf-8"),"html.parser").findAll("span")
    result2 = BeautifulSoup(result2.content.decode("utf-8"),"html.parser").findAll("span")
    register_type = ""
    for span in result1:
        if(firstname in span.text and lastname in span.text):
            register_type = "vet-level1"

    for span in result2:
        if(firstname in span.text and lastname in span.text):
            register_type = "vet-level2"
    
    if(register_type != ""):
        ref = {
            "register_type":register_type
        }
        if(debug):
            get_execution_time(start_time)
        return generate_return(1,f"{firstname} {lastname} is found in vet database",ref,"")
    else:
        if(debug):
            get_execution_time(start_time)
        return generate_return(0,f"{firstname} {lastname} is not found in vet database",{},"")

def medic_search(firstname:str,lastname:str):
    if(debug):
        start_time = time.time()

    if(firstname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify firstname")
    
    if(lastname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify lastname")
    
    main_site = "https://checkmd.tmc.or.th"
    url = main_site

    form_data = {
        "checkCode":1,
        "nm":firstname,
        "lp":lastname
    }

    try:
        result = post(url, data=form_data)
        if(result.status_code != 200):
            if(debug):
                get_execution_time(start_time)
            return generate_return(-1,"",{},f"{url} return status {result.status_code}")
        
    except ConnectionError:
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},f"Unable to connect to {main_site}")
    
    result = BeautifulSoup(result.text, 'html.parser')
    result = result.findAll("article",class_="col-sm-9 col-md-9 col-lg-10")
    if(result == None or result == []):
        if(debug):
            get_execution_time(start_time)
        return generate_return(0,f"{firstname+" "+lastname} is not found in docter database.",{},"")
    else:
        certificate_date = result[0].find("span").text.strip()
        major = [i.text.strip() for i in result[0].findAll("li")]
        pattern = r'\((.*?)\)'
        major = [j[0].strip() for j in [re.findall(pattern, i) for i in major]]
        ref = {
            "certificate_date":certificate_date[-4:],
            "major":major,
            "source":url
        }
        if(debug):
            get_execution_time(start_time)
        return generate_return(1,f"{firstname} {lastname} is found in docter database",ref,"")
        
def seminar1(firstname:str,lastname:str) -> dict:
    if(debug):
        start_time = time.time()

    if(firstname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify firstname")
    
    if(lastname == ""):
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},"Please specify lastname")
    
    main_site = "https://www.dft.go.th/seminar-dft/th-th/name10092562"
    url = main_site

    try:
        result = get(url, verify=False)
        if(result.status_code != 200):
            if(debug):
                get_execution_time(start_time)
            return generate_return(-1,"",{},f"{url} return status {result.status_code}")
        
    except ConnectionError:
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},f"Unable to connect to {main_site}")
    
    result = BeautifulSoup(result.text,"html.parser").findAll("div",class_="col-md-3")
    result = "".join([i.text.strip().replace("\r","").replace("\t","").replace("\n\n","") for i in result])
    if(firstname in result and lastname in result):
        ref = {
            "seminar_topic":"หลีกภัยสงครามการค้า มุ่งหน้าอินเดียและเอเชียใต้",
            "seminar_date":"10 September 2019",
            "seminar_location":"หอประชุมศาสตราจารย์สังเวียน อินทรวิชัย ชั้น 7 อาคาร C ตลาดหลักทรัพย์แห่งประเทศไทย 93 ถ.รัชดาภิเษก แขวงดินแดง เขตดินแดง กรุงเทพฯ 10400",
            "source":url
        }
        if(debug):
            get_execution_time(start_time)
        return generate_return(1,f"{firstname+" "+lastname} is found in this seminar.",ref,"")
    else:
        if(debug):
            get_execution_time(start_time)
        return generate_return(0,f"{firstname+" "+lastname} is not found in this seminar.",{},"")

def construct_blacklist():
    # https://process3.gprocurement.go.th/BlackListWeb/jsp/control.blacklist
    # https://process3.gprocurement.go.th/BlackListWeb/jsp/BLK1300N.jsp
    # Try to scrap but fail, will try better techniques
    return

def dentist_search():
    # https://thaiortho.org/certified-orthodontist
    # Will finish later
    return

def buddist_search(firstname:str,lastname:str) -> dict:
    if(debug):
        start_time = time.time()
        count=0
    main_site = "https://www.gongtham.net/passlist/"
    try:
        result = get(main_site)
    except ConnectionAbortedError:
        if(debug):
            get_execution_time(start_time)
        return generate_return(-1,"",{},f"Unable to connect to {main_site}")
    
    result = BeautifulSoup(result.text,"html.parser").findAll("select")
    exam_years = result[0]
    level = result[1]
    exam_type = result[2]

    exam_years = [i.text for i in exam_years.findAll("option")]
    level = [i.text for i in level.findAll("option")]
    exam_type = [i.text for i in exam_type.findAll("option")]
    char_list = ['จ', 'ฉ', 'ห', 'อ', 'พ', 'ศ', 'ภ', 'ส', 'ร', 'ม', 'ก', 'ต', 'ย', 'ข', 'ช', 'บ', 'น', 'ป', 'ล']

    for year in exam_years:
        for class_ in level:
            for section in exam_type:
                for province in char_list:
                    url = main_site+f"?examyear={year}&class={class_}&section={section}&snr={province}&firstname={firstname}&lastname={lastname}"
                    result = get(url)
                    result = BeautifulSoup(result.text,"html.parser")
                    header = result.findAll("span")
                    header = [i.text for i in header]

                    if(debug):
                        count += 1
                        if(count % 200 == 0):
                            print(f"Current Search year: {year}, class: {class_}, section: {section}, province: {province} with total {count} requests")

                    if("เกิดข้อผิดพลาดในการสืบค้น" not in header):
                        result = result.find("tbody").findAll("td")
                        certificate_id = result[0].text.strip()
                        title = result[1].text.strip()
                        alias = result[3].text.strip()
                        temple = result[7].text.strip()
                        province = result[9].text.strip()
                        birth_year = result[5].text.strip()
                        ref = {
                            "certificate_id":certificate_id,
                            "title":title,
                            "alias":alias,
                            "temple_name":temple,
                            "temple_province":province,
                            "birth_year":birth_year,
                            "certificate_year":year,
                            "certificate_level":class_,
                            "certificate_type":section,
                            "source":url
                        }
                        if(debug):
                            print(f"{BLUE}Total Request: {RESET}{count} requests")
                            get_execution_time(start_time)
                        return generate_return(1,f"{firstname} {lastname} is found in monk database",ref,"")
    if(debug):
        print(f"{BLUE}Total Request: {RESET}{count} requests")
        get_execution_time(start_time)
    return generate_return(0,f"{firstname} {lastname} is not found in monk database",{},"")

# Test Case
# print(terrorist_search("อำรัน","มิง"))
# print(company_tax_register("เอก","กลิ่นขจร"))
# print(teaching_certificate("ไกรยศ","เพชราเวช"))
# print(vet_search("มนยา","เอกทัตร์"))
# print(medic_search("พรชนก","ถีระวงษ์"))
# print(seminar1("ทินกร","ทองขันธ์"))
# print(buddist_search("ดนัย","นาคช้อย"))