# Importing the necessary modules:
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Setting up the Flask app
app = Flask(__name__)

# Setting up the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Id of the task
    content = db.Column(db.String(200), nullable=True)  # Task Description, nullable for potential null values
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Date of creation

    def __repr__(self):
        return f'<Task {self.id}>'  # Representation of a task object

# Route for the home page
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')  # Getting the task content from the form
        if task_content is not None and task_content.strip():  # Check for non-empty content
            new_task = Todo(content=task_content)  # Creating a new task object and set its content
            try:
                db.session.add(new_task)  # Adding the new task to the database
                db.session.commit()  # Committing the changes
                return redirect('/')  # Redirecting to the home page
            except Exception as e:
                return f'There was an issue adding your task: {e}'
        else:
            return render_template('popup.html')  # Render the popup template

    else:
        # Getting all the tasks from the database and ordering them by date of creation
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)  # Rendering the home page with the tasks

# Route for deleting a task
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
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
                return redirect('/')
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)