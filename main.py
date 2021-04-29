from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fshuppprcznqku:c40eea0c5cc185e4cc9eb252ff51fb571f04b373cc612420338962638ceda414@ec2-54-155-35-88.eu-west-1.compute.amazonaws.com:5432/d325f9dtt49eu3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'whatKey'

db = SQLAlchemy(app)
loginManager = LoginManager()
loginManager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return self.username

@loginManager.user_loader
def userLoader(userID):
    return User.query.get(int(userID))

@app.route('/')
def index():
    return render_template('index.html', title="Index Route")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        data = request.get_json()
        users = User.query.all()

        return redirect('/home')
        # user = User.query.filter_by(username).first()
        # login_user(user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method =='GET':
        return render_template('register.html')
    
    elif request.method == 'POST':
        data = request.get_json()
        users = User.query.all()

        for user in users:
            if data['username'] == user.username:
                return render_template('error.html')

        newUser = User(username=data['username'], password=generate_password_hash(data['password']))

        db.session.add(newUser)
        db.session.commit()       

        return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged Out")
    return redirect('/')

@app.route('/home')
@login_required
def home():
    return render_template('index.html', 
        title="Home", 
        content=f"Logged in as {current_user}", 
        )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
