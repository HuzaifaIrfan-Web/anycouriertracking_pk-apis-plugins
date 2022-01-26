import datetime
import time
import os


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.chrome.options import Options as ChromeOptions




selenium_hub_host_name = os.environ.get('HUB_URI','http://127.0.0.1:4444/wd/hub')
print(selenium_hub_host_name)


use_firefox=False

# import urllib
# request_url = urllib.request.urlopen(host_name)
# print(request_url.read())

# time.sleep(5)


import datetime




firefox_opt = FirefoxOptions()
firefox_opt.add_argument("--headless")
firefox_opt.set_preference('permissions.default.stylesheet', 2)
firefox_opt.set_preference('permissions.default.image', 2)
firefox_opt.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')


chrome_opt = ChromeOptions()
# chrome_opt.add_argument('--headless')
chrome_opt.add_argument('--no-sandbox')
chrome_opt.add_argument('--disable-dev-sh--usage')
# chrome_prefs = {}
# chrome_prefs["profile.default_content_settings"] = {"images": 2}
# chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
# chrome_opt.experimental_options["prefs"] = chrome_prefs


time.sleep(5)





class Driver_Controller():

    def __init__(self):

        self.drivers=[]

        self.url='http://www.erpstcourier.com/awb_tracking2.php?keyword='


        

        for i in range(0,1):

            print(datetime.datetime.now(), end=' ')



            # if use_firefox:
            #     print(f'madhurcouriers_in Setting Up Firefox Selenium Driver {i}')
            #     driver = webdriver.Firefox(options=firefox_opt)
            # else:
            #     print(f'madhurcouriers_in Setting Up Chrome Selenium Driver {i}')
            #     driver = webdriver.Chrome(options=chrome_opt)


            print(f'Setting Up Chrome Selenium Driver {i}')
            
            driver = webdriver.Remote(
            command_executor=selenium_hub_host_name,
            desired_capabilities={
                        "browserName": "chrome",
                    },options=chrome_opt)
            


            driver.get(self.url)

            refreshed=int(datetime.datetime.now().timestamp())


            self.drivers.append({'use':None,'driver':driver,'used':0, 'refreshed':refreshed})

            print(datetime.datetime.now(), end=' ')

            if use_firefox:

                print(f'Started Firefox Selenium Driver {i}')
            
            else:

                print(f'Started Chrome Selenium Driver {i}')









    def select_driver(self,req_id):

        selecting=True

        while selecting:

            for i,driver_obj in enumerate(self.drivers):
                
                if driver_obj['use'] ==None:

                    driver_obj['use']=req_id

                    used=int(datetime.datetime.now().timestamp())
                    # print(epoch)
                    driver_obj['used']=used

                    driver=driver_obj['driver']
                    driver_index=i
                    print(datetime.datetime.now(), end=f' {req_id} ')
                    print(f'{i} Selenium Driver Selected')


                    # refreshed=int(datetime.datetime.now().timestamp())
                    # print(epoch)
                    # if (refreshed > driver_obj['refreshed'] +3600 ):
                    #     print(datetime.datetime.now(), end=' ')
                    #     print('hour passed refreshing')
                    #     self.refresh_driver(driver_index,req_id)

                    # self.refresh_driver(driver_index,req_id)
                        


                    selecting=False
                    break
                else:
                    used=int(datetime.datetime.now().timestamp())
                    # print(epoch)
                    if (used > driver_obj['used'] + 45 ):
                        print(datetime.datetime.now(), end=' ')
                        print(f'{i} Driver Use TimeOut 45 secs')
                        driver_obj['use'] =None

        return driver_index, driver



        


    def check_driver_use(self,driver_index,req_id):
        if self.drivers[driver_index]['use'] == req_id:
            return True
        else:
            return False


    def release_driver(self,driver_index,req_id):
        if self.check_driver_use(driver_index,req_id):
            self.drivers[driver_index]['use'] =None
            print(f'{driver_index} Driver released by {req_id}')

    

    def refresh_driver(self,driver_index,req_id):
        if self.check_driver_use(driver_index,req_id):
            print(f'{driver_index} Driver refreshing by {req_id}')
            self.drivers[driver_index]['driver'].get(self.url)
            refreshed=int(datetime.datetime.now().timestamp())
            self.drivers[driver_index]['refreshed']=refreshed

            time.sleep(5)
    
    
