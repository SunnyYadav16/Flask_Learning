from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, StringField
from wtforms.validators import Optional


class SearchForm(FlaskForm):
    searched_post_by_title = StringField('Searched Post Title')
    searched_post_by_content = StringField('Searched Post Content')
    searched_author = StringField('Searched Author')
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    enddate = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Search')
