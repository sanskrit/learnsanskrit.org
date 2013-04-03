from lso.lib import LSOBlueprint

guide = LSOBlueprint('guide', __name__,
                     static_folder='static',
                     template_folder='templates')

import views
