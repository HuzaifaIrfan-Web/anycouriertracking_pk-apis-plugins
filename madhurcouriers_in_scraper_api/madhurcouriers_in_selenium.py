
from bs4 import BeautifulSoup



import os


import uuid



try:

    from .driver_controller import *

except:

    from driver_controller import *
    









    
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


 
    drivers[index]['use'] =None
    
    soup = BeautifulSoup(innerHtml, 'html.parser')
    # print(f'{req_id} soup')

    # with open('innerHtml.txt', 'w') as file:
    #     file.write(innerHtml)

    # print(f'{req_id} saved soup')
    



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

