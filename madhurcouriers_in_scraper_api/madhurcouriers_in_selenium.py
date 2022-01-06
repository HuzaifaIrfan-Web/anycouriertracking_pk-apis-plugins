
from bs4 import BeautifulSoup



import os


import uuid

import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options as FirefoxOptions





url='https://www.madhurcouriers.in/CNoteTracking'

try:

    from .settings import use_firefox
except:
  
    from settings import use_firefox






import datetime


drivers=[]


firefox_opt = FirefoxOptions()
firefox_opt.add_argument("--headless")
firefox_opt.set_preference('permissions.default.stylesheet', 2)
firefox_opt.set_preference('permissions.default.image', 2)
firefox_opt.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')


from selenium.webdriver.chrome.options import Options
chrome_opt = Options()
chrome_opt.add_argument('--headless')
chrome_opt.add_argument('--no-sandbox')
chrome_opt.add_argument('--disable-dev-sh--usage')


for i in range(0,1):

    print(datetime.datetime.now(), end=' ')



    if use_firefox:
        print(f'madhurcouriers_in Setting Up Firefox Selenium Driver {i}')
        driver = webdriver.Firefox(options=firefox_opt)
    else:
        print(f'madhurcouriers_in Setting Up Chrome Selenium Driver {i}')
        driver = webdriver.Chrome(options=chrome_opt)


    driver.get(url)


    drivers.append({'use':None,'driver':driver,'epoch':0})

    print(datetime.datetime.now(), end=' ')

    if use_firefox:

        print(f'madhurcouriers_in Started Firefox Selenium Driver {i}')
    
    else:

        print(f'madhurcouriers_in Started Chrome Selenium Driver {i}')









def select_driver(req_id):

    selecting=True

    while selecting:

        for i,driver_obj in enumerate(drivers):
            
            if driver_obj['use'] ==None:

                driver_obj['use']=req_id

                epoch=int(datetime.datetime.now().timestamp())
                # print(epoch)
                driver_obj['epoch']=epoch

                driver=driver_obj['driver']
                index=i
                print(datetime.datetime.now(), end=f' {req_id} ')
                print(f'{i} Selenium Driver Selected')


                selecting=False
                break
            else:
                epoch=int(datetime.datetime.now().timestamp())
                # print(epoch)
                if (epoch > driver_obj['epoch'] +20):
                    print(datetime.datetime.now(), end=' ')
                    print(f'{i} Driver Use TimeOut')
                    driver_obj['use'] =None

    return index, driver



    


    
def track(tracking_number_text):


    req_id = uuid.uuid1().hex
    print(f'new reqid {req_id}')

    selecting=True
    while selecting:

        index,driver=select_driver(req_id)

        if drivers[index]['use']==req_id:
            selecting=False






    


    if not drivers[index]['use']==req_id:
        print(f'{req_id} driver {index} not using.')
        return track(tracking_number_text)




    old_url = str(driver.current_url)
    print(f'{req_id} Driver {index} Old URL {old_url}')


    
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
    print(f'{req_id} Driver {index} New URL {new_url}')


    if not(new_url == old_url):
        driver.get(url)

        print(f'{req_id} Driver {index} {new_url} not equal {old_url}')
            
        drivers[index]['use'] =None

        return track(tracking_number_text)

    # else:
    #     print(f'{req_id} Driver {index} {new_url} equal {old_url}')
            
    #     drivers[index]['use'] =None

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


 
    drivers[index]['use'] =None
    
    soup = BeautifulSoup(innerHtml, 'html.parser')
    print(f'{req_id} soup')

    with open('innerHtml.txt', 'w') as file:
        file.write(innerHtml)

    print(f'{req_id} saved soup')
    



    try:
        response=scrape_data(tracking_number_text,soup)
        print(f'{req_id} Driver {index} Got Response')
        return response
    
    except:
        print(f'{req_id} Driver {index} Got NO Response')
        raise Exception
        # return {'msg':'Not Found'}

    
    

    


    
def scrape_data(tracking_number_text,soup):

    trs=soup.find_all("tr")
    track_histories=[]

    for tr in trs:
        tds=tr.find_all("td")
    
        # for td in tds:
        try:

            # print(tds[0].text.strip())
            # print(tds[1].text.strip())
            # print(tds[2].text.strip())
            # print(tds[3].text.strip())
            # print(tds[4].text.strip())

            track_history=[tds[0].text.strip(),tds[1].text.strip(),tds[2].text.strip(),tds[3].text.strip(),tds[4].text.strip()]

            track_histories.append(track_history)


        except:
            print('no')
        # try:
        #     DELIVERY_STATUS.append(tds[1].text)
        # except:
        #     pass


    return_obj={'tnum':tracking_number_text,'track_histories':track_histories}

        


    return return_obj

