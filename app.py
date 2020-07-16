from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'I am Random'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	def __repr__(self):
		return '<task %r>' % self.id

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))


@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == "POST":
		if request.form['pass1'] == request.form['pass2']:
			uname = request.form['uname']
			mail = request.form['email']
			passwd = request.form['pass1']
			register = user(username = uname, email = mail, password = passwd)
			db.session.add(register)
			db.session.commit()
			return redirect('login.html')
		else:
			return "Password Does not match!!"

	else:
		return render_template('register.html')

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
    	session['username'] = request.form["uname"]
    	uname = request.form["uname"]
    	passwd = request.form["passwd"]
    	login = user.query.filter_by(username=uname, password=passwd).first()
    	if login is not None:
            return redirect('/dash')
    else:
    	return render_template('/login.html')

@app.route("/dash",methods=["GET", "POST"])
def dash():
	if 'username' in session:
		username = session['username']
		if request.method == 'POST':
			task_content = request.form['content']
			new_task = Todo(content=task_content)
			try:
				db.session.add(new_task)
				db.session.commit()
				return redirect('/dash')
			except:
				return 'There was an issue adding your task'

		else:
			tasks = Todo.query.order_by(Todo.date_created).all()
			return render_template('dash.html', username=username, tasks=tasks)
	else:
		return redirect('/login')

@app.route('/logout', methods=['POST','GET'])
def logout():
	session.pop('username', None)
	return redirect('/')

@app.route('/', methods=['POST','GET'])
def index():
	return render_template('index.html')


@app.route('/delete/<int:id>')
def delete(id):
	task_to_delete = Todo.query.get_or_404(id)

	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/dash')
	except:
		return 'There was a problem to delete that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
	task = Todo.query.get_or_404(id)

	if request.method == 'POST':
		task.content = request.form['content']

		try:
			db.session.commit()
			return redirect('/dash')
		except:
			return 'There was an issue updating your task'

	else:
		return render_template('update.html',task=task)


if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)