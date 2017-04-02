#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import hashlib
import pymysql.cursors
import datetime
from secret import *

#conn = pymysql.connect( host= HOST, user= USERNAME, password= PASSWORD, db= DB, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

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
	conn = pymysql.connect( host= HOST, user= USERNAME, password= PASSWORD, db= DB, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password'].encode('utf-8')
	print username
	print password
	md5password = hashlib.md5(password).hexdigest()
	print md5password
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
	print data
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
	if request.method == "POST":
		print "HEJEKHFKJDKJFS"
	return render_template('home.html', logged_in = True)


@app.route('/construction')
def construction():
	return render_template('construction.html', logged_in = True)


<<<<<<< Updated upstream
=======
@app.route('/incoming', methods=['POST'])
def incoming():
#	Json looks like
#	{u'type': u'text', u'message-timestamp': u'2017-03-15 06:10:32', u'messageId': u'0C000000214A3020', u'text': u"It's working!", u'msisdn':
#		u'13478135351', u'to': u'16202052698', u'keyword': u"IT'S"}
	if request.method == 'POST':
		textJson = request.json
		print "sent from: " + textJson['msisdn']
		print "text: " + textJson['text']
		#TODO
		try:
			conn = pymysql.connect( host= HOST, user= USERNAME, password= PASSWORD, db= DB, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
		except:
			return "", 200
		cursor = conn.cursor()
		#executes query
		query = "INSERT INTO `in_message` (`number`, `message`, `time`) VALUES (%s, %s, %s)"
		cursor.execute(query, (textJson['msisdn'], textJson['text'], textJson['message-timestamp']))
		#stores the results in a variable
		conn.commit()
		#use fetchall() if you are expecting more than 1 data row
		cursor.close()
		return '', 200
	else:
		abort(400)

>>>>>>> Stashed changes
@app.route('/logout')
def logout():
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
