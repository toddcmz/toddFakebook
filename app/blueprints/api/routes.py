from flask import request, jsonify
from . import bp
from app.models import Post, User
from app.blueprints.api.helpers import token_required

# we started writing some structure for what we want the API to allow
# a user to do

# receive all posts
@bp.get('/posts')
@token_required
def api_posts(thisUser):
    result = []
    # add to this list all posts in database
    thesePosts = Post.query.all() # .all() is returning all posts, where is post is a class
    for eachPost in thesePosts:
        result.append({'id': eachPost.id,
                       'body':eachPost.body,
                       'timestamp': eachPost.timestamp,
                       'author': eachPost.user_id})
        
    return jsonify(result), 200 # this 200 is returning a "success" status

# receive posts from single user
@bp.get('/posts/<username>')
@token_required
def user_posts(thisUser, username):
    thisUser = User.query.filter_by(username=username).first()
    if thisUser: # if they give us a username we query for it, if there's no match then the username give was invalid
        return jsonify([{'id': eachPost.id,
                        'body':eachPost.body,
                        'timestamp': eachPost.timestamp,
                        'author': eachPost.user_id
                        } for eachPost in thisUser.posts]), 200
    return jsonify([{'message':'Invalid username'}]), 404

# send single post
@bp.get('/post/<postid>')
@token_required
def get_post(thisUser, postid):
    try:
        thisPost = Post.query.get(postid)
        return jsonify([{'id': thisPost.id,
                        'body':thisPost.body,
                        'timestamp': thisPost.timestamp,
                        'author': thisPost.user_id
                        }]), 200
    except:
        return jsonify([{'message': 'Invalid post id'}]), 404

# make a post
@bp.post('/newPost')
@token_required
def make_post(thisUser):
    try:
        # receive post data
        thisContent = request.json
        # make an instance of a post
        # add foreign key to user id column in post table
        thisPost = Post(body=thisContent.get('body'), user_id=thisUser.user_id)
        # commit post
        thisPost.commit()
        # return message
        return jsonify([{'message':'Post Created', 'body':thisPost.body}]), 200
    except:
        return jsonify([{'message': 'invalid form data for new post'}]), 401