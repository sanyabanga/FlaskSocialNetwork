from flask import Flask, redirect, request, url_for

from flask_security.core import Security
from sqlalchemy.orm import session
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand, current, migrate
from flask_script import Manager

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemySessionUserDatastore, Security, current_user


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


### ADMIN ###
from models import *

class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass

class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']

class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'posts']


admin = Admin(app, 'FlaskBlog', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))


### Flask-Security ###
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)