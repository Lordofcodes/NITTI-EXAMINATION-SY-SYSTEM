from flask import Flask, render_template, flash, redirect, url_for, session, logging, request,json
from flask_mysqldb import MySQL
import os
from functools import wraps
app = Flask(__name__)

# config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'nitti'
app.config['MYSQL_PASSWORD'] = 'nitticomputer'
app.config['MYSQL_DB'] = 'students'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MySQL
mysql = MySQL(app)



@app.route('/', methods = ['GET', 'POST'])
	
def login():
	if request.method == 'POST':
		#get form field data
		username = request.form['username']
		password = request.form['password']
		#create cursor
		cur = mysql.connection.cursor()
		#get user by user name
		result = cur.execute("SELECT * FROM student_login_detail WHERE username=%s", [username])
		if result>0:
			#get the data
			data = cur.fetchone()
			candidate_password = data['password'];
			#compare password
			if password==candidate_password:
				session['logged_in'] = True
				session['username'] = username
				return redirect(url_for('dashboard') )
			else:
				error = 'Check your password.'
				return render_template('login.html',error=error)
			#close connection
			cur.sclose();
		else:
			error = 'User not found.'
			return render_template('login.html',error=error)
	return render_template('login.html')

#check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):

		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('login'))
	return wrap

#dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	return render_template('dashboard.html')

#logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	return redirect(url_for('login'))
@app.route('/test', methods=['GET','POST'])
@is_logged_in
def test():
	#create cursor
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM questions")
	data = cur.fetchall()
	if request.method == 'POST':
		score=0
		for i in range(len(request.form)):
			app.logger.info(request.form.getlist(str(i+1)))
			app.logger.info([data[i]['answer']])
			if request.form.getlist(str(i+1))==[data[i]['answer']]:
				score= score+1
		return render_template('result.html', score=score)
		app.logger.info(a)
	return render_template('quiz.html', data=data)
if __name__ == '__main__':
	app.secret_key = os.urandom(24)
	app.run(debug=True)
