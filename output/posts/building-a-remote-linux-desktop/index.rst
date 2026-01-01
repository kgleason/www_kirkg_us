.. title: Building a Remote Linux Desktop
.. slug: building-a-remote-linux-desktop
.. date: 2015-01-29 19:31:57 UTC-05:00
.. tags: linux, digital-ocean, x2go, ubuntu-mate, technology
.. link: 
.. description: .. _Digital Ocean: https://www.digitalocean.com/?refcode=18b80ab28634

.. type: text

Step 1: Build the server
~~~~~~~~~~~~~~~~~~~~~~~~~

The other day, for giggles, I decided to see if I could convert a virtual private server (VPS) into a desktop and access it remotely. Seems to have worked, so I've decided to do it again, in case anyone else ever wanted to. At the end of this, you'll have a server at `Digital Ocean`_ running `Ubuntu MATE`_ that you can access from almost any platform with X2Go_.

.. _Digital Ocean: https://www.digitalocean.com/?refcode=18b80ab28634
.. _Ubuntu MATE: https://www.ubuntu-mate.org
.. _X2Go: http://wiki.x2go.org

Start out by going to `Digital Ocean`_ and spinning up a new droplet. I chose Ubuntu 14.04 x64, but it shouldn't bee too much work to get this working with Ubuntu 14.10. Wait your requisite 57 seconds (mine only took 44 seconds!!), and connect to the machine. While completely optional, `Digital Ocean`_ has some `great recommendations`_ with what to do `after you build your droplet`_. At the very least, configure yourself a firewall, leaving port 22 (or whatever port you choose) open. Our remote desktop will only need SSH to connect. It's probably also a good idea to run some updates: 

.. _Digital Ocean: https://www.digitalocean.com/?refcode=18b80ab28634
.. _great recommendations: https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-14-04
.. _after you build your droplet: https://www.digitalocean.com/community/tutorials/additional-recommended-steps-for-new-ubuntu-14-04-servers

.. code-block:: bash

	apt-get update
	apt-get upgrade
	apt-get dist-upgrade
	shutdown -r now

.. TEASER_END

Step 2: A server no more
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming that you followed all of those steps up there, you now have a pretty good server built up. Now it is time to make it not a server. I'm certain that there are a bunch of ways to accomplish this, but I like to try to keep it simple. Start by running ```tasksel```. Unselect everything except for **openssh-server**. Wait a couple of seconds for the process to complete. Once that is done, you can install Ubuntu MATE as follows:

.. code-block:: bash

	sudo apt-add-repository ppa:ubuntu-mate-dev/ppa
	sudo apt-add-repository ppa:ubuntu-mate-dev/trusty-mate
	sudo apt-get update && apt-get upgrade
	sudo apt-get install ubuntu-mate-core ubuntu-mate-desktop

That will take a few minutes to complete. Grab yourself a drink.

Step 3: Remote access
~~~~~~~~~~~~~~~~~~~~~~

You've now got a respectable little machine up and running with the new hotness in lightweight desktop environments. But no way to access it. Let's fix that.

.. code-block:: bash

	sudo add-apt-repository ppa:x2go/stable
	sudo apt-get update
	sudo apt-get install x2goserver x2goserver-xsession

Your shiny new x2go server is now installed and running.

Step 4: Connecting
~~~~~~~~~~~~~~~~~~~~~~

At this point you'll need to install an X2Go client on your local machine. I'll leave that to you. Once you have it installed, you can configure your client according to the screenshot below.

|

.. image:: /images/X2GoClientConfig.png
	:alt: X2Go Client Configuration Screen
	:align: center

|

You can name the connection however you see fit. The value of the *host* field should be the IP of your `Digital Ocean`_ VPS, or a name that you have configured in DNS. The *login* will be the name of the user that you created -- in the name of all things holy and sacred, please don't use root to connect! The *SSH port* should be whatever you configured it to be. If you set up public key authentication for SSH, then you can check the *Try auto login (ssh-agent or default ssh key)* option. Lastly, make sure that you set the *Session type* to MATE.

.. _Digital Ocean: https://www.digitalocean.com/?refcode=18b80ab28634

There are some interesting bits in the *Connection* tab. 

|

.. image:: /images/X2GoConnectionConfig.png
	:alt: X2Go Connection Configuration Screen
	:align: center

|

You can use the stuff in here to tweak your connection settings. Personally, I find the defaults to be perfectly ussable, but it is nice to have the options if you ever find yourself with an abysmal connection.

Some words of warning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I've only played with this minimally. Your mileage may vary. I'm not responsible if you lose all of your data, or if your cloud desktop gets hacked, cracked, compromised, infected, stolen, etc. In short, I did this cause I was bored and curious. Do with it what you will. If you have questions, feel free to email me, or find me on twitter. If you have complaints, type them all into a file called ``ComplaintsForKirk.txt`` and run this command:

.. code-block:: bash

	cat ComplaintsForKirk.txt > /dev/null

I swear that I'll respond to them as soon as I get them.