# Robert Jones
# 9.13.22
# Tides program

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd


# begin_date = input('enter start date {yyyy,dd,mm}: ')
begin_date = '2022,01,01'
# end_date = input('enter end date {yyyy,dd,mm}: ')
end_date = '2024,01,01'

date_range = pd.date_range(begin_date,end_date,freq='MS').strftime('%Y%m%d').tolist()
print(date_range)


def get_data(URL):
    print(URL)
    driver = webdriver.Chrome(executable_path=r'C:\Users\Bob\Desktop\SpringBoard\chromedriver\chromedriver.exe')
    wait = WebDriverWait(driver,20)
    driver.get(URL)
    wait.until(EC.visibility_of_element_located((By.ID,'data_listing')))
    data = driver.find_elements(By.ID,'data_listing_table')

    table = []
    for ele in data:
        for col in ele.find_elements(By.TAG_NAME,'td'):
            table.append(col.text)

    return table   


def make_table():
    main_table = []
    for i in range(len(date_range)-1):
        URL = 'https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9413616&units=standard&bdate='+date_range[i]+'&edate='+date_range[i+1]+'&timezone=LST/LDT&clock=12hour&datum=MLLW&interval=hilo&action=data'
        main_table.append(get_data(URL))
    return main_table

def make_df(table):
    flat_list = [item for sublist in table for item in sublist]
    composite_table = [flat_list[x:x+5] for x in range(0,len(flat_list),5)]
    df = pd.DataFrame(composite_table,columns=['Date','DOTW','Time','Predicted(ft)','Hi_Low'])
    df.to_csv('C:/Users/Bob/Desktop/SpringBoard/Python_Projects/Tides/tide_df/tide_df.csv')


# Make Dataframe
# make_df(make_table())