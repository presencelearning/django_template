{% if False %}
django_template
==============================

This is a django template, to use it you can do something like:
::
    django-admin startproject --template <path_to_project> --extension=py,rst,yml <project_name>
    or
    django-admin startproject --template https://github.com/presencelearning/django_template/zipball/master --extension=py,rst,yml test_project

{% endif %}
Getting up and running
----------------------

Basics
^^^^^^

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* python3
* python3-dev
* pip3
* virtualenv or pyvenv
* MySQL

First open a terminal and make sure to create and activate a virtualenv_::

    $ cd {{ project_name }}
    $ virtualenv -p `which python3` .virtualenv
    $ source .virtualenv/bin/activate

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Then install the requirements for local development::

    $ pip install -r requirements/local.txt


Connect to mysql::

    $ mysql -u root -p

If you don't already have a user, create one::

    > CREATE USER 'learning'@'localhost' IDENTIFIED BY 'learning';
    > GRANT ALL PRIVILEGES ON * . * TO 'learning'@'localhost';
    > FLUSH PRIVILEGES;

Create a local MySQL database::

    $ CREATE DATABASE {{ project_name }} CHARACTER SET utf8 COLLATE utf8_general_ci;

Run ``migrate`` on your new database::

    $ python manage.py migrate

You can now run the ``runserver_plus`` command::

    $ python manage.py runserver_plus

Open up your browser to http://127.0.0.1:8000/ to see the site running locally.

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

To create an **superuser account**, use this command::

    $ python manage.py createsuperuser


Settings
------------

See config/settings/common.py for default settings and https://django-environ.readthedocs.org/en/latest/ for the format of the main ones.


Documentation
-------------

To initialize the sphinx documentation::

    $ sphinx-quickstart --project="{{ project_name }}" --author="PresenceLearning" -v 0.1 -r 0.1 -l en --makefile -q docs


Celery
^^^^^^
This app comes with Celery but it runs in eager mode by default (executes tasks directly without sending them to a broker).

To run a celery worker:

.. code-block:: bash

    celery -A {{ project_name }}.taskapp worker -l info

Please note: For Celerys import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.


Registering your app on test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you don't use the default port or host, you will need to register a new client on Auth (on test) to be able to login. Here is an example if you run on port 9000::

    ./manage.py create_client --name=localhost9000 --id=localhost9000 --secret=<yoursecret> --rooturl="http://localhost:9000" --redirecturl="http://localhost:9000/oidc/callback/" --logouturl="http://localhost:9000/logout/""
