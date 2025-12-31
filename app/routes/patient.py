from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Appointment
from app.extenshions import db
from app.utils import role_required

patient_bp = Blueprint("patient", __name__, url_prefix="/patient")

@patient_bp.route("/dashboard")
@login_required
@role_required("patient")
def dashboard():
    doctors = User.query.filter_by(role="doctor").all()
    return render_template("patient_dashboard.html", doctors=doctors)

@patient_bp.route("/book/<int:doctor_id>", methods=["GET", "POST"])
@login_required
@role_required("patient")
def book(doctor_id):
    doctor = User.query.get_or_404(doctor_id)

    if request.method == "POST":
        appt = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor.id,
            date=request.form["date"],
            time=request.form["time"]
        )
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for("patient.dashboard"))

    return render_template("book_appointment.html", doctor=doctor)
