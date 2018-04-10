import requests
import MySQLdb

term = {"Fall": "92", "Summer2": "76", "SummerOL": "51", "Summer10": "39",
        "Summer1": "25", "Spring": "14", "Winter": "03"}

c_dict = {"A": ['AC ENG', 'AFAM', 'ANATOMY', 'ANESTH', 'ANTHRO', 'ARABIC', 'ART', 'ART HIS', 'ART STU', 'ARTS', 'ARTSHUM', 'ASIANAM'],
          "B": ['BANA', 'BATS', 'BIO SCI', 'BIOCHEM', 'BME', 'BSEMD'],
          "C": ['CAMPREC', 'CBEMS', 'CEM', 'CHEM', 'CHINESE', 'CLASSIC', 'COGS', 'COM LIT', 'COMPSCI', 'CRITISM', 'CSE'],
          "D": ['DANCE', 'DERM', 'DEV BIO', 'DRAMA'],
          "E": ['E ASIAN', 'EARTHSS', 'ECO EVO', 'ECON', 'ED AFF', 'EDUC', 'EECS', 'EHS', 'ENGLISH', 'ENGR', 'ENGRCEE', 'ENGRMAE', 'ENGRMSE', 'EPIDEM', 'ER MED', 'EURO ST'],
          "F": ['FAM MED', 'FIN', 'FRENCH'],
          "G": ['GERMAN', 'GLBL ME', 'GLBLCLT', 'GREEK'],
          "H": ['HEBREW', 'HINDI', 'HISTORY', 'HUMAN', 'HUMARTS'],
          "I": ['I&C SCI', 'IN4MATX', 'INT MED', 'INTL ST', 'ITALIAN'],
          "JK":['JAPANSE', 'KOREAN'],
          "L": ['LATIN', 'LAW', 'LINGUIS', 'LIT JRN', 'LPS'],
          "M": ['MATH', 'MED', 'MED ED', 'MED HUM', 'MGMT', 'MGMT EP', 'MGMT FE', 'MGMT HC', 'MGMTMBA', 'MGMTPHD', 'MIC BIO', 'MOL BIO', 'MPAC', 'MUSIC'],
          "N": ['NET SYS', 'NEURBIO', 'NEUROL', 'NUR SCI'],
          "O": ['OB/GYN', 'OPHTHAL'],
          "P": ['PATH', 'PED GEN', 'PEDS', 'PERSIAN', 'PHARM', 'PHILOS', 'PHRMSCI', 'PHY SCI', 'PHYSICS', 'PHYSIO', 'PLASTIC', 'POL SCI', 'PORTUG', 'PSY BEH', 'PSYCH', 'PUB POL', 'PUBHLTH'],
          "R": ['RAD SCI', 'RADIO', 'REL STD', 'ROTC', 'RUSSIAN'],
          "S": ['SOC SCI', 'SOCECOL', 'SOCIOL', 'SPANISH', 'SPPS', 'STATS', 'SURGERY'],
          "T-Z": ['TAGALOG', 'TOX', 'UCDC', 'UNI AFF', 'UNI STU', 'VIETMSE', 'VIS STD', 'WOMN ST', 'WRITING']
          }

def get_info(data_form:dict):
    # send request to WebReg and get course info in text form
    url    = "https://www.reg.uci.edu/perl/WebSoc"
    header = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    while True:
        try:
            response = requests.post(url, data = data_form)
            break
        except: print("Order Invalid.")
    return response.text

def dept_format(dept:str):
    dept = dept.replace(' ', '')
    dept = dept.replace('&', '')
    dept = dept.replace('/', '')
    dept.lower()
    return dept

def add_row(info:list, cur):
    info[0] = dept_format(info[0])
    #print(info[0])
    cur.execute("REPLACE INTO {} (course_num, course_code, type, waitlist, status)\
                 VALUES ('{}', '{}', '{}', '{}', '{}')".format(info[0], info[1], info[2], info[3], info[4], info[5]))

def handle(raw_info:str, dept:str, cur):
    # grab [dept, course_num, course_code, type, waitlist, status]
    # from raw_info, then add each course to database
    raw_info_list = raw_info.split('\n')[20:]
    str_len = len(dept)
    for line in raw_info_list:
        if line == "": continue
        if line[0:str_len].upper() == dept:
            c_num = line[9:13]
            c_num = c_num.rstrip()
        else:
            if line[4:9] == "CCode":
                er_index = line.find("Enr") + 3
                wl_index = line.find("WL") + 2
                st_index = line.find("Status")
            elif line[4:9].isdigit():
                c_code   = line[4:9]
                type     = line[10:13]
                waitlist = line[er_index:wl_index]
                waitlist = waitlist.lstrip()
                status   = line[st_index:]
                status   = status.rstrip()
                add_row([dept, c_num, c_code, type, waitlist, status], cur)

def update_db(cur):
    year_term = "2018-" + term["Spring"]
    for i, j in c_dict.items():
        for dept in j:
            data_form = {"YearTerm": year_term,
                 "Dept": dept,
                 "CourseNum": "",
                 "CourseCodes": "",
                 "Submit": "Display Text Results"
                 }
            raw_info = get_info(data_form)
            handle(raw_info, dept, cur)


def search(dept, c_num, c_code):
    # search and update database
    
    data_form = {"YearTerm": "2018-" + term["Spring"],
                 "Dept": dept,
                 "CourseNum": course_num,
                 "CourseCodes": course_code,
                 "Submit": "Display Text Results"
                 }

    raw_info = get_info(data_form)
    handle(raw_info, dept, cur)

def init(cur):
    # initialize database by creating tables for all departments
    for i, j in c_dict.items():
        for dept in j:
            dept = dept_format(dept)
            cur.execute("CREATE TABLE IF NOT EXISTS {} (\
                course_num varchar(255),\
                course_code varchar(255),\
                type varchar(255),\
                waitlist varchar(255),\
                status varchar(255),\
                PRIMARY KEY(course_code))".format(dept))

def main():
    db = MySQLdb.connect(host = "localhost",
                         user = "root",
                         passwd = "b!fjdi829wAsd625",
                         db = "uci_course")
    cur = db.cursor()
    #init(cur)
    update_db(cur)
    db.commit()
    db.close()

if __name__ == "__main__":
    main()
