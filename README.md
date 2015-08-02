learnsanskrit.org
=================

This is the source code for [learnsanskrit.org](http://learnsanskrit.org).


Building learnsanskrit.org
--------------------------


1. Install necessary packages. If you use Ubuntu, you can use this script:

        sudo ./bin/install-ubuntu-packages.sh

   If you're not using Ubuntu, you can examine
   `./bin/install-ubuntu-packages.sh` to see which packages are required.

2. Install necessary Python packages:

        sudo pip install virtualenv
        virtualenv env && source env/bin/activate
        pip install -r requirements.txt

3. Create Postgres database:

        sudo service postgres start
        sudo -u postgres createuser $USER
        createdb -u $USER learnsanskrit

4. Initialize the database:

        from lso import create_app
        app = create_app(__name__)

        # Run this for all blueprints
        from <blueprint> import setup
        setup.create(app)
        setup.seed(app)

5. Run on localhost:

        python runserver.py

6. Whenever you're done, kill the server and exit the virtualenv:

        deactivate


Testing learnsanskrit.org
-------------------------

    py.test test/*.py


Components
----------

- grammar guide
- dictionary
- assorted tools (transliterator, meter recognizer)
- "reading environment" with texts, translations, commentaries, and other data
