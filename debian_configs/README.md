# Debian Configs
I had initially planned on deploying this Django site on Heroku. But in the end Heroku was going to be cost prohibitive, so I opted for Digital Ocean. But man, was it more difficult that Heroku was.

This folder has all of the things I ended up doing to get the site up and runnung on Debian 11 in Digital Ocean.

I ran these commands to kind of get started:

   ```bash
   # Make a place to store Django static files
   sudo mkdir /opt/django
   chmod kirk:www-data /opt/django
   ```

## High level process:

   1. Install postgres, nginx, and certbot (for LetsEncrypt)
   1. Follow the Digital Ocean docs to set up Lets Encrypt for Nginx
   1. Create a user in postgres to house the database
   1. Create a database for the site
   1. Grant permissions on the database to the new user
   1. On the server, generate an ssh key for the user who will run the Django site.
   1. On githib, add the public key as a deployment key in the repository
   1. Create repo secrets in guthub:
      * SSH_HOST: The name of the server (or IP address)
      * SSH_USERNAME: The name of the user who will run the django app
      * SSH_KEY: The secret key that was generated above
   1. On the server put the public key into `~/.ssh/authorized_keys` if it isn't allready there
   1. Clone the repository.
   1. `cd` into the new directory
   1. `pip -mvenv .venv`
   1. `source .venv/bin/activate`
   1. `pip install -r requirements.txt`
   1. `export DJANGO_SETTINGS_MODULE=blogsite.settings.prod`
   1. `python manage.py createsuperuser` and follow the prompts to make the django admin user.
   1. `python manage.py migrate`
   1. `python manage.py collectstatic` # This step will be done by the github automation after this, but for the first time, it'll need to be run manually.
   1. `cd` into the `blogsite/settings` directory
   1. create a file named .env and in Python style, add the following values. Use a long random string for the value of the `SECRET_KEY`:
      * SECRET_KEY=
      * DATABASE_NAME=
      * DATABASE_USER=
      * DATABASE_PASS=
   1. `sudo ln -s /etc/nginx/sites-available/kirkg.us.conf /etc/nginx/sites-enabled/`
   1. `sudo rm -f /etc/nginx/sites-enabled/default`

Things should be all set now. Start nginx, and then enable the gunicorn socket with systemctl. 