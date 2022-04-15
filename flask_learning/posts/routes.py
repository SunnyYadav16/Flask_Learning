from flask import Blueprint, render_template, redirect, flash, url_for, abort, request
from flask_login import login_required, current_user

from flask_learning import db
from flask_learning.models import Post
from flask_learning.posts.forms import PostForm, SearchForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f"Your posts has been created", "success")
        return redirect(url_for("main.home_page"))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', title='Post.title', post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your posts has been updated!", 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', form=form, title='Update Post', legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your posts has been deleted!", "success")
    return redirect(url_for('main.home_page'))


@posts.route('/search', methods=['GET', 'POST'])
def search_post():
    form = SearchForm()
    post = Post.query
    if form.validate_on_submit():
        post_searched = form.searched.data

        posts = post.filter(Post.content.like('%' + post_searched + '%'))
        posts = posts.order_by(Post.title).all()

    return render_template("search.html", post_searched=post_searched, form=form, posts=posts)
