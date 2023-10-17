#Importing modules
from flask import Flask, render_template, url_for
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
@app.route('/')
def index():
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)