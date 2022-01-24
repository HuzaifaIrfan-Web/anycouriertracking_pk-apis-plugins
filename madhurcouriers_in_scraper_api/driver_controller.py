import datetime
import time
import os


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options as FirefoxOptions


url='https://www.madhurcouriers.in/CNoteTracking'

selenium_hub_host_name = os.environ.get('HUB_URI','http://127.0.0.1:4444/wd/hub')
print(selenium_hub_host_name)


try:

    from .settings import use_firefox
except:
  
    from settings import use_firefox


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

time.sleep(5)


for i in range(0,1):

    print(datetime.datetime.now(), end=' ')



    # if use_firefox:
    #     print(f'madhurcouriers_in Setting Up Firefox Selenium Driver {i}')
    #     driver = webdriver.Firefox(options=firefox_opt)
    # else:
    #     print(f'madhurcouriers_in Setting Up Chrome Selenium Driver {i}')
    #     driver = webdriver.Chrome(options=chrome_opt)


    print(f'madhur Setting Up Chrome Selenium Driver {i}')
    
    driver = webdriver.Remote(
    command_executor=selenium_hub_host_name,
    desired_capabilities={
                "browserName": "chrome",
            })
    


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



    

