from flask import Blueprint, abort, current_app as app, render_template

main = Blueprint('main', __name__, url_prefix='/')
api = Blueprint('api', __name__, url_prefix='/api')


@main.teardown_request
def remove_session(exception=None):
    # TODO: teardown `sanskrit` session
    pass


@main.route('/')
def index():
    return render_template('index.html')


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500
