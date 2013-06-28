import os

from flask import redirect
from flask.ext.admin import Admin, BaseView, AdminIndexView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.security import current_user
from flask.ext.wtf import Form
from werkzeug import secure_filename
from wtforms import FileField

import database
import texts.models
import texts.lib


class UploadForm(Form):
    path = FileField("XML Document")


class AuthMixin(object):

    def is_accessible(self):
        return current_user.has_role('admin')


class LSOView(AuthMixin, BaseView):
    pass


class LSOModelView(AuthMixin, ModelView):
    pass


class LSOIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.has_role('admin'):
            return self.render(self._template)
        else:
            return redirect('/')


class TextUploadView(LSOView):

    """
    View for uploading XML documents to the library.
    """

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = UploadForm()
        print form.path.__dict__
        if form.validate_on_submit():
            data = form.path.data
            filename = secure_filename(data.filename)
            filename = os.path.join(app.config['UPLOAD_DIR'], filename)
            data.save(filename)
            success = True
            texts.lib.process_text_xml(filename)
        else:
            filename = None
            success = False
        return self.render('admin/texts/upload.html', form=form,
                           success=success)


class TextView(LSOModelView):
    column_exclude_list = form_excluded_columns = ('division',)
    column_labels = {'xmlid_prefix': 'XML ID prefix'}



admin = Admin(name='learnsanskrit.org', index_view=LSOIndexView())

admin.add_view(TextUploadView(
               category='Collection',
               name='Upload',
               url='texts/upload'))

admin.add_view(TextView(texts.models.Text, database.session,
                        category='Collection',
                        name='Texts',
                        url='texts/manage'))

admin.add_view(LSOModelView(texts.models.Author, database.session,
                         category='Collection',
                         name='Authors',
                         url='texts/authors'))

admin.add_view(LSOModelView(texts.models.Segment, database.session,
                         category='Collection',
                         name='Segments',
                         url='texts/segments'))

admin.add_view(LSOModelView(texts.models.Division, database.session,
                         category='Collection',
                         name='Divisions',
                         url='texts/divisions'))

# Attach to app
# -------------
from lso import app
admin.init_app(app)
