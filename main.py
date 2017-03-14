#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import hashlib
import pymysql.cursors
import datetime
import os
import nexmoAPI
import time
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
	return render_template('construction.html', logged_in = True)


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
