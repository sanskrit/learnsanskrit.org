from flask import Blueprint, jsonify


bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/pandit/<q>")
def pandit(q):
    data = {"q": q}
    return jsonify(data)
