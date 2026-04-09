import os
from flask import send_from_directory
from werkzeug.utils import secure_filename
from extensions import cache   

from flask import Blueprint, request, jsonify
from models import db,  User, StudentProfile, PlacementDrive, Application, CompanyProfile
from multiple_use import check_role
from jwt_utils import verify_token


student_bp = Blueprint("student", __name__)




@student_bp.route("/test", methods=["POST"])
def test_student():

    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"})

    if user.role != "student":
        return jsonify({"error": "Access denied: Only students allowed"})

    return jsonify({"message": "Welcome Student"})







@student_bp.route("/drives", methods=["POST"])
def view_drives():
    token = request.headers.get("Authorization")
    data_token = verify_token(token)
    if not data_token:
        return jsonify({"error": "Invalid token"})

    user = User.query.get(data_token["user_id"])
    data = request.get_json()
    branch = data.get("branch")

    if not check_role(user, "student"):
        return jsonify({"error": "Only students can view drives"})


    if branch:
        drives = PlacementDrive.query.filter_by(status="approved", branch_required=branch).all()
    else:
        drives = PlacementDrive.query.filter_by(status="approved").all()

    result = []
    for drive in drives:
        result.append({
            "id": drive.id,
            "job_title": drive.job_title,
            "company_id": drive.company_id,
            "branch_required": drive.branch_required,
            "cgpa_required": drive.cgpa_required,
            "year_required": drive.year_required,
            "deadline": str(drive.deadline)
        })

    # 5 min ke liye save
    # cache.set(cache_key, result, timeout=300)

    return jsonify(result)




@student_bp.route("/apply", methods=["POST"])
def apply_drive():

    from jwt_utils import verify_token

    #  TOKEN CHECK
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"})

    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})

    user = User.query.get(data_token["user_id"])


    data = request.get_json()
    drive_id = data.get("drive_id")

    
    if not check_role(user, "student"):
        return jsonify({"error": "Only students can apply"})

    #
    student = StudentProfile.query.filter_by(user_id=user.id).first()

    if not student:
        return jsonify({"error": "Student profile not found"})

    
    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({"error": "Drive not found"})

    # eligibility checks
    if drive.branch_required != student.branch:
        return jsonify({"error": "Not eligible: Branch mismatch"})

    if student.cgpa < drive.cgpa_required:
        return jsonify({"error": "Not eligible: CGPA too low"})

    if student.year != drive.year_required:
        return jsonify({"error": "Not eligible: Year mismatch"})

    # duplicate apply check
    existing_application = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()

    if existing_application:
        return jsonify({"error": "Already applied to this drive"})

    # create application
    application = Application(
        student_id=student.id,
        drive_id=drive.id
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Applied successfully"})




@student_bp.route("/applications", methods=["POST"])
def student_applications():

    from jwt_utils import verify_token

    
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"})

    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})

    user = User.query.get(data_token["user_id"])

    
    if not check_role(user, "student"):
        return jsonify({"error": "Only students allowed"})

    
    student = StudentProfile.query.filter_by(user_id=user.id).first()

    if not student:
        return jsonify({"error": "Student profile not found"})

    # applications
    applications = Application.query.filter_by(student_id=student.id).all()

    result = []

    for app in applications:
        drive = PlacementDrive.query.get(app.drive_id)
        company = CompanyProfile.query.get(drive.company_id)
        company_user = User.query.get(company.user_id)

        result.append({
            "company_name": company.company_name,
            "job_title": drive.job_title,
            "status": app.status,
            "applied_on": str(app.application_date)
        })

    return jsonify(result)






UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@student_bp.route("/profile", methods=["GET"])
def get_profile():

    token = request.headers.get("Authorization")
    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})
    
    user = User.query.get(data_token["user_id"])
    student = StudentProfile.query.filter_by(user_id=user.id).first()
    return jsonify({
        "name": user.name,
        "email": user.email,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "year": student.year,
        "resume": student.resume
    })

@student_bp.route("/profile", methods=["PUT"])
def update_profile():

    token = request.headers.get("Authorization")
    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})
    
    user = User.query.get(data_token["user_id"])
    student = StudentProfile.query.filter_by(user_id=user.id).first()
    data = request.get_json()
    if data.get("name"):
        user.name = data["name"]
    if data.get("branch"):
        student.branch = data["branch"]
    if data.get("cgpa"):
        student.cgpa = data["cgpa"]
    if data.get("year"):
        student.year = data["year"]
    db.session.commit()
    return jsonify({"message": "Profile updated"})

@student_bp.route("/upload-resume", methods=["POST"])
def upload_resume():

    token = request.headers.get("Authorization")
    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})
    user = User.query.get(data_token["user_id"])
    student = StudentProfile.query.filter_by(user_id=user.id).first()
    file = request.files.get("resume")

    if not file:
        return jsonify({"error": "No file uploaded"})
    filename = secure_filename(f"resume_{user.id}_{file.filename}")
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    student.resume = filename
    db.session.commit()
    return jsonify({"message": "Resume uploaded", "filename": filename})





@student_bp.route("/export", methods=["POST"])
def export_csv():

    token = request.headers.get("Authorization")
    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})
    user = User.query.get(data_token["user_id"])
    student = StudentProfile.query.filter_by(user_id=user.id).first()
    
    from tasks import export_student_csv
    task = export_student_csv.delay(student.id)
    return jsonify({"message": "Export started", "task_id": task.id})

@student_bp.route("/task-status/<task_id>", methods=["GET"])
def task_status(task_id):
    from tasks import export_student_csv
    task = export_student_csv.AsyncResult(task_id)

    if task.state == "SUCCESS":
        filename = os.path.basename(task.result)
        return jsonify({
            "status": "done",
            "file": task.result,
            "download_url": f"http://127.0.0.1:5000/exports/{filename}"
        })
    return jsonify({"status": task.state})


@student_bp.route("/companies", methods=["GET"])
def get_companies():
    token = request.headers.get("Authorization")
    data_token = verify_token(token)
    if not data_token:
        return jsonify({"error": "Invalid token"})

    # Sirf approved companies
    companies = CompanyProfile.query.filter_by(
        approval_status="approved"
    ).all()

    result = []
    for c in companies:
        user = User.query.get(c.user_id)

        # Company ki approved drives
        drives = PlacementDrive.query.filter_by(
            company_id=c.id,
            status="approved"
        ).all()

        drives_list = []
        for d in drives:
            drives_list.append({
                "id": d.id,
                "job_title": d.job_title,
                "job_description": d.job_description,
                "branch_required": d.branch_required,
                "cgpa_required": d.cgpa_required,
                "year_required": d.year_required,
                "deadline": str(d.deadline),
                "salary": d.salary 
            })

        result.append({
            "id": c.id,
            "company_name": c.company_name,
            "website": c.website,
            "hr_contact": c.hr_contact,
            "drives": drives_list
        })

    return jsonify(result)