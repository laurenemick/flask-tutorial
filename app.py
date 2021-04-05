from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

# initialize app
app = Flask(__name__)

# define DB uri or location
ENV = 'prod'

if ENV == 'dev': # we'll have our DB
    app.debug = True # b/c we're in development and want server to keep running
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/lexus'
else: # production
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iwjrmigeudxqsi:2f0df1425f12e94beb7bb73a2512c5605d5c01d2e1409d848a9cbb307a23aa96@ec2-52-1-115-6.compute-1.amazonaws.com:5432/d4kot7rptm64bk'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # or else we'll get a warning

db = SQLAlchemy(app) # use to query db

# MODELS
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    # constructor/initializer
    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/') # create route with decorator
def index(): # define method or Fn
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # get data and put form data into vars
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields.')
        # check if customer already exists
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template['success.html']
        return render_template('index.html', message='You have already submitted feedback.')

# make sure it's actually running
if __name__ == '__main__':
    app.run()