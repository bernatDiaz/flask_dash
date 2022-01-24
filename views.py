from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort

class AdminModelView(ModelView):

    def is_accessible(self):
        return getattr(current_user, 'admin', False)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        abort(401)