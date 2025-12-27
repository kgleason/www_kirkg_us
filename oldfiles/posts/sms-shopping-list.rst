.. title: SMS Shopping List, Part 1
.. slug: sms-shopping-list-part-1
.. date: 2014-06-28 21:54:58 UTC-05:00
.. tags: twilio, technology, python, programming,
.. link:
.. description:
.. type: text

The Problem
============

I have 3 kids. And a wife. We lead pretty hectic lives, and there doesn't seem
to be an end in sight to the insanity. Given all of that, it seems as if we
always have a list of stuff that we need from the grocery store.

More than once, I've been at the grocery store fulfilling the needs on the
pre-written list only to be bombarded with text messages asking for this and that.
Sometimes I get lucky and manage to get everything on the lists (the written
lists and all of the impromptu SMS lists). More often than not I end up overlooking
something because it isn't all in one place. Quite frankly it doesn't help that
I'm easily distracted in the grocery store.

There has to be a better way.

.. TEASER_END

The Solution
==============

Obviously, we need a centralized mobile list that is easy for everyone to add
to and access. Also, since everyone, myself excluded, prefers to communicate via
text message, it seems like I should probably use that.

Recently I've been playing around in Python. One day I stumbled across
Charles Leifer's post_ about writing a note taking app in Python with Flask.
I thought the idea was pretty brilliant, and it hit me that I could do something
like that to solve my shopping list problem.

.. _post: https://charlesleifer.com/blog/saturday-morning-hack-a-little-note-taking-app-with-flask/

The requirements, as I saw them:

* A centralized page to view the current list.
* Ability to add items to the list via SMS
* Ability to see who had added a specific item, and when

At work we use Twilio_ for web based telephony, so I
had a basic understanding of how it worked. I had already been through the
`Twilio python tutorials`_ and knew how to do some pretty basic stuff in Python
with Twilio. The tutorials even used Flask. So the plan was decided.

.. _Twilio: http://www.twilio.com
.. _`Twilio python tutorials`: https://www.twilio.com/docs/quickstart/python/sms/hello-monkey

The implementation
===================

Set up
~~~~~~~~

For the most part, I used `Twilio's documentation`_ about setting up the dev
environment. The gist of it was something like this:

.. _`Twilio's documentation`: https://www.twilio.com/docs/quickstart/python/devenvironment

- Install python and some tools:
   - ``brew installl python``
   - ``brew doctor``
   - Fix any changes from above
   - ``easy_install pip``
   - ``pip install virtualenv``
- Create a virtual environment for holding all of my stuff:
   - ``virtualenv --no-site-packages SMShoppingList``
   - ``cd SMShoppingList``
   - ``source bin/activate``
- Install the packages I need to get started
   - ``pip install Flask SQLAlchemy twilio Flask-Migrate Flask-Script WebHelpers``

The last thing I did was to set up git with a .gitignore file. Nothing magical
here -- just ``git init`` and then pull down the `sample python .gitignore file`_
from Github.

.. _`sample python .gitignore file`: https://github.com/github/gitignore/blob/master/Python.gitignore

Getting started
~~~~~~~~~~~~~~~~~

I started out with some basic stuff. First I made the directory structures that I needed
``mkdir -p app/static app/templates`` and then set up the init for the app:

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

Basic models:

.. code-block:: python
    :number-lines:

    # app/models.py
    from app import db

Basic views:

.. code-block:: python
    :number-lines:

    # app/views.py
    import os
    from flask import render_template, request
    from app import app

    @app.route('/')
    def index():
        return render_template('index.html')

A config file

.. code-block:: python
    :number-lines:

    # config.py
    CONFIG = { 'DBURI': 'sqlite:////Users/kirk/Projects/SMShoppingList/app.db.sqlite3' }

The last thing I wanted was a Django-style manage.py. I'm not sure why I do it
this way, to be honest. It works for me, so I just roll with it. Until I find a
better way ....

.. code-block:: python
    :number-lines:

    # manage.py
    from app import app, manager
    from flask.ext.migrate import MigrateCommand

    manager.add_command('db', MigrateCommand)

    app.debug = True
    manager.run()

Adding some style & pages
~~~~~~~~~~~~~~~~~~~~~~~~~~

Since I have practically 0 design skills, I decided from the beginning that I
would use `Twitter's Bootstrap`_ to just make a lot of that stuff work.
I downloaded the zip, and copied the dist/{css,js} into app/static.

.. _`Twitter's Bootstrap`: http://getbootstrap.com/

.. code-block:: bash
    :number-lines:

    cp -r ~/Downloads/bootsrap-3.1.1/dist/{css,js} app/static

With Bootstrap in place, I could start adding some basic pages. I started with a
basic HTML template to define the basic look of all of the pages of the site.

.. code-block:: html
    :number-lines:

    # app/templates/layout.html
    <!DOCTYPE html>
    <html>
        <head>
            <title>Shopping List</title>
            <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/bootstrap.min.css') }}\"/>
            <!--<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/custom.css') }}\"/>-->
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
            <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/bootstrap-responsive.min.css') }}\" rel=\"stylesheet\">
            <script type=\"text/javascript\" src=\"{{ url_for('static', filename='js/refresh.js') }}\"></script>
            <script type=\"text/javascript\" src=\"http://code.jquery.com/jquery.min.js\"></script>
            <script type=\"text/javascript\" src=\"{{ url_for('static', filename='js/bootstrap.min.js') }}\"></script>
        </head>
        <body>
            <div class=\"container\">
                <header>
                    <nav id=\"myNavbar\" class=\"navbar navbar-default navbar-inverse navbar-static-top\" role=\"navigation\">
                        <div class=\"container\">
                            <div class=\"navbar-header\">
                                <button type=\"button\" class=\"navbar-toggle\" data-toggle=\"collapse\" data-target=\"#navbarCollapse\">
                                    <span class=\"sr-only\">Toggle navigation</span>
                                    <span class=\"icon-bar\"></span>
                                    <span class=\"icon-bar\"></span>
                                    <span class=\"icon-bar\"></span>
                                </button>
                                <a class=\"navbar-brand\" href=\"{{ url_for('index') }}\">Shopping List</a>
                            </div>
                            <!-- Collect the nav links, forms, and other content for toggling -->
                            <div class=\"collapse navbar-collapse\" id=\"navbarCollapse\">
                                <ul class=\"nav navbar-nav\">
                                    <li><a href=\"{{ url_for('people') }}\">People</a></li>
                                    <li class=\"divider-vertical\"></li>
                                    <li><a href=\"{{ url_for('help') }}\">Help</a></li>
                                </ul>
                            </div>
                        </div>
                    </nav>
                </header>
                <div class=\"container\">
                    <div class=\"blog-header\">
                        <h1 class=\"blog-title\">Shopping List</h1>
                        <p class=\"lead blog-description\">Send an SMS so the shopping list number to add an item to the list</p>
                    </div>
                </div>
                {% block content %}

                {% endblock %}

                <div class=\"modal-footer\">
                    <h4>&copy; kirkg.us</h4>
                </div>
            </div>
        </body>
    </html>

I'm not going to go through this line by line. Suffice to say that this template
defines a horizontal nav bar that persists across all of the pages, and a
persistent header & footer.

Modelling it all out
~~~~~~~~~~~~~~~~~~~~~

With the basic site layout defined, it was time to get to some functionality. I
defined some models. From my requirements, I had 2 basic objects I was going to
need to deal with, a person and a list item.

Starting with a person, I knew that, at least at the beginning, I didn't want to
design a complicated authentication system. So with that, I really only needed
to know the persons name & mobile phone number. Here is what I ended up with.

.. code-block:: python
    :number-lines:

    # app/models.py Fragment
    class Person(db.Model):
        __tablename__ = 'person'
        id = db.Column(db.Integer, primary_key=True)
        firstname = db.Column(db.String(100))
        lastname = db.Column(db.String(100))
        mobile = db.Column(db.String(12), unique=True)

    @classmethod
    def all(cls):
        return Person.query.order_by(Person.lastname, Person.firstname).all()

    @classmethod
    def find_by_mobile(cls, mobile):
        return Person.query.filter(Person.mobile == mobile).first()

    @property
    def display_name(self):
        if self.firstname:
            return \"{0} {1}\".format(self.firstname, self.lastname)
        else:
            return self.mobile

The person class requires that a mobile phone number be unique. Since the
primary communication will be happening via SMS, duplicate mobile phone numbers
would be way too hard to deal with.

Aside from the basic class, I've added a couple of class methods. The ``all()``
class method will return a list of all of the people in the table. The
``find_by_mobile()`` is a shortcut way to find a person by their mobile number.

Lastly, I defined a class property (you may need to scroll down in the code window)
that is an easy way to get someone's name in the way I want to display it on the screen.

---------

Thinking about an item in the list, I wanted to know the following things about it:

* what is it
* who added it
* when was it added
* has it been purchased yet

Given that, I ended up with a model that looks like this:

.. code-block:: python
    :number-lines:

    class ListItem(db.Model):
        __tablename__ = 'list_item'
        id = db.Column(db.Integer, primary_key=True)
        list_item = db.Column(db.String(200))
        created = db.Column(db.DateTime, default = datetime.datetime.now)
        closed = db.Column(db.Boolean, default=False)
        created_by = db.Column(db.Integer, db.ForeignKey('person.id'))

    @property
    def creator(self):
        p = Person.query.filter(Person.id == self.created_by).first()
        return p.display_name

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)

    @classmethod
    def all(cls):
        return ListItem.query.order_by(desc(ListItem.id)).all()

    @classmethod
    def all_open(cls):
        return ListItem.query.filter(ListItem.closed == False).order_by(desc(ListItem.id)).all()

Again I created a couple of class methods and properties to make my life easier
down the road. They should all be pretty self explanatory. You can see the
complete file, including all of the Python imports on github_.

.. _github: https://github.com/kgleason/SMShoppingList/blob/5b057cbd9e68ab40b65969dfc3c4eca2d9114e54/app/models.py

Displaying the list
~~~~~~~~~~~~~~~~~~~~

Next I needed some HTML to display the list.

.. code-block:: html
    :number-lines:

    # app/templates/index.html
    {% extends 'layout.html' %}
    {% block content %}
        <h3>The List</h3>
        <hr/>
    {% if not my_list %}
        The list appears to be empty
    {% else %}
        <table class=\"table\">
            <thead>
                <tr>
                    <th></th>
                    <th>Item</th>
                    <th>Requested By</th>
                    <th>Added</th>
                </tr>
            </thead>
        <tbody>
    {% for i in my_list %}
            <tr>
                <td><input type=\"checkbox\" name=\"{{ i.id }}\" value=\"{{ i.purchased }}\"/></td>
                <td>{{ i.list_item }}</td>
                <td>{{ i.creator }}</td>
                <td>{{ i.created_in_words }} ago</td>
            </tr>
    {% endfor %}
        </tbody>
    </table>

    {% endif %}
    {% endblock %}

This jinja2 template will process a Python dictionary passed in that is called
``my_list``. It draws a table, and iterates over ``my_list`` for each row in the
table. The last thing I need for a basic test is a way to generate the list to pass in.

The views
~~~~~~~~~~~

I knew that I needed to define the index view, and I quickly learned that I
needed to define every view that I reference in the layout.html file.

.. code-block:: python
    :number-lines:

    # app/views.py
    import os
    from flask import render_template, request
    from app import app
    from models import ListItem

    @app.route('/')
    def index():
        return render_template('index.html', my_list=ListItem.all_open())

    # A place holder route until I build the people page.
    @app.route('/people')
    def people():
        return render_template('index.html')

    # A place holder router until I build the help page
    @app.route('/help')
    def help():
        return render_template('index.html')

For right now, the /people and /help pages will display an empty index page.
We'll get those pages fixed in a bit. The important bit in that file is the index route.
When the index.html template is rendered, it is passed in all of the open list items.

Testing
~~~~~~~~~

At this point, it seemed like a good time to test. If you've taken the time to
read this far, then I think it is only fair that I admit that I am writing this
post several months after I wrote the code. I've reconcstucted a lot of what I
did, and how I did it from my git commit logs, and my general memory of that day.
At this point, I think that you should be able to run this thing, but it will be
pretty lack luster. If you are entering in the code line by line, then the next
steps *may not work*. If that is the case, I do apologize up front.

Before we can fire the whole thing up, need to build the database. Because of
the way that I have the manage.py file set up, it should be accomplishable with
the following commands:

.. code-block:: bash
    :number-lines:

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py runserver -r -d

The first command (db init) will create a migrations folder, and create the
database file itself. You only need to run this command one time.

The second command (db migrate) will cause the models that are defined in the
models.py to be converted into database scripts. Since this is the first
migration, essentially what will happen is that the create scripts for the 2
tables will be created.

The 3rd command (db upgrade) will apply the scripted changes, which are sitting
in the newly minted migrations folder, to the actual database.

The final command (runserver) will cause the Flask web server to start up. The
`-r` flag will make it look for changes in the underlying Python files. If
changes are detected, then the Flask server will reload itself automatically.
The `-d` flag causes it to run in debug mode, which means that you will get
useful debugging output in the web browser when a non-fatal error is encoutnered.

At this point, if all went well, you should be able to open a web browser and
browse to `localhost:5000`_ and see the basic layout of the site. Of course, the
list is empty so there isn't much to see.


.. _`localhost:5000`: http://localhost:5000


Adding some items by hand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Without the SMS stuff set up, we need to resort to a couple of tricks to get
some data into the database so we can see what it looks like on the page. Go
ahead and fire up another terminal and ``cd`` into your project directory.
Activate the virtual environment with ``source bin/activate``. Once you are in
the virtual environment, you can get an interactive shell with ``python manage.py shell``.
The commands below will walk through getting some basic stuff set up inside your app.

.. code-block:: python
    :number-lines:

    # Import some bits from the app
    # The >>> are the shell indicator in Python. You do not need to type them in.
    >>> import app
    >>> from app.models import *
    >>> import config
    >>>

    # Start out by creating a person
    >>> p = Person(firstname='Kirk', lastname='Gleason', mobile='+18005551212')

    # You can verify your person object by calling them forth in Python:
    >>> p.firstname
    'Kirk'
    >>> p.mobile
    '+18005551212'
    >>>

    # In models.py, we defined an ID to each person. Is it there?
    >>> p.id
    >>>
    # Guess not yet ....

    # Let's save it to the database.
    # Note that the following 2 steps will add the person record to the database.
    # If you don't want this to happen, then you should probably skip these commands.
    >>> db.session.add(p)
    >>> db.session.commit()
    >>>

    # You can verify that it was written to the database by seeing if the ID was created, since it is the primary key in the database.
    >>> p.id
    1
    >>>

    # Now that there is a person, we can add something to the list and save it to the database
    >>> i = ListItem(list_item='Test Shopping List Item', created_by=p.id)
    >>> db.session.add(i)
    >>> db.session.commit()

If you want, you can close out of the shell with Ctrl-D. Or you can leave it
open to continue adding items. First a couple of comments on what we just did.

We started by defining a person, and saving it in the database. We needed to create
the person first since the ListItem class requires a person for the 'created_by' field.

You may have noticed some special formatting on the phone number. If you
don't work with telephony very much, then it will look strange. That format however
is a pretty standard way to represent phone numbers in the world. This is the
format that Twilio uses and it is the format that I've chosen to stick with.
You can make it work differently, but you will need to make some changes in the
next article, when the Twilio bits are implemented. Twilio expects this format,
so I recommend that you save yourself the headache and implement it now. If you
did it incorrectly, and you have't yet closed your shell, then you can fix it
with ``p.mobile = '+1XXXXXXXXXX'`` and then ``db.session.add(p)`` and
``db.session.commit()`` to write the changes.

But the cool part is that if you refresh the page in your broswer, you will see
the newly added list item.

In the next installment, I'll walk through wrapping it all up. I'll cover adding
in the SMS functionalty, creating the People & Help pages, and adding in some
jquery to remove items from the list when you tick the box. Since I had some
challenges deploying this to a production environment, I'll aslo walk through how
I deployed everything, and then what I forsee the future bringing for this app.
