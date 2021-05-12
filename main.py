# __init__.py -> this has essential components that need to be used from initialisation
from api import app, db, loginManager
# forms.py -> this has the forms which are accessed by the various routes
from api.forms import LoginForm, PostForm, EditForm, ReplyForm
# models.py -> this contains the database models (tables) which are used for storing data
from api.models import User, Post, Reply
# routes subfolder -> this contains files with relevent routes, which have been split off to keep file sizes smaller
from api.routes import auth, view, post, reply


@loginManager.user_loader
def userLoader(userID):
    return User.query.get(int(userID))


if __name__ == "__main__":
    app.run(port=5000)
