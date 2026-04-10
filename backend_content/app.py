from flask import Flask, request
from config import Config
from models import db, User
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp
from werkzeug.security import generate_password_hash
from flask_cors import CORS

# from flask_caching import Cache
from extensions import Cache
import os
from flask import send_from_directory        
from flask_mail import Mail


app = Flask(__name__)
CORS(app)                 #it is only for connect backend to frontent
app.config.from_object(Config)   # config me jitni setthing store ki hai yha use karne ke liye isko use karte hai

cache = Cache(app)   

db.init_app(app)                


mail = Mail(app)

app.register_blueprint(auth_bp, url_prefix="/auth") 
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(company_bp,url_prefix="/company")
app.register_blueprint(student_bp, url_prefix="/student")



@app.route("/")
def home():
    return "Placement Portal Backend Running"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads'),
        filename
    )


@app.route('/exports/<filename>')
def export_file(filename):
    return send_from_directory(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'exports'),
        filename
    )




if __name__ == "__main__":

    with app.app_context():

        db.create_all()           

        # create admin automatically
        admin = User.query.filter_by(role="admin").first()

        if not admin:

            admin_user = User(
                name="Admin",
                email="admin@portal.com",
                password=generate_password_hash("admin123"),
                role="admin"
            )

            db.session.add(admin_user)

            db.session.commit()

            print("Admin created!")

    app.run(debug=True)