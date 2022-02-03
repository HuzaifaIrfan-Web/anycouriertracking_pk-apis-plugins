
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



    url='https://intelcom.ca/en/track-your-package/?tracking-id='

    url=url+str(tracking_number_text)

    # driver.implicitly_wait(1000)
    driver.get(url)
    time.sleep(2)




    
    body = driver.find_element(By.CLASS_NAME , "js-tracking-details")
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

    js_tracking_results=soup.find_all('div', attrs={'class': 'js-tracking-result'})

    if(js_tracking_results):
        print(True)
    else:
        raise Exception

    track_histories=[]

    for js_tracking_result in js_tracking_results:
        ps=js_tracking_result.find_all("p")

        try:
            track_title = ps[0].text.strip()
        except:
            track_title=''
            
        try:
            track_text = ps[1].text.strip()
        except:
            track_text=''

        try:
            datetime = ps[2].text.strip()
        except:
            datetime=''



        track_history={
            'track_title':track_title,
            'track_text':track_text,
            'datetime':datetime,
        }

        track_histories.append(track_history)




    return_obj={'tnum':tracking_number_text,'track_histories':track_histories}
            


    return return_obj

