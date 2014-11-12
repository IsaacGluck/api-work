from flask import Flask, request, url_for, redirect, render_template
import json, urllib2

app=Flask(__name__)

@app.route("/", methods=["GET","POST"])
@app.route("/index", methods=["GET","POST"])
def index():
	if request.method=="GET":
		return render_template("index.html")
	else:
		latitude = request.form["latitude"]
		longitude = request.form["longitude"]
		if authenticate_location(latitude, longitude):
			info = location_lookup(latitude, longitude)
			person1 = info[0][0] + " " + info[0][1]
			person2 = info[0][2] + " " + info[0][3]
			person3 = info[0][4] + " " + info[0][5]

			hist1 = vote_history(info[1][0])
			hist2 = vote_history(info[1][1])
			hist3 = vote_history(info[1][2])

			senators = []
			representative = ""
			history = []
			if info[2][0] == "senate":
				senators.insert(0,person1)
				history.insert(0,hist1)
			else:
				representative = person1
				history.append(hist1)
			if info[2][1] == "senate":
				senators.insert(0,person2)
				history.insert(0,hist2)
			else:
				representative = person2
				history.append(hist2)
			if info[2][2] == "senate":
				senators.insert(0,person3)
				history.insert(0,hist3)
			else:
				representative = person3
				history.append(hist3)

			return render_template("custom.html", senators=senators, representative=representative, history=history)
		else:
			return render_template("index.html", message="Please enter a valid latitude and longitude.")

def vote_history(bioguide_id):
	url = 'http://congress.api.sunlightfoundation.com/votes?voter_ids.%s__exists=true&bill__exists=true&apikey=ee03d2ba64534625b16f2b58662bc6cb&fields=result,bill.short_title,bill.official_title,voters.%s,source'%(bioguide_id,bioguide_id)
	print url
	request = urllib2.urlopen(url)
	result = request.read()
	d = json.loads(result)
	past_votes = []
	for i in d['results']:
		# 0 - bill name, 1 - abbreviated name, 2 - result, 3 - source, 4 - vote, 5 - website
		past_votes.append([ str(i['bill']['official_title']), str(i['bill']['short_title']), str(i['result']), str(i['source']), str(i['voters'][bioguide_id]['vote']), str(i['voters'][bioguide_id]['voter']['website']) ])
	return past_votes


def location_lookup(latitude, longitude):
	url='http://congress.api.sunlightfoundation.com/legislators/locate?apikey=ee03d2ba64534625b16f2b58662bc6cb&latitude=%s&longitude=%s&fields=last_name,first_name,bioguide_id,chamber'%(latitude, longitude)
	request = urllib2.urlopen(url)
	result = request.read()
	d = json.loads(result)
	try:
		# f = first, l = last
		# 0 - (0 - fn, 1 - ln, 2 - fn, 3 - ln, 4 - fn, 5 - ln ) 1 - (0 - sbio_id, 1 - hbio_id, 0 - hbio_id) 2 - (1 - chamber, 2 - chamber, 3 - chamber)
		return [ [ d['results'][0]['first_name'], d['results'][0]['last_name'], d['results'][1]['first_name'], d['results'][1]['last_name'], d['results'][2]['first_name'], d['results'][2]['last_name'] ], [ d['results'][0]['bioguide_id'], d['results'][1]['bioguide_id'], d['results'][2]['bioguide_id'] ], [ d['results'][0]['chamber'], d['results'][1]['chamber'], d['results'][2]['chamber'] ] ]
	except IndexError:
		return None

def authenticate_location(lati, longi):
	try:
		latitude = float(lati)
		longitude = float(longi)
	except ValueError:
		return False
	if location_lookup(latitude, longitude) == None:
		return False
	if longitude < -66.95 or longitude > 172.450000 or latitude < 71.383333 or latitude > 18.916667:
		return True
	else:
		return False

if __name__=='__main__':
   app.debug=True
   app.run()
   #app.run(host='0.0.0.0',port=8000) ON NETWORK

# 40.798601, -73.971328