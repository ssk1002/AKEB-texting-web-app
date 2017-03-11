import urllib
import urllib2
import json
import time
from secret import *

print API_KEY
print API_SECRET
print FROM_NUMBER

def sendText(number, text):
	'''This function sends out a single text message to the provided number as a string it also 
	checks if the number starts with 1 since this is planned to be used primarly in the US.'''
	if number[0] != '1': #check for starting with 1
		number = "1" + number #if not add 1
	
	params = {
		'api_key': API_KEY,
		'api_secret': API_SECRET,
		'to': number,
		'from': FROM_NUMBER,
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
		print '--------------'
		print messages
		for message in messages:
			if message["status"] == "0":
				print "success"
	else :
		#Check the errors
		print "unexpected http {code} response from nexmo api". response.code
		print response.code


