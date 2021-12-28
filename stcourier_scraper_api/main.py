import json
import uuid
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)

from stcourier_firefox_selenium import track








@app.route('/track/stcourier_scraper_api',methods = ['GET'])
def api():


    try:
        tracking_number = int(request.args.get('q'))
        print(f'q: {tracking_number}')



        if len(str(tracking_number)) == 11:
            print('Valid T num')
        else:
            return jsonify({'msg':'Please Enter Valid Tracking Number'}), 422
    

    except:
        return jsonify({'msg':'Please Enter Tracking Number'}), 422





    try:
        response=track(tracking_number)
        return jsonify(response), 200
    except:
        
        return jsonify({'msg':'NO Details Found'}), 422

if __name__ == '__main__':
	app.run(debug=True)
    



