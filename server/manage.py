import datetime
import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint, User
from app.main import create_app, db, app

# app = create_app(os.getenv('MOOC_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@app.before_first_request
def create_user():
    user = User.query.filter_by(username='admin').first()
    if not user:
        new_user = User(
            username='admin',
            password='admin',
            name='admin',
            email='admin@localhost',
            avatar='',
            registered_on=datetime.datetime.utcnow(),
            roles=['system', 'manager', 'user']
        )
        db.session.add(new_user)
        db.session.commit()


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs unit tests."""
    tests = unittest.TestLoader().discover('app/text', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()


