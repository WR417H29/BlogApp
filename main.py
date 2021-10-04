from api import app, db, loginManager
from api.routes import auth, view, post, reply
from api.models.user import User


@loginManager.user_loader
def userLoader(userID):
    return User.query.get(int(userID))


if __name__ == "__main__":
    app.run(port=5000)
