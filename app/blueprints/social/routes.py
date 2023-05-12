from . import bp 
from flask import render_template, flash, redirect, url_for, g
from app.models import Post, User
from app.forms import PostForm
from flask_login import current_user, login_required

@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        thisPost = Post(body=form.body.data)
        thisPost.user_id = current_user.user_id
        thisPost.commit()
        # redirecting to user page (not yet built out)
        flash('Published', 'success')
        return redirect(url_for('social.user_page', username=current_user.username))
    return render_template('post.jinja', title='New Post', form=form, user_search_form=g.user_search_form)

# the <username> is using a "slug"
@bp.route('/userpage/<username>')
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first() # this should return one row of one element
    # if we didn't use.first() we'd get a list back instead of just one element.
    return render_template('user_page.jinja', title="All Posts", user = user, user_search_form=g.user_search_form)

@bp.post('/usersearch')
@login_required
def user_search():
    if g.user_search_form.validate_on_submit:
        return redirect(url_for('social.user_page', username = g.user_search_form.user.data))
    return redirect(url_for('main.home'))