from flask import Blueprint, redirect, render_template, session, url_for
from .forms import InfoForms
from flask_learning.models import Post
from datetime import datetime

date_time = Blueprint('date_time_picker', __name__)


@date_time.route("/dating", methods=['GET', 'POST'])
def select_date_time():
    form = InfoForms()
    if form.validate_on_submit():
        session['startdate'] = form.start_date.data
        session['enddate'] = form.end_date.data
        return redirect(url_for('date_time_picker.dates'))
    return render_template('dating.html', form=form)


@date_time.context_processor
def formss():
    form = InfoForms()
    return dict(form=form)


@date_time.route("/datetime", methods=["GET", "POST"])
def dates():
    startdate = session['startdate']
    enddate = session['enddate']

    startdate = datetime.strptime(startdate, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')
    enddate = datetime.strptime(enddate, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')
    posts = Post.query.filter(Post.date_posted.between(startdate, enddate))
    return render_template('date.html', posts=posts)
