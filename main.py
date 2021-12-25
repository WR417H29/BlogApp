from api import app, loginManager
from api.models.user import User


@loginManager.user_loader
def userLoader(userID):
    return User.query.get(int(userID))


if __name__ == "__main__":
    app.run(port=8080)
