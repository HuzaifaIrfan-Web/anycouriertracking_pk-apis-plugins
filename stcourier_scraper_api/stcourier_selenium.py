
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time


import uuid

try:
    from .stcourier_captcha_solver import captcha_solver
    from .Driver_Controller import Driver_Controller

except:
    from stcourier_captcha_solver import captcha_solver
    from Driver_Controller import Driver_Controller
    
driver_controller=Driver_Controller()


def return_captcha_image(driver):
    captcha_image=driver.find_element_by_xpath('//*[@id="captchaimg"]').screenshot_as_png
    while(len(captcha_image)< 200):
        len(captcha_image)
        captcha_image=driver.find_element_by_xpath('//*[@id="captchaimg"]').screenshot_as_png

    return captcha_image



def save_captcha_image(captcha_image):

    tmp_captchas_folder='tmp/captchas'

    if not os.path.exists(tmp_captchas_folder):
        os.makedirs(tmp_captchas_folder)
    captcha_file_name = str(uuid.uuid4())

    captcha_path=f'{tmp_captchas_folder}/{captcha_file_name}.png'

    with open(captcha_path, 'wb') as file:
        file.write(captcha_image)
    
    print(captcha_path)
    return captcha_path




def use_captcha_solution(driver, captcha_solution):
    # eleUserMessage = driver.find_element_by_id("track_no")
    eleUserMessage = driver.find_element(By.ID, "captcha_code")
    eleUserMessage.clear()
    eleUserMessage.send_keys(captcha_solution)


    # driver.find_element_by_id('btnload').click()
    driver.find_element(By.ID , "SEARCH").click()






def check_validation(driver):
    time.sleep(1)
    # driver.implicitly_wait(1000)

    try:

        warning_text=driver.find_element_by_xpath('//*[@class="alert text-center alert-warning"]')
        print(warning_text.text)
        return False

    except:
        print('stcourier Validation correct')
        return True



    


    
def track(tracking_number_text):
    # tracking_number_text=63346811006
    # url='http://www.erpstcourier.com/awb_tracking2.php?keyword='
    # url=url+str(tracking_number_text)
    

    req_id = uuid.uuid1().hex

    selecting=True
    while selecting:

        driver_index,driver=driver_controller.select_driver(req_id)

        if driver_controller.check_driver_use(driver_index,req_id):
            selecting=False




    # driver.get(url)




    
    running=True
    while(running):

        if not driver_controller.check_driver_use(driver_index,req_id):
            print(f'{req_id} driver {driver_index} not using.')
            return track(tracking_number_text)

        eleUserMessage = driver.find_element(By.ID, "keyword")
        eleUserMessage.clear()
        eleUserMessage.send_keys(tracking_number_text)


        captcha_image=return_captcha_image(driver)
        captcha_path=save_captcha_image(captcha_image)
        captcha_solution = captcha_solver(captcha_path)[1]
        print(captcha_solution)
        use_captcha_solution(driver,captcha_solution)
        running = not check_validation(driver)


    
    body = driver.find_element(By.TAG_NAME , "body")



    innerHtml=body.get_attribute('innerHTML')

    # driver.quit()

    driver_controller.release_driver(driver_index,req_id)

    soup = BeautifulSoup(innerHtml, 'html.parser')


    try:

        response=scrape_data(soup)
    
    except:
        raise Exception
        # return {'msg':'Not Found'}
    
    

    return response


    
def scrape_data(soup):


    DELIVERY_STATUS_el=soup.find("table")

    trs=DELIVERY_STATUS_el.find_all("tr")

    DELIVERY_STATUS=[]

    for tr in trs:
        tds=tr.find_all("td")
        # print(tds)
        # for td in tds:
        try:
            DELIVERY_STATUS.append(tds[1].text)
        except:
            pass

    try:
        Current_Status=DELIVERY_STATUS[0]
    except:
        Current_Status=''

    try:
        Orgin_SRC=DELIVERY_STATUS[1]
    except:
        Orgin_SRC=''

    try:
        Destination=DELIVERY_STATUS[2]
    except:
        Destination=''

    try:
        Consignment=DELIVERY_STATUS[3]
    except:
        Consignment=''

    try:
        Book_DateTime=DELIVERY_STATUS[4] 
    except:
        Book_DateTime=''

    try:
        Delivery_DateTime=DELIVERY_STATUS[5]
    except:
        Delivery_DateTime=''


    DELIVERY_STATUS_obj={

    "Current_Status":Current_Status,
"Orgin_SRC":Orgin_SRC,
"Destination":Destination,
"Consignment":Consignment,
"Book_DateTime":Book_DateTime,
"Delivery_DateTime":Delivery_DateTime,

}

    track_histories_li=[]

    try:

        track_history=soup.find("div", class_="white-box b-l")

        tracking_number=track_history.find_all("h4")[0].find("span").text



        track_histories_ul=track_history.find("ul", class_="tracking")
        track_histories_li=track_histories_ul.find_all("li")

    except:
        print('timeline not found')



    track_histories=[]

    for track_history_li in track_histories_li:
        

        try:
            date_time=track_history_li.find('div', class_="tracking-date")
            date=date_time.find('h5', class_="tracking-title").text

                    
        except:
            date=''  
        try:
            timestr=date_time.find('p').text

        except:
            timestr=''  
        # print(date.text)
        # print(timestr.text)
        
        try:
            panel=track_history_li.find('div', class_="tracking-panel")
        

            tracking_title=panel.find('h4').text
        # print(tracking_title)
        except:
            tracking_title=''     

        try:
            span_el=panel.find('span').text
        except:
            span_el=''
        # print(span_el)

        try:
            p_el=" ".join(panel.find('p').text.replace(span_el, "").split())
        # print(p_el)
        except:
            p_el=''

        track_history={
            "date":date,
            "time":timestr,
            "tracking_title":tracking_title,
            "span":span_el,
            "p":p_el,
        }

        track_histories.append(track_history)



    return_obj={
        "tnum":tracking_number,
        "status":DELIVERY_STATUS_obj,
        "track_histories":track_histories
    }

    return return_obj

