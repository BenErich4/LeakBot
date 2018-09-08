import gpsReader
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/_get_gps/', methods=['POST'])
def _get_gps():
	#get latitude/longitude from the read() function imported from gpsReader.py
	gpsData = gpsReader.read()
	
	#returns a json object (a kind of dictionary) with a key called 'data' with
	#a corresponding value that's a snippet of HTML code containing our gpsData
	#formatted by the template in response.html
	return jsonify({'data': render_template('response.html', gpsData=gpsData)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
