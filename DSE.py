import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import csv
import random
from itertools import count
import itertools
import schedule
import time

def datasets():


    page = requests.get("https://www.dsebd.org/company_listing.php")
    soup = BeautifulSoup(page.content, 'html.parser')
    codes1=[]
    # Finding trading codes
    trading = soup.find_all("div", {"class": "BodyContent"})
    codes=soup.find_all("a", {"class": "ab1"})
    for i in trading:
      code=i.find_all("a")
      for only_code in code:
        c=only_code.text.strip()
        codes1.append(c)

    element_to_remove = 'More...'
    trading_codes = [x for x in codes1 if x != element_to_remove]
    findex = trading_codes.index('TB10Y0126')
    lindex=trading_codes.index('TB5Y1225')
    start_index = findex
    end_index = lindex
    trading_codes = [x for i, x in enumerate(trading_codes) if i < start_index or i > end_index]
    # Generating unique IDs
    uid=[]
    counter = count(start=1)  # Start counting from after the last row of dataset
    counter2= count(start=1001)
    text = "DSE"
    for _ in range(len(trading_codes)):
      serial_number = next(counter)
      random_number = next(counter2)
      unique_id = f"{text}-{serial_number}-{random_number}"
      uid.append(unique_id)

    scrip_codes=[]
    urls=[]
    sectors=[]
    websites=[]
    oinfo=[]
    for i in range(0,len(trading_codes)):
        url=f'https://www.dsebd.org/displayCompany.php?name={trading_codes[i]}'
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        # Finding scrip code
        try:
            tag_value = soup.find("tr", {"class": "alt"})
            if tag_value is not None:
                scrip_code=tag_value.find_all('th')
                try:
                    scrip=scrip_code[1].text
                    sl=slice(11,17)
                    scrip_codes.append(scrip[sl])
                except TypeError:
                  print()
            else:
              print()
        except TypeError:
            print()
        #urls
        urls.append(url)
        #Finding Sectors
        try:
            tag_value = soup.find_all("div", {"class": "table-responsive"})
            if len(tag_value)>=2:
                tr=tag_value[2].find_all("tr", {"class": "alt"})
                if len(tr)>=1 :
                    td=tr[1].find_all("td")
                    sectors.append(td[1].text)
                else:
                  print()
            else:
                print()
        except TypeError:
            print()
        # Finding Websites
        try:
            tag_value2 = soup.find_all("div", {"class": "table-responsive"})
            if len(tag_value2)>=11:
                tr=tag_value2[11].find_all("tr")
                if len(tr)>=5:
                    td=tr[5].find_all("td")
                    a=td[1].find("a", {"class": "ab1"})
                    websites.append(a.text)
                else:
                  print()
            else:
                  print()
        except TypeError:
          print()
        #Finding Other Information
        try:
            tag_value3 = soup.find_all("div", {"class": "table-responsive"})
            tr=tag_value3[9].find_all("tr")
            sli=slice(54,66)
            #handling index error for null rows
            try:
              if(tr[3] in tr):
                tr1=tr[3].find_all("td")
                date=tr1[0].text
                float_numbers = re.findall(r'\d+\.\d+',tr1[1].text)
                sponsor,govt,institute,foreign,public=float_numbers
                oinfo.append([uid[i],date[sli],sponsor,govt,institute,foreign,public])
              if (tr[5] in tr):
                tr2=tr[5].find_all("td")
                date=tr2[0].text
                float_numbers = re.findall(r'\d+\.\d+',tr2[1].text)
                if len(float_numbers)==5:
                  sponsor,govt,institute,foreign,public=float_numbers
                  oinfo.append([uid[i],date[sli],sponsor,govt,institute,foreign,public])
              if (tr[7] in tr):
                tr3=tr[7].find_all("td")
                date=tr3[0].text
                float_numbers = re.findall(r'\d+\.\d+',tr3[1].text)
                if len(float_numbers)==5:
                  sponsor,govt,institute,foreign,public=float_numbers
                  oinfo.append([uid[i],date[sli],sponsor,govt,institute,foreign,public])
            except IndexError:
                print("")
        except TypeError:
          print()
    # Find all the company names
    company_name=[]
    page1 = requests.get("https://www.dsebd.org/company_listing.php")
    soup1 = BeautifulSoup(page1.content, 'html.parser')
    tradingx = soup1.find_all("div", {"class": "BodyContent"})
    comp=soup1.find_all("span")
    for i in tradingx:
      comp=i.find_all("span")
      for only_comp in comp:
        c=only_comp.text.strip()
        company_name.append(c)
    # removing the security company
    start_index = findex
    end_index = lindex
    company_name1 = [x for i, x in enumerate(company_name) if i < start_index or i > end_index]
    company_names=[]
    for i in company_name1:
        compname= re.findall(r'\((.*?)\)', i)
        company_names.append(compname)
    company_names = list(itertools.chain(*company_names))

    #convering datas into pandas dataframe and converting into csv file
    data = { 'Company_ID': uid,'Company_Name': company_names,'Sectors': sectors,'Trading_Codes':trading_codes,'Scrip_Codes':scrip_codes,'Websites':websites,'Urls':urls}
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()
    df.to_csv('company_data.csv', index=False)

    column_labels = ['Company_ID','Date','Sponsor', 'Govt','Institute','Foreign','Public']
    df2 = pd.DataFrame(oinfo,columns=column_labels)
    df2.to_csv('other_info_data.csv', index=False)
    


# Schedule the job to run every day at 10:00 AM Dhaka time
schedule.every().day.at("17:00").do(datasets)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)





