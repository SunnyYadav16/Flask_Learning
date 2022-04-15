from flask import Blueprint, request, render_template
from flask_learning.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home_page():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about_user():
    return render_template('about.html', title='About')
