from flask import Blueprint, render_template
from flask_login import login_required
from app.models import User, Appointment
from app.utils import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    doctors = User.query.filter_by(role="doctor").all()
    appointments = Appointment.query.all()
    return render_template(
        "admin_dashboard.html",
        doctors=doctors,
        appointments=appointments
    )
