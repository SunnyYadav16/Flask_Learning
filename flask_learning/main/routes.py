from flask import Blueprint, request, render_template, jsonify
from flask_learning.models import Post, User
from sqlalchemy import or_
from sqlalchemy.orm import load_only
from flask_learning import db

from .forms import SearchForm

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home_page():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', form1=form, posts=posts)


@main.route("/about")
def about_user():
    return render_template('about.html', title='About')


@main.context_processor
def home_form():
    form = SearchForm()
    return dict(form=form)


@main.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    post_searched, author_searched, content_searched = "", "", ""
    start_date, end_date = None, None

    if form.validate_on_submit():
        filter_list = []

        """For searching data in the database according to the Author of the post"""
        if form.searched_author.data:
            author_searched = form.searched_author.data

            user_found = User.query.with_entities(User.id).filter(User.username.ilike('%' + author_searched + '%')).all()

            new_tuple = []
            for i in range(len(user_found)):
                new_tuple.append(user_found[i][0])

            new_tuple = tuple(new_tuple)
            filter_list.append(Post.user_id.in_(new_tuple))

        """For searching data in the database according to the content of the post"""
        if form.searched_post_by_content.data:
            content_searched = form.searched_post_by_content.data
            filter_list.append(Post.content.ilike('%' + content_searched + '%'))

        """For searching data in the database according to the title of the post"""
        if form.searched_post_by_title.data:
            post_searched = form.searched_post_by_title.data
            filter_list.append(Post.title.ilike('%' + post_searched + '%'))

        """For searching data in the database according to the startdate of the post"""
        if form.startdate.data:
            start_date = form.startdate.data.strftime('%Y-%m-%d')
            filter_list.append(Post.date_posted >= start_date)

        """For searching data in the database according to the enddate of the post"""
        if form.enddate.data:
            end_date = form.enddate.data
            filter_list.append(Post.date_posted <= end_date)

        """Final Query"""
        posts = Post.query.filter(*filter_list).order_by(Post.title).all()

    return render_template("search.html", form1=form, posts=posts)
