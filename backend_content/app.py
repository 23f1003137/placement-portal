from flask import Flask
from config import Config
from models import db, User

app = Flask(__name__)

app.config.from_object(Config)   # config me jitni setthing store ki hai yha use karne ke liye isko use karte hai

db.init_app(app)                 #Isse SQLAlchemy ko pata chal jata hai:
                                 #“Ye Flask app ka database hai”.


@app.route("/")
def home():
    return "Placement Portal Backend Running"


if __name__ == "__main__":

    with app.app_context():

        db.create_all()           #Ye saare models ko database tables me convert karta hai.

        # create admin automatically
        admin = User.query.filter_by(role="admin").first()

        if not admin:

            admin_user = User(
                name="Admin",
                email="admin@portal.com",
                password="admin123",
                role="admin"
            )

            db.session.add(admin_user)

            db.session.commit()

            print("Admin created!")

    app.run(debug=True)