mkdir $1/$2
cd $1/$2
: > __init__.py
: > filters.py
: > forms.py
: > models.py
: > views.py
mkdir static templates
cd templates
mkdir $2
