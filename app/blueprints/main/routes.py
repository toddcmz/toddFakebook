from . import bp
from app import app
from app.forms import UserSearchForm
from flask import render_template, g

@app.before_request
def before_request():
    g.user_search_form = UserSearchForm() # this is creating a new global variable

@bp.route('/')
def home():
    matrix = {
        'instructors': ('Sean', 'Dylan'),
        'students': ['beth', 'karim', 'allan', 'carie', 'boros']
    }
    return render_template('index.jinja', title='Home', instructors = matrix['instructors'], students=matrix['students'], user_search_form=g.user_search_form)

@bp.route('/friends')
def friends():
    return render_template('friends.jinja', title="Friends",user_search_form=g.user_search_form)

@bp.route('/about')
def about():
    return render_template('about.jinja', title='About', user_search_form=g.user_search_form)