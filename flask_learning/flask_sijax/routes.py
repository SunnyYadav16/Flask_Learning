from flask import g, Blueprint, render_template

flask_sijax = Blueprint('flask_sijax', __name__)


@flask_sijax.route('/hello')
def hello():
    def say_hi(obj_response):
        obj_response.alert('Hi there!')

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('say_hi', say_hi)
        return g.sijax.process_request()
    return render_template('about.html')
