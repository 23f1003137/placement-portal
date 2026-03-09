import os

class Config:

    SECRET_KEY = "placement-secret"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))   #Ye current folder ka absolute path deta hai.

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "placement.db")  #Isse database correct folder me create hota hai.
                                                                                     # example:- sqlite:///E:\Placement_Portal_V2\backend\placement.db

    SQLALCHEMY_TRACK_MODIFICATIONS = False