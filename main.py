from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:sal3mr3ignS@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Sal3mr3!gnS'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(455))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def page_redirect():
    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def display():
    if request.method == 'GET':

        blog_id = request.args.get('id')

        if (blog_id):
            post = Blog.query.get(blog_id)

            return render_template('blogpost.html', post=post)
    
    all_blog_posts = Blog.query.all()

    return render_template('blog.html', all_blog_posts=all_blog_posts) 

@app.route('/newpost', methods=['POST', 'GET'])
def add_blog_post():
    
    if request.method == 'POST':
        
        title = request.form['title']
        body = request.form['body']

        new_blog_post = Blog(title, body)
        db.session.add(new_blog_post)
        db.session.commit()
        
        return redirect('/blog?id=' + str(new_blog_post.id))  
    
    else:
        
        all_blog_posts = Blog.query.all()

        return render_template('newpost.html', all_blog_posts=all_blog_posts)


if __name__ == '__main__':
    app.run()