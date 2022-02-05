
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

import time


import uuid



try:

    from .Driver_Controller import Driver_Controller

except:

    from Driver_Controller import Driver_Controller
    



driver_controller=Driver_Controller()





    
def track(tracking_number_text):


    req_id = uuid.uuid1().hex
    print(f'new reqid {req_id}')

    selecting=True
    while selecting:

        driver_index,driver=driver_controller.select_driver(req_id)

        if driver_controller.check_driver_use(driver_index,req_id):
            selecting=False






    


    if not driver_controller.check_driver_use(driver_index,req_id):
        print(f'{req_id} driver {driver_index} not using.')
        return track(tracking_number_text)




    old_url = str(driver.current_url)
    print(f'{req_id} Driver {driver_index} Old URL {old_url}')


    
    eleUserMessage = driver.find_element(By.ID, "ContentPlaceHolder1_txtCNote")
    eleUserMessage.clear()
    print(f'{req_id} clear textbox')
    eleUserMessage.send_keys(tracking_number_text)
    print(f'{req_id} input textbox')

    driver.find_element(By.ID , "ContentPlaceHolder1_btnSearch").click()
    print(f'{req_id} search click')

    # driver.implicitly_wait(1000)
    time.sleep(2)


    new_url = str(driver.current_url)
    print(f'{req_id} Driver {driver_index} New URL {new_url}')


    if not(new_url == old_url):
        
        driver_controller.refresh_driver(driver_index,req_id)

        print(f'{req_id} Driver {driver_index} {new_url} not equal {old_url}')
            
        driver_controller.release_driver(driver_index,req_id)

        return track(tracking_number_text)

    # else:
    #     print(f'{req_id} Driver {index} {new_url} equal {old_url}')
            
    #     drivers[index]['use'] =;

    #     return track(tracking_number_text)


        # eleUserMessage = driver.find_element(By.ID, "ContentPlaceHolder1_txtCNote")
        # eleUserMessage.clear()
        # eleUserMessage.send_keys(tracking_number_text)

        # driver.find_element(By.ID , "ContentPlaceHolder1_btnSearch").click()

        # # driver.implicitly_wait(1000)
        # time.sleep(2)







    
    body = driver.find_element(By.ID , "ContentPlaceHolder1_gvBookings")
    print(f'{req_id} find body')



    innerHtml=body.get_attribute('innerHTML')


 
    driver_controller.release_driver(driver_index,req_id)
    
    
    soup = BeautifulSoup(innerHtml, 'html.parser')
    # print(f'{req_id} soup')

    # with open('innerHtml.txt', 'w') as file:
    #     file.write(innerHtml)

    # print(f'{req_id} saved soup')
    



    try:
        response=scrape_data(tracking_number_text,soup)
        print(f'{req_id} Driver {driver_index} Got Response')
        return response
    
    except:
        print(f'{req_id} Driver {driver_index} Got NO Response')
        raise Exception
        # return {'msg':'Not Found'}

    
    

    


    
def scrape_data(tracking_number_text,soup):

    trs=soup.find_all("tr")
    track_histories=[]

    for tr in trs:
        tds=tr.find_all("td")
    
        # for td in tds:
    
        try:
            Sr_No = tds[0].text.strip()
        except:
            Sr_No=''

        try:
            Date = tds[1].text.strip()
        except:
            Date=''

        try:
            Transaction_Type = tds[2].text.strip()
        except:
            Transaction_Type=''
            continue

        try:
            Status = tds[3].text.strip()
        except:
            Status=''

        try:
            Remark = tds[4].text.strip()
        except:
            Remark=''

        track_history={
            'Sr_No':Sr_No,
            'Date':Date,
            'Transaction_Type':Transaction_Type,
            'Status':Status,
            'Remark':Remark
        }

        track_histories.append(track_history)





    return_obj={'tnum':tracking_number_text,'track_histories':track_histories}

        


    return return_obj

