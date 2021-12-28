
from bs4 import BeautifulSoup



import os


import uuid

from stcourier_captcha_solver import captcha_solver
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options as FirefoxOptions




# selenium_hub_host_name = os.environ.get('HUB_URI','http://127.0.0.1:4444/wd/hub')
# print(selenium_hub_host_name)


# import urllib
# request_url = urllib.request.urlopen(host_name)
# print(request_url.read())

# time.sleep(5)


import datetime


drivers=[]


firefox_opt = FirefoxOptions()
firefox_opt.add_argument("--headless")
# firefox_opt.set_preference('permissions.default.stylesheet', 2)
# firefox_opt.set_preference('permissions.default.image', 2)
# firefox_opt.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')


from selenium.webdriver.chrome.options import Options
chrome_opt = Options()
chrome_opt.add_argument('--headless')
chrome_opt.add_argument('--no-sandbox')
chrome_opt.add_argument('--disable-dev-sh--usage')


url='http://www.erpstcourier.com/awb_tracking2.php?keyword='

for i in range(0,1):
    
    print(datetime.datetime.now(), end=' ')

    # print(f'Setting Up Firefox Selenium Driver {i}')
    # driver = webdriver.Firefox(options=firefox_opt)

    print(f'Setting Up Chrome Selenium Driver {i}')
    driver = webdriver.Chrome(options=chrome_opt)

    # driver = webdriver.Remote(
    # command_executor=selenium_hub_host_name,
    # desired_capabilities={
    #             "browserName": "firefox",
    #         })


    

    driver.get(url)
    drivers.append({'use':None,'driver':driver,'epoch':0})

    print(datetime.datetime.now(), end=' ')

    # print(f'Started Firefox Selenium Driver {i}')
    print(f'Started Chrome Selenium Driver {i}')






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
    time.sleep(3)

    try:

        warning_text=driver.find_element_by_xpath('//*[@class="alert text-center alert-warning"]')
        print(warning_text.text)
        return False

    except:
        print('Validation correct')
        return True



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
    # tracking_number_text=63346811006
    # url='http://www.erpstcourier.com/awb_tracking2.php?keyword='
    # url=url+str(tracking_number_text)
    

    req_id = uuid.uuid1().hex

    selecting=True
    while selecting:

        index,driver=select_driver(req_id)

        if drivers[index]['use']==req_id:
            selecting=False




    # driver.get(url)




    
    running=True
    while(running):

        if not drivers[index]['use']==req_id:
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
    drivers[index]['use'] =None
    
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


    Current_Status=DELIVERY_STATUS[0]
    Orgin_SRC=DELIVERY_STATUS[1]
    Destination=DELIVERY_STATUS[2]
    Consignment=DELIVERY_STATUS[3]
    Book_DateTime=DELIVERY_STATUS[4]
    Delivery_DateTime=DELIVERY_STATUS[5]

    DELIVERY_STATUS_obj={

    "Current_Status":Current_Status,
"Orgin_SRC":Orgin_SRC,
"Destination":Destination,
"Consignment":Consignment,
"Book_DateTime":Book_DateTime,
"Delivery_DateTime":Delivery_DateTime,

}



    track_history=soup.find("div", class_="white-box b-l")

    tracking_number=track_history.find_all("h4")[0].find("span").text



    track_histories_ul=track_history.find("ul", class_="tracking")
    track_histories_li=track_histories_ul.find_all("li")




    track_histories=[]

    for track_history_li in track_histories_li:
        date_time=track_history_li.find('div', class_="tracking-date")
        date=date_time.find('h5', class_="tracking-title").text
        timestr=date_time.find('p').text
        # print(date.text)
        # print(timestr.text)
        

        panel=track_history_li.find('div', class_="tracking-panel")
        
        tracking_title=panel.find('h4').text
        # print(tracking_title)

        span_el=panel.find('span').text
        # print(span_el)

        p_el=" ".join(panel.find('p').text.replace(span_el, "").split())
        # print(p_el)

        track_history={
            "date":date,
            "time":timestr,
            "tracking_title":tracking_title,
            "span":span_el,
            "p":p_el,
        }

        track_histories.append(track_history)



    return_obj={
        "tracking_number":tracking_number,
        "DELIVERY_STATUS":DELIVERY_STATUS_obj,
        "track_histories":track_histories
    }

    return return_obj

