from flask import request, redirect, render_template, flash, session
from helper_functions import input_validation, password_match
from models import User, Blog
from app import app, db


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'list_blogs', 'single_post', 'index']
    if request.endpoint not in allowed_routes and 'email' not in session:
        flash("You must be logged in to continue")
        return redirect('/login')



@app.route('/')
def page_redirect():
    return redirect('/index')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User does not exist")
            return render_template('login.html', title="Log In to Bloggin")

        if not password == user.password:
            flash("User password incorrect")
            return render_template('login.html', title="Log In to Bloggin")

        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/newpost')

    return render_template('login.html', title="Log In to Bloggin")        



@app.route('/signup', methods=['POST', 'GET'])
def signup():
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
                return render_template('signup.html', title="Register to Bloggin")    

        else:
            if not input_validation(password):
                flash("Password must be more than 3 characters in length and contain no spaces")
            if not password_match(password, verify):
                flash("Password and password confirmation do not match")

                return render_template('signup.html', title="Register to Bloggin")

    return render_template('signup.html', title="Register to Bloggin")       



@app.route('/index', methods=['GET', 'POST'])
def index():    
    all_blog_users = User.query.all()
    return render_template('index.html', all_blog_users=all_blog_users)



@app.route('/blog', methods=['POST', 'GET'])
def list_blogs():    
    if request.method == 'GET':
        user = request.args.get('id')

        if user:
            single_user_posts = Blog.query.filter_by(owner=user).all()
            return render_template('blog.html', posts=single_user_posts)

        else:
            all_blog_posts = Blog.query.all()
            return render_template('blog.html', posts=all_blog_posts)             



@app.route('/blogpost')
def single_post():
    blog_id = request.args.get('id')
    post = Blog.query.get(blog_id)
    return render_template('blogpost.html', post=post)



@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        owner = session['email']

        new_blog_post = Blog(title, body, owner)
        db.session.add(new_blog_post)
        db.session.commit()
        
        return redirect('/blogpost?id=' + str(new_blog_post.id)) 

    else:
        return render_template('newpost.html')



@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')



if __name__ == '__main__':
    app.run()