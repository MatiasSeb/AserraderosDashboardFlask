from flask import Blueprint, render_template
from flask_login import login_required

databaseRoutes = Blueprint('databaseRoutes', __name__)


@databaseRoutes.route("/admin/config_db")
@login_required
def admin_config_dbconn():
    return render_template("admin_config_dbconn.html")

@databaseRoutes.route("/admin/config_data")
@login_required
def admin_config_data():
    return render_template("admin_config_data.html")