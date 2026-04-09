from flask import Blueprint, request, jsonify
from models import db, User, StudentProfile, CompanyProfile
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from jwt_utils import generate_token






auth_bp = Blueprint("auth", __name__)      #Blueprint Flask ka modular routing system hai.
                                           #(Ye file authentication routes handle karegi.)


@auth_bp.route("/register/student", methods=["POST"])  
def register_student():

    data = request.get_json()  
    print("DATA RECEIVED:", data)

    name = data.get("name")
    email = data.get("email")
    password = generate_password_hash(data.get("password"))
    branch = data.get("branch")
    cgpa = data.get("cgpa")
    year = data.get("year")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Email already exists"})

    # create user
    user = User(
        name=name,
        email=email,
        password=password,
        role="student"
    )

    db.session.add(user)
    db.session.commit()

    print("User created with ID:", user.id)

    # create student profile
    student = StudentProfile(
        user_id=user.id,
        branch=branch,
        cgpa=cgpa,
        year=year
    )

    print("Creating student profile...")

    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student registered successfully"})
   


@auth_bp.route("/register/company", methods=["POST"])
def register_company():

    data = request.get_json()

    email = data.get("email")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already exists"})


    # create user
    user = User(
        name=data.get("name"),
        email=data.get("email"),
        password=generate_password_hash(data.get("password")),
        role="company"
    )

    db.session.add(user)
    db.session.commit()

    # create company profile
    company = CompanyProfile(
        user_id=user.id,
        company_name=data.get("company_name"),
        hr_contact=data.get("hr_contact"),
        website=data.get("website")
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({"message": "Company registered successfully"})



@auth_bp.route("/login", methods=["POST"])
def login():
    print("LOGIN API HIT")  

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    
    if not email or not password:
        return jsonify({"error": "Email and password required"})

    
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"})

    # check active
    if not user.is_active:
        return jsonify({"error": "Account is deactivated by admin"})

    
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password"})

    # generate token
    token = generate_token(user)

    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role,
        "token": token
    })



