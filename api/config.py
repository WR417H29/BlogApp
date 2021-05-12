class AppConfig(object):  # this is an object that stores the configuration of the flask app
    SQLALCHEMY_DATABASE_URI = 'postgresql://fshuppprcznqku:c40eea0c5cc185e4cc9eb252ff51fb571f04b373cc612420338962638ceda414@ec2-54-155-35-88.eu-west-1.compute.amazonaws.com:5432/d325f9dtt49eu3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "oohnooneknowsthis"
