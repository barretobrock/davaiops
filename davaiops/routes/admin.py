from flask import (
    render_template,
    Blueprint
)
from flask_login import login_required
# Internal packages
from davaiops.flask_base import db

admin = Blueprint('admin', __name__)


# @admin.route('/admin')
# @login_required
# def tables() -> str:
#     """Main blog"""
#     # Render buttons to tables
#     tbls = db.metadata.tables.keys()
#     return render_template('account/admin.html', tables=tbls, title='Admin')


# @admin.route('/admin/tbl/<string:tbl_name>')
# @login_required
# def render_table(tbl_name: str):
#     page = request.args.get('page', 1, type=int)
#     if tbl_name in db.metadata.tables.keys():
#         # Begin rendering table
#         model = get_model_by_tablename(db, tbl_name)
#         results = model.query.paginate(page=page, per_page=20)
#         return render_template('account/admin_table.html', results=results)
#     else:
#         flash(f'Table {tbl_name} not found. Please check the name and try again.', 'alert-danger')
