import os

from flask import flash, redirect
from flask.ext.admin import Admin, BaseView, AdminIndexView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.security import current_user
from werkzeug import secure_filename
from wtforms import FileField, Form, validators

import lso.texts
import lso.texts.models
from .database import db


class UploadForm(Form):
    path = FileField("XML Document", [validators.Required()])


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
            lso.texts.lib.process_text_xml(filename)
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

admin.add_view(TextView(lso.texts.models.Text, db.session,
                        category='Collection',
                        name='Texts',
                        url='texts/manage'))

admin.add_view(LSOModelView(lso.texts.models.Author, db.session,
                            category='Collection',
                            name='Authors',
                            url='texts/authors'))

admin.add_view(LSOModelView(lso.texts.models.Segment, db.session,
                            category='Collection',
                            name='Segments',
                            url='texts/segments'))

admin.add_view(LSOModelView(lso.texts.models.Division, db.session,
                            category='Collection',
                            name='Divisions',
                            url='texts/divisions'))
