import urllib
import urllib2
import json
import time


API_KEY = ""
API_SECRET = ""

text = ""

for number in numbers:
	number = "1" + number
	print number
	
	params = {
		'api_key': API_KEY,
		'api_secret': API_SECRET,
		'to': number,
		'from': '16202052698',
		'text': text
	}
	
	url = 'https://rest.nexmo.com/sms/json?' + urllib.urlencode(params)
	print url
	request = urllib2.Request(url)
	request.add_header('Accept', 'application/json')
	response = urllib2.urlopen(request)

	if response.code == 200 :
		data = response.read()
		#Decode JSON response from UTF-8
		decoded_response = json.loads(data.decode('utf-8'))
		# Check if your messages are succesful
		messages = decoded_response["messages"]
		print messages
		for message in messages:
			if message["status"] == "0":
				print "success"
	else :
		#Check the errors
		print "unexpected http {code} response from nexmo api". response.code
		print response.code
		
	time.sleep(5)

