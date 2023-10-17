#Importing modules
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Setting up the Flask app
app = Flask(__name__)

#Setting up the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True) #Id of the task
    content = db.Column(db.String(200), nullable = False) #Task Description
    date_created = db.Column(db.DateTime, default = datetime.utcnow) #Date of creation
    
    def __repr__(self):
        return '<Task %r>' % self.id

##Routes:

#Route for the home page
@app.route('/', methods= ['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] #Getting the task content from the form
        new_task = Todo(content = task_content) #Creating a new task object and set its content
        
        try:
            db.session.add(new_task) #Adding the new task to the database
            db.session.commit() #Commiting the changes
            return redirect('/') #Redirecting to the home page
        except:
            return 'There was an issue adding your task'
        
    else:
        
        #Getting all the tasks from the database and ordering them by date of creation
        tasks = Todo.query.order_by(Todo.date_created).all() 
        
        return render_template('index.html', tasks = tasks) #Rendering the home page with the tasks

#Route for deleting a task       
@app.route('/delete/<int:id>')
def delete(id):
    
    #Getting the task to delete
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete) #Deleting the task
        db.session.commit() #Commiting the changes
        return redirect('/') #Redirecting to the home page
    except:
        return 'There was a problem deleting the task'
    
#Route for updating a task
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    
    #Getting the task to update
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit() #Commiting the changes
            return redirect('/') #Redirecting to the home page
        except:
            return 'There was an issue updating your task'
        
    else:
        return render_template('update.html', task = task)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)