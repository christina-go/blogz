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


@app.route('/blog', methods=['GET', 'POST'])
def index():

    blog_posts = Blog.query.filter_by().all()
    return render_template('all-blog-posts.html', title=title, body=body)



@app.route('/newpost', methods=['POST', 'GET'])
def add_blog_post():
    
    if request.method == 'POST':
        
        title = request.form['title']
        body = request.form['body']
        
        new_blog_post = Blog(title, body)
        db.session.add(new_blog_post)
        db.session.commit()  

        return redirect('/blog')  
    
    flash("Something went wrong")
    return render_template('add-blog-post.html')


if __name__ == '__main__':
    app.run()