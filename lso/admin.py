import os

from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.wtf import Form
from werkzeug import secure_filename
from wtforms import FileField

import database
import texts.models
import texts.lib

admin = Admin(name='learnsanskrit.org')


class UploadForm(Form):
    path = FileField("XML Document")


class LSOView(BaseView):

    """`BaseView` with authentication"""

    def is_accessible(self):
        # TODO: auth
        return True


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


class TextView(ModelView):
    column_exclude_list = form_excluded_columns = ('division',)
    column_labels = {'xmlid_prefix': 'XML ID prefix'}


admin.add_view(TextUploadView(
               category='Texts',
               name='Upload',
               url='texts/upload'))

admin.add_view(TextView(texts.models.Text, database.session,
                        category='Texts',
                        name='Manage',
                        url='texts/manage'))

admin.add_view(ModelView(texts.models.Segment, database.session,
                         category='Texts',
                         name='Segments',
                         url='texts/segments'))

admin.add_view(ModelView(texts.models.Division, database.session,
                         category='Texts',
                         name='_Divisions',
                         url='texts/divisions'))

# Attach to app
# -------------
from lso import app
admin.init_app(app)
