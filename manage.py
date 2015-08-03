from flask.ext.script import Manager
from lso import create_app
import lso.database

app = create_app(__name__, 'development.config')

manager = Manager(app)


@manager.command
def create_db():
    """Creates all tables."""
    lso.database.db.create_all()


if __name__ == '__main__':
    manager.run()
