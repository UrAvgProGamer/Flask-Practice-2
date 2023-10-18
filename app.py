# Importing the necessary modules:
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Setting up the Flask app
app = Flask(__name__)
app.secret_key = 'e1a139751d4d7926bb9d4d1faea91a0ffcdc05321a54d750'

# Setting up the SQLite database
app.config.from_pyfile('instance/config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Todo', backref='user', lazy=True)  # Define the relationship with tasks

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Add user_id foreign key

    def __repr__(self):
        return f'<Task {self.id}>'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for the home page
@app.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')
        if task_content is not None and task_content.strip():
            new_task = Todo(content=task_content, user=current_user)  # Set user_id using current_user
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/index')
            except Exception as e:
                return f'There was an issue adding your task: {e}'
        else:
            return render_template('popup.html')

    else:
        tasks = current_user.tasks  # Get tasks associated with current user
        return render_template('index.html', tasks=tasks)

# Route for deleting a task
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/index')
    except Exception as e:
        return f'There was a problem deleting the task: {e}'

# Route for updating a task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_content = request.form.get('content')
        if task_content is not None and task_content.strip():
            task.content = task_content
            try:
                db.session.commit()
                return redirect('/index')
            except Exception as e:
                return f'There was an issue updating your task: {e}'
        else:
            return render_template('popup.html')
    else:
        return render_template('update.html', task=task)

# Route for displaying popup
@app.route('/popup')
def popup():
    return render_template('popup.html')

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)  # Log in the user
            next_page = request.args.get('next')  # Get the next parameter from the URL
            return redirect(next_page or '/index')  # Redirect to next page or /index

        return 'Invalid username or password. Please try again.'

    return render_template('login.html')

# Route for registering a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return 'Both username and password are required.'

        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return 'User registered successfully!'
        except Exception as e:
            return f'There was an issue registering the user: {e}'

    return render_template('register.html')

# Route for displaying user information
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
