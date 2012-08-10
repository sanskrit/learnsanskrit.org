#!/bin/bash
# create_blueprint.sh

APP=$1
BLUEPRINT=$2

SCRIPT_DIR=$(dirname $0)
PROJECT_DIR=$(dirname $SCRIPT_DIR)
cd $PROJECT_DIR

## Folders
mkdir $APP/$BLUEPRINT && cd $_
mkdir static templates templates/$BLUEPRINT

## Files

# __init__
cat << EOF > __init__.py
from flask import Blueprint

$BLUEPRINT = Blueprint('$BLUEPRINT', __name__, static_folder='static', template_folder='templates')

import views
EOF

# Filters
: > filters.py

# Forms
: > forms.py

# Models
cat << EOF > models.py
from ..database import engine, session
EOF

# Views
cat << EOF > views.py
from flask import render_template

from . import $BLUEPRINT
EOF
