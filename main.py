#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import hashlib
import pymysql.cursors
import datetime
import os
import nexmoAPI
import time
import BaseHTTPServer
import urlparse
#from secret import * //No need since in .env file and on heroku

#conn = pymysql.connect( host= HOST, user= USERNAME, password= PASSWORD, db= DB, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

#DEFINE VARIABLES
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
DB = os.environ.get("DB")
FROM_NUMBER = os.environ.get("FROM_NUMBER")
HOST = os.environ.get("HOST")
PASSWORD = os.environ.get("PASSWORD")
USERNAME = os.environ.get("USERNAME")

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
#	"""Tell Nexmo that you have recieved the GET request."""
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

		"""Parse parameters in the GET request"""
		parsed_path = urlparse(s.path)
		try:
				inbound_message = dict([p.split('=') for p in parsed_path[4].split('&')])
		except:
				inbound_message = {}

		message = ''
	#		"""Check the is an inbound message"""
		if  (not inbound_message.has_key('to') ) or (not inbound_message.has_key('msisdn')) or (not inbound_message.has_key('text')):
			p ("This is not an inbound message")
		elif inbound_message.has_key('concat'):
			"""Deal with a concatenated message"""
			message_parts = shelve.open( inbound_message['concat-ref'])
			message_parts[ inbound_message['concat-part']] = inbound_message['text']
			no_of_parts = len(message_parts)
			if Integer(inbound_message['concat-total']) == no_of_parts:
				iterator = iter(message_parts)
				for i in iterator:
					message = message_parts[i] + message
			message_parts.close()
		elif not message:
			message = inbound_message['text']

		if ( inbound_message['type'] == 'binary'):
			print "Do some binary stuff"
		elif (inbound_message['type'] == 'unicode'):
			print "Do some unicode stuff"
		elif message:
			print ( inbound_message['msisdn'] + " says " + message )
	


#Initialize the app from Flask
app = Flask(__name__)

#Define a route to hello function
@app.route('/')
def hello():
	if session.get('logged_in') is True:
		return redirect(url_for('home'))
	return redirect(url_for('index'))
	

#Define route for index
@app.route('/index')
def index():
	return render_template('index.html')
	
	
#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')


#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	try:
		conn = pymysql.connect( host= HOST, user= USERNAME, password= PASSWORD, db= DB, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	except:
		print "Yo you done messed up"
		error = 'Server connection error - contact site admin'
		return render_template('login.html', error=error)
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password'].encode('utf-8')
	md5password = hashlib.md5(password).hexdigest()
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM users WHERE username = %s and password = %s'
	cursor.execute(query, (username, md5password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	conn.close()
	if data:
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['logged_in'] = True
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)



@app.route('/home', methods=['GET', 'POST'])
def home():
	if session.get('logged_in') is not True:
		return redirect(url_for('index'))
	if request.method == "POST":
		numberstxt = request.form.get('numbers')
		textMessage = request.form.get('textMessage')
		numbers = numberstxt.split(',')
		cost = 0
		count = 0
		failures = []
		for number in numbers:
			messCost = nexmoAPI.sendText(number, textMessage)
			if messCost == 0:
				failures.append(number)
			else:
				cost += messCost
				count += 1
			time.sleep(1)
		print "GOT TO HERE!!!!!"
		print count
		print cost
		print failures
		return render_template('message_sent.html', logged_in = True, count = count, cost = cost, failures = failures)
	return render_template('home.html', logged_in = True)


@app.route('/construction')
def construction():
	if session.get('logged_in') is not True:
		return redirect(url_for('index'))
	return render_template('construction.html', logged_in = True)


@app.route('/incoming', methods=['GET', 'POST'])
def incoming():
	print "HERE!!!"
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class(('127.0.0.1', 5000), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % ('127.0.0.1', 5000)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % ('127.0.0.1', 5000)

@app.route('/logout')
def logout():
	if session.get('logged_in') is not True:
		return redirect(url_for('index'))
	session.pop('username')
	session.pop('logged_in')
	success = 'logged out!'
	return redirect(url_for('index'))


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
