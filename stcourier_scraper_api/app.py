# from typing import Optional

# from fastapi import FastAPI, HTTPException

# # from stcourier_chrome_selenium import track

# from .stcourier_firefox_selenium import track as return_details
 
# try:
#     from .stcourier_firefox_selenium import track as return_details
# except:
#     from stcourier_firefox_selenium import track as return_details

try:
    from .stcourier_chrome_selenium import track as return_details
except:
    from stcourier_chrome_selenium import track as return_details
 

# app = FastAPI()


# # @app.get("/")
# # def read_root():
# #     return {"Hello": "World"}


# # @app.get("/items/{item_id}")
# # def read_item(item_id: int, q: Optional[str] = None):
# #     return {"item_id": item_id, "q": q}

# @app.get("/track/stcourier_scraper_api")
# def track_query(tnum: Optional[str] = None):

#     try:
#         tracking_number=int(tnum)
#         print(tracking_number)
#         if len(str(tracking_number)) == 11:
#             print('Valid Tnum')
#         else:
#             raise HTTPException(status_code=404, detail="Please Enter valid Tracking Number")
#             # return {'msg':'Please Enter valid Tracking Number'}

#     except:
#         raise HTTPException(status_code=404, detail="Please Enter valid Tracking Number")
#         # return {'msg':'Please Enter valid Tracking Number'}


#     try:
#         response=track(tracking_number)
#     except:
        
#         raise HTTPException(status_code=404, detail="Not Found")
#         # response={'msg':'Internal Server Error'}


#     return  response




import json
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)





# @app.route('/docs',methods = ['GET'])
# def index():
#     return render_template('index.html')



@app.route('/track/stcourier_scraper_api',methods = ['GET'])
def stcourier_track():

    # tnum=int(tnum_str)

    try:

        tnum = request.args.get('tnum')
        print(f'stcourier tnum: {tnum}')

    except:
        
        return jsonify({'tnum':tnum, 'message':'Invalid Tracking Number'}), 422


    if not tnum:
        return jsonify({'tnum':tnum, 'message':'Invalid Tracking Number'}), 422



    if not (len(str(tnum)) == 11):
        return jsonify({'tnum':tnum, 'message':'Invalid Tracking Number'}), 422



    tracking_details=return_details(tnum)

    # try:
    #     # tracking_details=return_details(tnum)
    # except:
    #     return jsonify({'tnum':tnum, 'message':'Tracking Details Not Found'}), 404

    return jsonify(tracking_details), 200

if __name__ == '__main__':
	app.run(debug=True)