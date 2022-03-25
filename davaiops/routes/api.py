from flask import Blueprint

# Internal packages

api = Blueprint('api', __name__)


# @api.route('/api/tbl/posts')
# def get_posts() -> str:
#     """Return posts table"""
#     query_parameters = request.args
#     id = query_parameters.get('id')
#     if id is None:
#         # Return the whole table
#         posts = Posts.query.order_by(Posts.id.asc()).all()
#     else:
#         # Filter by id
#         posts = Posts.query.filter_by(id=id).all()
#     return jsonify(posts)

#
# @api.route('/api/tbl/user')
# def get_users() -> str:
#     """Return user table"""
#     query_parameters = request.args
#     id = query_parameters.get('id')
#     query = User.query
#     if id is None:
#         # Return the whole table
#         query = query.order_by(User.id.asc())
#     else:
#         # Filter by id
#         query = query.filter(User.id == id)
#     query = query.with_entities(User.id, User.username)
#
#     # return jsonify(query.all())
#     return jsonify(db.session.query(User).options(defer(User.password)))
