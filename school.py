from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# app configurations
app = Flask(__name__) # initialize flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///school' #connect to database from flask
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# linking sqlalchemy to flask app
db = SQLAlchemy(app)

# incase of changes in database schemas
migration = Migrate(app,db)

# creating models
class Schools(db.Model):
    '''Creates the table for schools in the database school'''
    __tablname__ = 'schools'
    sid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(15), nullable=False)
    telephone = db.Column(db.String(10), nullable=False)
    level = db.Column(db.String(10), nullable=False)

    # dunder method to return the created object
    # def __repr__(self):
    #     return f'<{self.name}: {self.location} {self.telephone} {self.level}>'

# maps model (the class and attributes) to table and columns in the table
db.create_all()

@app.route('/')
def index():
    return render_template('index.html', school=Schools.query.all())

@app.route('/school/create-school', methods=['POST'])
def create_school():
    # create variables to receive input from user through json
    name = request.get_json()['name']
    loc = request.get_json()['location']
    tel = request.get_json()['telephone']
    lev = request.get_json()['level']
    school = Schools(name=name,telephone=tel,location=loc,level=lev)
    db.session.add(school)
    db.session.commit()
    return jsonify({
        'name':school.name,
        'location':school.location,
        'telephone':school.telephone,
        'level':school.level
    })

if __name__=='__main__':
    app.debug=True
    app.run()
