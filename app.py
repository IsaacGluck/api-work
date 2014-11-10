from flask import Flask, request, url_for, redirect, render_template
import json, urllib2

app=Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('lookup'))

@app.route('/lookup')
@app.route('/lookup/<ip>')
def lookup(ip='46.19.37.108'):
	url = 'http://www.telize.com/geoip/%s'
	url = url%(ip)
	request = urllib2.urlopen(url)
	result = request.read()
	d = json.loads(result)
	page = ''
	for r in d.keys():
		print d[r]
		page += '<p>' + r + ": " + str(d[r]) + '</p>'
	return page


if __name__=='__main__':
   app.debug=True
   app.run()
   #app.run(host='0.0.0.0',port=8000) ON NETWORK