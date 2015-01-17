.. title: Test Restructured test
.. slug: test-restructured-test
.. date: 2515-01-13 19:31:56 UTC-05:00
.. tags:
.. link:
.. description:
.. type: text

==============
Heading 1
==============

Getting started
=================

Trying to figure out how to get started with restructed text.

See the Python_ home page for info.

`Write to me`_ with your questions.

.. _Python: http://www.python.org
.. _Write to me: jdoe@example.com

So what happens with this paragraph?

.. code-block:: python
    :number-lines:

    # app/__init__.py
    from flask import Flask
    from flask.ext.sqlalchemy import SQLAlchemy
    from flask.ext.script import Manager
    from flask.ext.migrate import Migrate
    from config import CONFIG

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['DBURI']

    db = SQLAlchemy()
    db.app = app
    db.init_app(app)

    migrate = Migrate(app, db)
    manager = Manager(app)

    from app import models, views

That should be a colorized code block
