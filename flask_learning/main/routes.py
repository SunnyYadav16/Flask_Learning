from flask import Blueprint, request, render_template
from flask_learning.models import Post
from flask_learning.posts.forms import SearchForm
from sqlalchemy import or_


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


@main.context_processor
def navbar():
    form = SearchForm()
    return dict(form=form)

@main.route('/search', methods=['POST'])
def search_post():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    if form.validate_on_submit():

        post_searched = form.searched.data
        print(post_searched)
        posts = posts.filter(or_(Post.title.like('%' + post_searched + '%'),Post.content.like('%' + post_searched + '%')))
        posts = posts.order_by(Post.title).all()


    return render_template("search.html", searched=post_searched, form=form, posts=posts)
