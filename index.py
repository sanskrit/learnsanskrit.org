import os
import sys

import production

activate_this = os.path.join(production.virtualenv_path, '/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
sys.path.append(production.htdocs_dir)

from lso import create_app
application = create_app(__name__, 'production')
