import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.beat_schedule = {
    "daily-reminder": {
        "task": "tasks.send_daily_reminders",
        "schedule": crontab(hour=8, minute=0),
    },
    "monthly-report": {
        "task": "tasks.send_monthly_report",
        "schedule": crontab(day_of_month=1, hour=7, minute=0),
    },
}

def get_app():
    from app import app
    return app

def send_email(to, subject, html_body):
    app = get_app()
    from flask_mail import Message
    with app.app_context():
        from app import mail
        msg = Message(
            subject=subject,
            recipients=[to],
            html=html_body
        )
        mail.send(msg)
        print(f"Email sent to {to} ")

#  Daily Reminder
@celery.task
def send_daily_reminders():
    app = get_app()
    from models import PlacementDrive, Application, StudentProfile, User
    from datetime import date, timedelta

    with app.app_context():
        tomorrow = date.today() + timedelta(days=1)

        drives = PlacementDrive.query.filter_by(
            status="approved"
        ).filter(
            PlacementDrive.deadline == tomorrow
        ).all()

        for drive in drives:
            apps = Application.query.filter_by(
                drive_id=drive.id,
                status="applied"
            ).all()

            for a in apps:
                student = StudentProfile.query.get(a.student_id)
                user = User.query.get(student.user_id)

                html = f"""
                <h2>Drive Deadline Reminder</h2>
                <p>Dear {user.name},</p>
                <p>Drive <b>{drive.job_title}</b> ki deadline 
                <b>kal</b> hai!</p>
                <p>Abhi apply karo!</p>
                <br>
                <p>Placement Portal</p>
                """

                try:
                    send_email(
                        to=user.email,
                        subject=f"Reminder: {drive.job_title} deadline tomorrow!",
                        html_body=html
                    )
                except Exception as e:
                    print(f"Email error: {e}")


#  Monthly Report
@celery.task
def send_monthly_report():
    app = get_app()
    from models import PlacementDrive, Application, User

    with app.app_context():
        drives_count = PlacementDrive.query.count()
        applied = Application.query.count()
        selected = Application.query.filter_by(status="selected").count()
        rejected = Application.query.filter_by(status="rejected").count()
        shortlisted = Application.query.filter_by(status="shortlisted").count()

        admin = User.query.filter_by(role="admin").first()

        html = f"""
        <h2>Monthly Placement Activity Report</h2>
        <hr>
        <h3>Summary</h3>
        <table border="1" cellpadding="8" cellspacing="0">
            <tr>
                <th>Category</th>
                <th>Count</th>
            </tr>
            <tr>
                <td>Total Drives</td>
                <td>{drives_count}</td>
            </tr>
            <tr>
                <td>Total Applications</td>
                <td>{applied}</td>
            </tr>
            <tr>
                <td>Selected</td>
                <td>{selected}</td>
            </tr>
            <tr>
                <td>Shortlisted</td>
                <td>{shortlisted}</td>
            </tr>
            <tr>
                <td>Rejected</td>
                <td>{rejected}</td>
            </tr>
        </table>
        <br>
        <p>Placement Portal — Auto Generated Report</p>
        """

        try:
            send_email(
                to=admin.email,
                subject="Monthly Placement Activity Report",
                html_body=html
            )
        except Exception as e:
            print(f"Email error: {e}")


#  CSV Export
@celery.task
def export_student_csv(student_id):
    app = get_app()
    from models import Application, PlacementDrive, CompanyProfile, StudentProfile

    with app.app_context():
        apps = Application.query.filter_by(student_id=student_id).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Student ID", "Company", "Job Title", "Status", "Applied On"
        ])

        for a in apps:
            drive = PlacementDrive.query.get(a.drive_id)
            company = CompanyProfile.query.get(drive.company_id)
            writer.writerow([
                student_id,
                company.company_name,
                drive.job_title,
                a.status,
                str(a.application_date)
            ])

        os.makedirs("exports", exist_ok=True)
        filename = f"exports/student_{student_id}.csv"
        with open(filename, "w", newline="") as f:
            f.write(output.getvalue())

        return filename