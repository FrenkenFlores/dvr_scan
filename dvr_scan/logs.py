from dvr_scan.auth import login_required
from flask import Blueprint, render_template
from .db import get_db


# The number of cameras on each page
PAGINATION = 2
bp = Blueprint("logs", __name__, url_prefix="/logs")


@bp.route("/", methods=["GET", "POST"])
@login_required
def logs():
    db = get_db()
    logs = db.execute("SELECT * FROM events").fetchall()
    db.close()
    return render_template("/logs.html", logs=logs)
