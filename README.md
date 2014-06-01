learnsanskrit.org
=================

This is the source code for [learnsanskrit.org](http://learnsanskrit.org),
a website with resources for learning and processing Sanskrit. The site is
built with [Flask](flask.pocoo.org/) and uses too many Python and JavaScript
libraries to comfortably list here.

All contributions are welcome!

Building learnsanskrit.org
--------------------------

**NOTE**: These instructions assume an Ubuntu system.

1. Install necessary packages:

        sudo ./bin/install-ubuntu-packages.sh

2. Install necessary Python packages:

        sudo pip install virtualenv
        virtualenv env && source env/bin/activate
        pip install -r requirements.txt

3. Create Postgres database:

        sudo service postgres start
        sudo -u postgres createuser $USER
        createdb -u $USER learnsanskrit

4. Initialize the database:

    TODO

5. Run on localhost:

        fab serve

6. Whenever you're done, kill the server and exit the virtualenv:

        deactivate
