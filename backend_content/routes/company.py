from flask import Blueprint, request, jsonify
from models import db, User, PlacementDrive, CompanyProfile, StudentProfile, Application
from datetime import datetime
from multiple_use import check_role
from jwt_utils import verify_token



company_bp= Blueprint("company", __name__)



@company_bp.route("/create-drive", methods=["POST"])
def create_drive():

    from jwt_utils import verify_token

    # TOKEN CHECK
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"})

    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})

    user = User.query.get(data_token["user_id"])


    data = request.get_json()

    
    if not check_role(user, "company"):
        return jsonify({"error": "Only companies can create drives"})

    
    company = CompanyProfile.query.filter_by(user_id=user.id).first()

    if not company:
        return jsonify({"error": "Company profile not found"})

    if company.approval_status != "approved":
        return jsonify({"error": "Company not approved by admin"})

    # create drive
    drive = PlacementDrive(
        company_id=company.id,
        job_title=data.get("job_title"),
        job_description=data.get("job_description"),
        branch_required=data.get("branch"),
        cgpa_required=data.get("cgpa"),
        year_required=data.get("year"),
        deadline=datetime.strptime(data.get("deadline"), "%Y-%m-%d").date(),
        salary=data.get("salary", "Not Disclosed") 
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({"message": "Placement drive created successfully"})


@company_bp.route("/my-drives", methods=["GET"])
def my_drives():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token missing"})

    data_token = verify_token(token)
    if not data_token:
        return jsonify({"error": "Invalid token"})

    user = User.query.get(data_token["user_id"])
    if not check_role(user, "company"):
        return jsonify({"error": "Only company allowed"})

    company = CompanyProfile.query.filter_by(user_id=user.id).first()
    if not company:
        return jsonify({"error": "Company profile not found"})

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    result = []
    for d in drives:
        applications = Application.query.filter_by(drive_id=d.id).all()

        applicants = []
        for app in applications:
            student = StudentProfile.query.get(app.student_id)
            student_user = User.query.get(student.user_id)
            applicants.append({
                "application_id": app.id,
                "student_name": student_user.name,
                "student_email": student_user.email,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "year": student.year,
                "resume": student.resume,
                "status": app.status
            })

        result.append({
            "id": d.id,
            "job_title": d.job_title,
            "job_description": d.job_description,
            "branch_required": d.branch_required,
            "cgpa_required": d.cgpa_required,
            "year_required": d.year_required,
            "salary": d.salary,
            "deadline": str(d.deadline),
            "status": d.status,
            "total_applicants": len(applicants),
            "applicants": applicants
        })

    return jsonify(result)



@company_bp.route("/close-drive", methods=["POST"])
def close_drive():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token missing"})

    data_token = verify_token(token)
    if not data_token:
        return jsonify({"error": "Invalid token"})

    user = User.query.get(data_token["user_id"])
    if not check_role(user, "company"):
        return jsonify({"error": "Only company allowed"})

    data = request.get_json()
    drive_id = data.get("drive_id")

    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({"error": "Drive not found"})

    company = CompanyProfile.query.filter_by(user_id=user.id).first()
    if drive.company_id != company.id:
        return jsonify({"error": "Unauthorized"})

    drive.status = "closed"
    db.session.commit()

    return jsonify({"message": "Drive closed successfully"})






@company_bp.route("/applications", methods=["POST"])
def view_applications():

    from jwt_utils import verify_token

    # TOKEN CHECK
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"})

    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})

    user = User.query.get(data_token["user_id"])

    
    if not check_role(user, "company"):
        return jsonify({"error": "Only companies can view applications"})

    
    company = CompanyProfile.query.filter_by(user_id=user.id).first()

    if not company:
        return jsonify({"error": "Company profile not found"})

    # company ke drives
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    result = []

    for drive in drives:

        applications = Application.query.filter_by(drive_id=drive.id).all()

        for app in applications:

            student = StudentProfile.query.filter_by(id=app.student_id).first()
            user_obj = User.query.filter_by(id=student.user_id).first()

            result.append({
                "id": app.id,
                "student_name": user_obj.name,
                "student_email": user_obj.email,
                "drive_id": drive.id,
                "job_title": drive.job_title,
                "status": app.status
            })

    return jsonify(result)



@company_bp.route("/update-status", methods=["POST"])
def update_application_status():

    from jwt_utils import verify_token

    # TOKEN CHECK
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"})

    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})

    user = User.query.get(data_token["user_id"])


    if not check_role(user, "company"):
        return jsonify({"error": "Only company can update status"})

    
    data = request.get_json()
    application_id = data.get("application_id")
    status = data.get("status")  # shortlisted / selected / rejected

    
    application = Application.query.get(application_id)

    if not application:
        return jsonify({"error": "Application not found"})

    
    drive = PlacementDrive.query.get(application.drive_id)

    
    company = CompanyProfile.query.filter_by(user_id=user.id).first()

    # SECURITY CHECK
    if drive.company_id != company.id:
        return jsonify({"error": "Unauthorized: Not your drive"})

    # update status
    application.status = status
    db.session.commit()

    return jsonify({"message": "Status updated successfully"})