from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Availability
from app.extenshions import db
from app.utils import role_required

doctor_bp = Blueprint("doctor", __name__, url_prefix="/doctor")

@doctor_bp.route("/dashboard")
@login_required
@role_required("doctor")
def dashboard():
    availabilities = Availability.query.filter_by(doctor_id=current_user.id).all()
    return render_template("doctor_dashboard.html", availabilities=availabilities)

@doctor_bp.route("/availability", methods=["GET", "POST"])
@login_required
@role_required("doctor")
def availability():
    if request.method == "POST":
        av = Availability(
            doctor_id=current_user.id,
            day=request.form["day"],
            start_time=request.form["start_time"],
            end_time=request.form["end_time"]
        )
        db.session.add(av)
        db.session.commit()
        return redirect(url_for("doctor.availability"))

    availabilities = Availability.query.filter_by(doctor_id=current_user.id).all()
    return render_template("availability.html", availabilities=availabilities)
