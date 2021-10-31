from flask import Blueprint, render_template


bp = Blueprint("tools", __name__, url_prefix="/tools")


@bp.route("/sanscript/")
def sanscript():
    return render_template(f"tools/sanscript.html")


@bp.route("/pandit/")
def pandit():
    return render_template(f"tools/pandit.html")


@bp.route("/ocr/")
def ocr():
    return render_template(f"tools/ocr.html")
