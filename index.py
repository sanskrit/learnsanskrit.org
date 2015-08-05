import os
import sys

sys.path.append(os.path.dirname(__file__))
import production

activate_this = os.path.join(production.virtualenv_path, 'bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from lso import create_app
application = create_app(__name__, 'production')
