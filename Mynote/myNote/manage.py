from app import create_app
import os
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
from app.extensions import db
from app.models import User, Posts,  Category

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Posts,Category=Category)

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
