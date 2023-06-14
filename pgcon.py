import psycopg2
import pandas as pd

conn = psycopg2.connect(database="employee",
                        host="localhost",
                        user="postgres",
                        password="08420",
                        port="5432")



cur=conn.cursor()

data1=pd.read_csv('company_data.csv')
rows1=data1.shape[0]

data2=pd.read_csv('other_info_data.csv')
rows2=data2.shape[0]


for i in range(0,rows1):
    try:
            cur.execute('insert into company_data values(%s,%s,%s,%s,%s,%s,%s)',(data1['Company_ID'][i],data1['Company_Name'][i],data1['Sectors'][i],data1['Trading_Codes'][i],str(data1['Scrip_Codes'][i]),data1['Websites'][i],data1['Urls'][i]))
            conn.commit()
    except psycopg2.errors.UniqueViolation:
            # Handle duplicate row (e.g., log an error, skip, etc.)
            print()




for i in range(0,rows2):
    cur.execute('insert into other_info_data values(%s,%s,%s,%s,%s,%s,%s)',(data2['Company_ID'][i],data2['Date'][i],float(data2['Sponsor'][i]),float(data2['Govt'][i]),float(data2['Institute'][i]),float(data2['Foreign'][i]),float(data2['Public'][i])))

cur.execute('''
    DELETE FROM other_info_data
    WHERE Company_ID IN (
        SELECT Company_ID
        FROM (
            SELECT Company_ID, ROW_NUMBER() OVER (partition BY Company_ID, Date_,Sponsor,Govt,Institute,Foreign_,Public_ ORDER BY Company_ID) AS rownum
            FROM other_info_data
        ) t
        WHERE t.rownum > 1
    )
''')
conn.commit()


