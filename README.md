# Dhaka-Stock-Exchange-data-visualization
This project is a web scraping task that scraps data from the DSE (Dhaka Stock Exchange) website using the BeautifulSoup library. In CSV files, it stores trading data and other information about listed companies that it has retrieved.
# Requirements
Using beautiful soup, scrape data from the DSE website:
- Scrap the data from https://dsebd.org/company_listing.php
- Page with a list of companies: https://dsebd.org/displayCompany.php?name=(trading_code)
- Scrap data using html tag,classes from browse devtool. 
- Create unique id for each row
- Details needed for scraping and cleaning
- Company name, Trading code, Scrip code, and Additional Company Information (Monthly),urls,websites
- To get the most recent data, run the script every day at 5:00 PM using scheduler
- Store information in a PostgreSQL database.
# Steps for implementation
- Run the `DSE.py` script to initiate the data scraping process
- The script will connect to the DSE website and retrieve `trading_codes` for listed companies.
- The trading codes will be extracted and cleaned to remove `security codes`.
- Additional information such as `scrip codes, URLs, company names, sectors, and websites` will also be extracted.
- The extracted data will be cleaned and processed.
- `Unique IDs` will be generated for each company name.
- From the other information table data about `sponsors/directors, institutes, public, govt, and foreign` data will be extracted.
- The data will be saved in two CSV files: `company_data.csv` and `other_info_data.csv`.
- The data will be inserted to the postgres database using psycopg2
- After insertion duplicate rows will be removed from the other_info_data table  


# Power BI Dash Board

![dse1](https://github.com/sobhanifahim/Dhaka-Stock-Exchange-data-visualization/assets/57230287/93cb6867-dcda-415c-8dba-00e1ababc799)

![dse2](https://github.com/sobhanifahim/Dhaka-Stock-Exchange-data-visualization/assets/57230287/b0f1ee55-5a2e-4658-94b4-4bf37b1a7926)
