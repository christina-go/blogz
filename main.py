from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from helper_functions import input_validation, password_match


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:sal3mr3ignS@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Sal3mr3!gnS'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(455))
    owner = db.Column(db.String(120), db.ForeignKey('user.email'))


    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    #blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['/login', '/signup', '/']
    if request.endpoint not in allowed_routes and 'email' not in session:
        flash("You must be logged in to continue")
        return redirect('/login')


@app.route('/')
def page_redirect():
    return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User does not exist")
            return render_template('login.html')

        if not password == user.password:
            flash("User password incorrect")
            return render_template('login.html')

        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/newpost')

    return render_template('login.html')        


@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        if input_validation(password) and password_match(password, verify) == True:
            existing_user = User.query.filter_by(email=email).first()

            if not existing_user:
                new_user = User(email, password)
                db.session.add(new_user)
                db.session.commit()
                session['email'] = email
                return redirect('/index')

            else:
                flash("User already exists")
                return render_template('signup.html')    

        else:
            if not input_validation(password):
                flash("Password must be more than 3 characters in length and contain no spaces")
            if not password_match(password, verify):
                flash("Password and password confirmation do not match")

                return render_template('signup.html')

    return render_template('signup.html')       

@app.route('/index', methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':

    #TODO: grab user info and display only their blog entries
    # owner = User.query.filter_by(email=session['email']).first()

        return render_template('singleUser.html')
    
    else:
    #TODO: if the request is a GET request, show all the blog users
    #as a href to their entries
    #all_blog_users = Users.query.all()
        return render_template('index.html')


@app.route('/newpost', methods=['POST', 'GET'])
def add_blog_post():
    
    if request.method == 'POST':
        
        title = request.form['title']
        body = request.form['body']
        owner = session['email']

        new_blog_post = Blog(title, body, owner)
        db.session.add(new_blog_post)
        db.session.commit()
        
        return redirect('/blog?id=' + str(new_blog_post.id))  
    
    else:
        
        all_blog_posts = Blog.query.all()

        return render_template('newpost.html', all_blog_posts=all_blog_posts)

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

if __name__ == '__main__':
    app.run()