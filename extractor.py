from scrapy import Selector
import csv
import requests
from datetime import date
from os import path


def get_data(link: str):
    url = f'https://www.myfloridalicense.com/{link}'
    data = requests.get(url = url).text
    return data


def check_odd(var_list: list):
    return len(var_list) % 2 == 1


def break_list(var_list: list):
    sol = list()
    odd = check_odd(var_list)
    for i in range(0, len(var_list), 2):
        if odd and i==len(var_list)-1:
            sol.append([var_list[i]])
            continue
        sol.append([var_list[i], var_list[i+1]])
    return sol

class extract():
    def __init__ (self, html, county):
        self.html = html
        self.county = county
        self.status = None


    def extract_data(self):
        # fileToRead = open("ec.txt", "r")
        # html = fileToRead.read()
        sel = Selector( text = self.html )

        today = date.today()
        date_check = str(today)[-2:]

        last_check_date = sel.xpath("//em[contains(./text(), '%s')]/text()" % date_check).get()

        a = sel.xpath("//form[@name='reportForm']//tr[@height = '40']").getall()
        entries = break_list(a)

        # print('splitting the data')

        final_data = []
        csv_columns = ['County', 'License_type', 'Name', 'Name_type', 'License_no', 'Rank', 'Status', 'Expiring_date', 'Primary_name_DBA Name', 'Licensure_date', 'License Location Address', 'Main Address', 'Mailing Address', 'Last_check_date']

        count = 1
        for ent in entries:
            new_sel = Selector (text = ent[0])
            try: 
                row_1 = new_sel.xpath("//font[@face='Arial']//text()").getall()
                if 'Application' in row_1[-1]:
                    license_type = row_1[0]
                    name = row_1[1]
                    name_type = row_1[2]
                    license_no = ''
                    rank = row_1[-2]
                    status = row_1[-1]
                    expiring_date = ''
                elif 'Eligible for Exam' in row_1[-1]:
                    license_type = row_1[0]
                    name = row_1[1]
                    name_type = row_1[2]
                    license_no = ''
                    rank = ''
                    status = row_1[-1]
                    expiring_date = ''
                else:
                    license_type = row_1[0]
                    name = row_1[1]
                    name_type = row_1[2]
                    license_no = row_1[3]
                    rank = row_1[4]
                    status = row_1[5]
                    expiring_date = row_1[6]
            except Exception as e: 
                print(e)
                print(f'failed at no {count}')


            link = new_sel.xpath("//a/@href").get()
            link_html = get_data(link)
            link_sel = Selector( text = link_html )

            if name_type == 'DBA':
                primary_name = link_sel.xpath("//small[contains(./text(), 'Primary Name')]/parent::b//text()").get()
            else:
                try :
                    primary_name = link_sel.xpath("//small[contains(./text(), 'DBA Name')]/parent::b//text()").get()
                except :
                    primary_name = link_sel.xpath("//small[contains(./text(), 'Primary Name')]/parent::b//text()").get()

            licensure_date = link_sel.xpath("//font[contains(./text(), 'Licensure Date')]/parent::td/following-sibling::td//b/text()").get()


            new_sel = Selector (text = ent[1])
            row_2 = new_sel.xpath("//font[@face='Arial']//text()").getall()
            row_2 = [n.replace('\xa0', '').replace('*', '') for n in row_2]
            row_2 = [n for n in row_2 if n != '']
            
            p = break_list(row_2)
            temp_dict = dict()
            for item in p:
                temp_dict[item[0].replace(':','')] = item[1]
            # print(temp_dict)

            data = {
                'County': self.county,
                'License_type': license_type,
                'Name': name,
                'Name_type': name_type,
                'License_no': license_no,
                'Rank': rank,
                'Status': status,
                'Expiring_date': expiring_date,
                'Primary_name_DBA Name': primary_name,
                'Licensure_date': licensure_date,
                'Last_check_date': last_check_date
            }

            data.update(temp_dict)
            final_data.append(data)
            count += 1

        csv_file = "Electrical_contractor.csv"

        try:
            checkFile = path.exists(csv_file)
            with open(csv_file, 'a', newline='') as csvfiles:
                writer = csv.DictWriter(csvfiles, fieldnames=csv_columns)
                if not checkFile:
                    writer.writeheader()
                writer.writerows(final_data)
                self.status = '200'
            
            csvfiles.close()
        except IOError:
            print("I/O error")
            self.status = '400'

        return self.status