from flask import Blueprint, request, jsonify
from models import db, User, PlacementDrive , CompanyProfile ,Application, StudentProfile
from multiple_use import check_role
from jwt_utils import verify_token
from extensions import cache             

admin_bp = Blueprint("admin", __name__)



@admin_bp.route("/test", methods=["GET"])
def test():
    return "Admin working"


@admin_bp.route("/approve-company", methods=["POST"])
def approve_company():

    from jwt_utils import verify_token

    #  TOKEN CHECK
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token missing"})

    data_token = verify_token(token)
    if not data_token:
        return jsonify({"error": "Invalid token"})

    user = User.query.get(data_token["user_id"])

    
    if not check_role(user, "admin"):
        return jsonify({"error": "Only admin can approve companies"})


    data = request.get_json()
    company_id = data.get("company_id")

    company = CompanyProfile.query.get(company_id)
    if not company:
        return jsonify({"error": "Company not found"})

    # approve
    company.approval_status = "approved"
    db.session.commit()

    return jsonify({"message": "Company approved successfully"})



@admin_bp.route("/approve-drive", methods=["POST"])
def approve_drive():

    from jwt_utils import verify_token

    
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token missing"})

    data_token = verify_token(token)
    if not data_token:
        return jsonify({"error": "Invalid token"})

    user = User.query.get(data_token["user_id"])

    
    if not check_role(user, "admin"):
        return jsonify({"error": "Only admin can approve drives"})

    
    data = request.get_json()
    drive_id = data.get("drive_id")

    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({"error": "Drive not found"})

    # approve
    drive.status = "approved"
    db.session.commit()

    return jsonify({"message": "Drive approved successfully"})

@admin_bp.route("/companies", methods=["GET"])
def get_companies():
    companies = CompanyProfile.query.all()
    result = []
    for c in companies:
        user = User.query.get(c.user_id)      # User fetch ho rha hai
        result.append({
            "id": c.id,
            "user_id": c.user_id,
            "company_name": c.company_name,
            "approval_status": c.approval_status,
            "is_active": user.is_active if user else True,  
            "email": user.email if user else "" 
        })
    return jsonify(result)


@admin_bp.route("/drives", methods=["GET"])
def get_drives():
    drives = PlacementDrive.query.all()

    result = []
    for d in drives:
        result.append({
            "id": d.id,
            "job_title": d.job_title,
            "status": d.status
        })

    return jsonify(result)



@admin_bp.route("/stats", methods=["GET"])
# @cache.cached(timeout=300, key_prefix="admin_stats")   
def get_stats():
    students = User.query.filter_by(role="student").count()
    companies = User.query.filter_by(role="company").count()
    drives = PlacementDrive.query.count()

    return jsonify({
        "students": students,
        "companies": companies,
        "drives": drives
    })



@admin_bp.route("/applications", methods=["GET"])
def get_all_applications():

    applications = Application.query.all()

    result = []

    for app in applications:
        student = StudentProfile.query.get(app.student_id)
        user = User.query.get(student.user_id)

        drive = PlacementDrive.query.get(app.drive_id)
        company = CompanyProfile.query.get(drive.company_id)

        result.append({
            "id": app.id,
            "student_name": user.name,
            "student_email": user.email,
            "company_name": company.company_name,
            "job_title": drive.job_title,
            "status": app.status,
            "applied_on": str(app.application_date),
            "resume": student.resume 
        })

    return jsonify(result)


@admin_bp.route("/search", methods=["GET"])
def search():

    query = request.args.get("q")

    students = User.query.filter(
        User.role == "student",
        User.name.ilike(f"%{query}%")
    ).all()

    companies = CompanyProfile.query.filter(
        CompanyProfile.company_name.ilike(f"%{query}%")
    ).all()

    student_result = []
    for s in students:
        student_result.append({
            "id": s.id,
            "name": s.name,
            "email": s.email
        })

    company_result = []
    for c in companies:
        company_result.append({
            "id": c.id,
            "company_name": c.company_name,
            "status": c.approval_status,
            "user_id": c.user_id   
        })

    return jsonify({
        "students": student_result,
        "companies": company_result
    })
@admin_bp.route("/toggle-user", methods=["POST"])
def toggle_user():

    token = request.headers.get("Authorization")
    if not token:                                    
        return jsonify({"error": "Token missing"})  
    
    data_token = verify_token(token)
    if not data_token:                                    
        return jsonify({"error": "Invalid token"})        

    user_admin = User.query.get(data_token["user_id"])

    if not check_role(user_admin, "admin"):
        return jsonify({"error": "Only admin allowed"})

    data = request.get_json()
    user_id = data.get("user_id")

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"})

    user.is_active = not user.is_active
    db.session.commit()

    return jsonify({
        "message": f"User {'activated' if user.is_active else 'deactivated'}",
        "is_active": user.is_active,
        "user_id": user_id  
    })
##################################################


@admin_bp.route("/reject-company", methods=["POST"])
def reject_company():

    token = request.headers.get("Authorization")
    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})
    
    user = User.query.get(data_token["user_id"])
    if not check_role(user, "admin"):
        return jsonify({"error": "Only admin allowed"})
    
    data = request.get_json()
    company = CompanyProfile.query.get(data.get("company_id"))

    if not company:
        return jsonify({"error": "Company not found"})
    
    company.approval_status = "rejected"
    db.session.commit()
    return jsonify({"message": "Company rejected"})

@admin_bp.route("/reject-drive", methods=["POST"])
def reject_drive():
    token = request.headers.get("Authorization")
    data_token = verify_token(token)

    if not data_token:
        return jsonify({"error": "Invalid token"})
    
    user = User.query.get(data_token["user_id"])
    if not check_role(user, "admin"):
        return jsonify({"error": "Only admin allowed"})
    
    data = request.get_json()
    drive = PlacementDrive.query.get(data.get("drive_id"))
    if not drive:
        return jsonify({"error": "Drive not found"})
    
    drive.status = "rejected"
    db.session.commit()
    return jsonify({"message": "Drive rejected"})




@admin_bp.route("/students", methods=["GET"])
def get_students():
    students = User.query.filter_by(role="student").all()
    result = []
    for s in students:
        result.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "is_active": s.is_active
        })
    return jsonify(result)


@admin_bp.route("/test-email", methods=["GET"])
def test_email():
    from tasks import send_daily_reminders, send_monthly_report
    send_monthly_report.delay()
    return jsonify({"message": "Email task triggered!"})