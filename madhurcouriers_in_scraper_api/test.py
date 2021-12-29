import grequests

import datetime
import json
urls = [
]

# host='server.skiie.com'
# host='0.0.0.0:5000'
host='localhost'


url=f'http://{host}/track/madhurcouriers_in_scraper_api?tnum=P501687103'



for i in range(0,2):

    urls.append(url)

start=datetime.datetime.now()

print(start)

rs = (grequests.get(u) for u in urls)




responses = grequests.map(rs)



for res in responses:
    # print(res.content)
    try:
        d = json.loads(res.content)
        print(d.keys())
        # print(d)
    except:
        print(res.content)
        print('json error')
    
end=datetime.datetime.now()
print(end-start)

