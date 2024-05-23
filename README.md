# Thailand Open Source Intelligent Integration
รวบรวมแหล่งสืบค้นข้อมูลบุคคลจากหลายๆ เว็ปไซต์สาธารณะในประเทศไทยด้วยเทคนิค `Web Scraping` โดยแหล่งข้อมูลที่ทำการเชื่อมได้แก่
- [สำนักงานป้องกันและปราบปามการฟอกเงิน](https://aps.amlo.go.th) (terrorist_search)
- [กรมสรรพากร](https://vsreg.rd.go.th) (company_tax_register)
- [คุรุสภา](https://www.ksp.or.th) (teaching_certificate)
- [สภาสัตวแพทย์](http://209.15.98.88) (vet_search)
- [แพทยสภา](https://checkmd.tmc.or.th/) (medic_search)
- [กรมการค้าต่างประเทศ](https://www.dft.go.th/seminar-dft/th-th/name10092562) (seminar1)
- [สำนักงานแม่กองธรรมสนามหลวง](https://www.gongtham.net/passlist/) (buddist_search)

## [Requirements](requirements.txt)
- Test on `Python 3.12.3`
- beautifulsoup4==4.12.3
- requests==2.32.2

## Global Variable
### Color
- RED : Change print outpu color to red
- GREEN : Change print output color to green
- BLUE : Change print output color to blue
- RESET : Change print output color to default

Usage
```python
print(f"{BLUE}Total Execution time: {RESET}1.00 s")
```

- debug : Show more details of execution such as execution time

## terrorist_search()
ค้นหารายชื่อบุคคลที่ถูกกำหนดตามมาตรา 7 (ก่อการร้ายหรือฟอกเงิน)
### Parameters
- string firstname: required
- string lastname: required

Usage
```python
print(terrorist_search("อำรัน","มิง"))
```

### Successful Return
```python
{
    status_code:int
    output_message:str
    ref:{
        register_id:str ; หมายเลขทะเบียน
        birth_date:str ; ปีเกิด
        address1:str ; ที่อยู่ 1
        address2:str ; ที่อยู่ 2
        source:str ; แหล่งอ้างอิง
    }
    error:str ; error message
}
```

### Bug Note
- เป็นการค้นหาแบบ `contains` ไม่ใช่ match หากพิมพ์ชื่อหรือนามสกุลไม่สมบูรณ์อาจจะเจอเช่นกัน

## company_tax_register()
ค้นหาข้อมูลผู้ประกอบการจดทะเบียนภาษีมูลค่าเพิ่ม ซึ่งยังคงประกอบกิจการอยู่
### Parameters
- string firstname: required
- string lastname: required

Usage
```python
print(company_tax_register("เอก","กลิ่นขจร"))
```

### Successful Return
```python
{
    status_code:int
    output_message:str
    ref:{
        register_id:str ; หมายเลขทะเบียน
        address:str ; ที่อยู่บริษัท
        source:str ; แหล่งอ้างอิง
    }
    error:str ; error message
}
```

## teaching_certificate()
ตรวจสอบใบอณุญาตการสอนของ`ครู`จากคุรุสภา
### Parameters
- string firstname: required
- string lastname: required

Usage
```python
print(teaching_certificate("ไกรยศ","เพชราเวช"))
```

### Successful Return
```python
{
    status_code:int
    output_message:str
    ref:{
        register_id:str ; หมายเลขทะเบียน
        address:str ; ที่อยู่บริษัท
        source:str ; แหล่งอ้างอิง
    }
    error:str ; error message
}
```

### Bug Note
- เนื่องจากเป็นการดึงตรงจาก source ที่เป็นตารางใหญ่ที่มีขนาดกว่า 20 MB อาจกิน memory ได้ (ทำการ implement requests แบบ stream)

## vet_search()
ตรวจสอบรายชื่อสัตวแพทย์จากสัตวแพทยสภา
### Parameters
- string firstname: required
- string lastname: required

Usage
```python
print(vet_search("มนยา","เอกทัตร์"))
```

### Successful Return
```python
{
    status_code:int
    output_message:str
    ref:{
        register_type:str ; ระดับของสัตวแพทย์
        source:str ; แหล่งอ้างอิง
    }
    error:str ; error message
}

```
### Bug Note
- เนื่องจากการตรวจสอบสัตวแพทย์ชั้น 1 และ ชั้น 2 เป็น request แยกกันจึงมีการ request 2 ครั้ง หากอันใดอันนึงล่มก็เกิดปัญหา (ยังไม่ได้เพิ่มวิธีแก้ไข)

## medic_search()
ตรวจสอบรายชื่อแพทย์จากแพทยสภา
### Parameters
- string firstname: required
- string lastname: required

Usage
```python
print(medic_search("พรชนก","ถีระวงษ์"))
```

### Successful Return
```python
{
    status_code:int
    output_message:str
    ref:{
        certificate_date:str ; ปีที่ออกใบอณุญาต
        major:list(str) ; ความถนัด
        source:str ; แหล่งอ้างอิง
    }
    error:str ; error message
}
```
## seminar1()
รายชื่อผู้ลงทะเบียนเข้าร่วมสัมมนา เรื่อง `หลีกภัยสงครามการค้า มุ่งหน้าอินเดียและเอเชียใต้` ของกระทรวงการต่างประเทศ
### Parameters
- string firstname: required
- string lastname: required

Usage
```python
print(seminar1("ทินกร","ทองขันธ์"))
```

### Successful Return
```python
{
    status_code:int
    output_message:str
    ref:{
        seminar_topic:str ; หัวข้อสัมนา
        seminar_date:str ; วันที่จัดสัมนา
        seminar_location:str ; สถานที่สัมนา
        source:str ; แหล่งอ้างอิง
    }
    error:str ; error message
}
```

## buddist_search()
ตรวจสอบรายชื่อผู้ที่รับการสอบนักธรรม
### Parameters
- string firstname: required
- string lastname: required

Usage
```python
print(buddist_search("ดนัย","นาคช้อย"))
```

### Successful Return
```python
{
    status_code:int
    output_message:str
    ref:{
        certificate_id:str ; หมายเลขใบประกาศ
        title:str ; คำนำหน้า
        alias:str ; ฉายา
        temple_name:str ; สังกัดวัด
        templte_provice:str ; จังหวัดที่สังกัด
        certificate_year:str ; ปีที่สอบ
        certificate_level:str ; ระดับนักธรรม
        certificate_type:str ; นิกาย
    }
    error:str ; error message
}
```
### Bug Note
- เนื่องจากปลายทางบังคับให้ใส่ทุก Parameter บวกกับ for loop หลายๆ ชั้น อาจทำให้โปรแกรมช้า และต้องส่ง requests มากกว่า 100 ครั้ง (ยังไม่ได้แก้ไข)

## construct_blacklist()
รายชื่อผู้ทิ้งการจ้างงาน
- https://process3.gprocurement.go.th/BlackListWeb/jsp/control.blacklist
- https://process3.gprocurement.go.th/BlackListWeb/jsp/BLK1300N.jsp
- ยังไม่ได้ทำการ Implement
- ยังไม่เข้าใจกระบวนการตรวจสอบ request ทางฝั่ง server

## dentist_search()
- https://thaiortho.org/certified-orthodontist
- ยังไม่ได้ทำการ Implement