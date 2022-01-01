

import json
from flask import Flask, render_template, request, jsonify, redirect





 
app = Flask(__name__)



@app.route('/',methods = ['GET'])
def index():
    return render_template('index.html')


from madhurcouriers_in_scraper_api.app import madhurcouriers_in_track

from stcourier_scraper_api.app import stcourier_track


app.add_url_rule('/track/madhurcouriers_in_scraper_api', 'madhurcouriers_in_track', madhurcouriers_in_track)

app.add_url_rule('/track/stcourier_scraper_api', 'stcourier_track', stcourier_track)
 


if __name__ == '__main__':
	app.run(debug=True)