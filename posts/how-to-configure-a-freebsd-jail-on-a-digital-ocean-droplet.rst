.. title: How to configure a FreeBSD Jail on a Digital Ocean Droplet
.. slug: how-to-configure-a-freebsd-jail-on-a-digital-ocean-droplet
.. date: 2015-02-21 20:55:57 UTC-05:00
.. tags: digital-ocean,freebsd,pf,jails,nginx,technology
.. category: How-To
.. link:
.. description:
.. type: text

One of the great things about FreeBSD is its long standing support for jails_.
A jail is a way to run a process or set of process in an environment that is
isolated from the host system. Processes created inside a jail cannot access files
outside of that jail.

.. _jails: http://www.freebsd.org/doc/handbook/jails.html

Over the course of this article, you will take a newly minted FreeBSD Droplet, do
some initial configuration, set up a jail, and install a simple web server
inside the jail.

In the end, you will be setting up a firewall to protect the host system. This
tutorial will be using the PF_ firewall that is included in FreeBSD. Aside from
configuring a firewall, you will also be making some tweaks to the default shell
as well as making some changes to the configuration of some of the default services.

.. _PF: http://www.freebsd.org/doc/handbook/firewalls-pf.html

.. TEASER_END

The default editor and shell prompt
=====================================

By default, FreeBSD uses *tcsh* as it's default shell, and *vi* as the default
editor. Both are pretty spartan, so in this optional section, you'll be updating
the shell prompt and the default editor. Since you'll probably want a better
editor in order to fix the shell prompt, we'll start with the editor.


A better editor
-----------------

The following command will install a version of *vim* that does not require X11.
Since it is the first time that the *pkg* command has been run, it is going to
do some initial setup & checks. If you've run *pkg* before, then your output may
look different.

|

.. code-block:: text

    > sudo pkg install vim-lite
    Updating FreeBSD repository catalogue...
    Fetching meta.txz: 100%   944 B   0.9k/s    00:01
    Fetching packagesite.txz: 100%    5 MB   1.8M/s    00:03
    Processing entries: 100%
    FreeBSD repository update completed. 23992 packages processed
    New version of pkg detected; it needs to be installed first.
    The following 1 packages will be affected (of 0 checked):

    Installed packages to be UPGRADED:
        pkg: 1.4.4 -> 1.4.12

    The process will require 23 KB more space.
    2 MB to be downloaded.

    Proceed with this action? [y/N]: y
    Fetching pkg-1.4.12.txz: 100%    2 MB   1.2M/s    00:02
    Checking integrity... done (0 conflicting)
    [1/1] Upgrading pkg from 1.4.4 to 1.4.12...
    [1/1] Extracting pkg-1.4.12: 100%
    Message for pkg-1.4.12:
     If you are upgrading from the old package format, first run:

      # pkg2ng
    Updating FreeBSD repository catalogue...
    FreeBSD repository is up-to-date.
    All repositories are up-to-date.
    The following 1 packages will be affected (of 0 checked):

    New packages to be INSTALLED:
        vim-lite: 7.4.591

    The process will require 20 MiB more space.
    5 MiB to be downloaded.

    Proceed with this action? [y/N]: y
    Fetching vim-lite-7.4.591.txz: 100%    5 MiB   1.6MB/s    00:03
    Checking integrity... done (0 conflicting)
    [1/1] Installing vim-lite-7.4.591...
    [1/1] Extracting vim-lite-7.4.591: 100%

|

In order to get tcsh to see the newly installed package, you'll need to rehash
the path:

|

.. code-block:: bash

    rehash

|

The rehash command should exit with no output.

A more helpful shell prompt
------------------------------

FreeBSD include a sample csh configuration file that is an excellent starting
off point. You'll need to grab a copy of it in order to get started:

|

.. code-block:: bash

    cp /usr/share/skel/dot.cshrc ~/.cshrc

|

Even though the default shell is tcsh, it will read ~/.cshrc, since tcsh inherits
a lot from the csh shell. Go ahead and open this file for editing:

|

.. code-block:: bash

    vim ~/.cshrc

|

You'll probably want to change a couple of the defaults in this file. The default
editor is set to *vi* and the default pager is set to *more*. Go ahead and change
these to *vim* and *less* respectively. In order to do this, change

|

.. code-block:: text

    . . .

    setenv  EDITOR  vi
    setenv  PAGER   more

    . . .

|

to

|

.. code-block:: text

    . . .

    setenv  EDITOR  vim
    setenv  PAGER   less

    . . .

|

You may not have noticed, but some of your keys may not work as expect -- Delete
is a great example. If you add the following chunk of code to the end of the file,
that problem will be fixed. This code will check the terminal type that is connected
and, if the terminal type is one that is expect, it will fix the whacky key bindings:

|

.. code-block:: bash

    if ($term == "xterm" || $term == "vt100" \
                || $term == "vt102" || $term !~ "con*") then
              # bind keypad keys for console, vt100, vt102, xterm
              bindkey "\e[1~" beginning-of-line  # Home
              bindkey "\e[7~" beginning-of-line  # Home rxvt
              bindkey "\e[2~" overwrite-mode     # Ins
              bindkey "\e[3~" delete-char        # Delete
              bindkey "\e[4~" end-of-line        # End
              bindkey "\e[8~" end-of-line        # End rxvt
    endif

|

After the file has been saved, you can exit, you can make your shell read the new configuration
with:

|

.. code-block:: text

    source ~/.cshrc

|

Your prompt should change immediately:

|

.. code-block:: text

    freebsd@hostname:~ %

|

Time and Time Zones
=====================

Time Zone
----------

While not entirely necessary, keeping the time on your server correct is a
recommended best practice. Start by setting the timezone of our server:

|

.. code-block:: bash

    sudo tzsetup

|

Right off the bat, you should be prompted about the hardware clock on your machine:

|

.. image:: /images/FreeBSD_tzsetup.png
    :align: center

|

You should choose "No" to set your clock to local time. Next you will be asked
to identify where in the world your server is located:

|

.. image:: /images/FreeBSD_regions.png
    :align: center

|

Next you'll need to be more specific about your region:

|

.. image:: /images/FreeBSD_subregions.png
    :align: center

|

Finally, you'll be asked to choose a timezone:

|

.. image:: /images/FreeBSD_TimeZones.png
    :align: center

|

NTP for accurate time keeping
--------------------------------

With the time zone all configured, it's a good idea to configure NTP to keep the
time accurate. FreeBSD comes by default with an implementation of the ISC NTP
client, but for this tutorial, we'll be using OpenNTPD_ in order to keep the configuration
as simple as possible:

.. _OpenNTPD: http://openntpd.org

|

.. code-block:: text

    > sudo pkg install openntpd
    Updating FreeBSD repository catalogue...
    FreeBSD repository is up-to-date.
    All repositories are up-to-date.
    The following 1 packages will be affected (of 0 checked):

    New packages to be INSTALLED:
    openntpd: 5.7p3,2

    The process will require 79 KiB more space.
    36 KiB to be downloaded.

    Proceed with this action? [y/N]: y
    Fetching openntpd-5.7p3,2.txz: 100%   36 KiB  37.4kB/s    00:01
    Checking integrity... done (0 conflicting)
    [1/1] Installing openntpd-5.7p3,2...
    ===> Creating users and/or groups.
    Creating group '_ntp' with gid '123'.
    Creating user '_ntp' with uid '123'.
    [1/1] Extracting openntpd-5.7p3,2: 100%

|

You can make OpenNTPD start by default, and start the service manually with the
following commands:

|

.. code-block:: bash

    sudo sh -c 'echo "openntpd_enable=\"YES\"" >> /etc/rc.conf'
    sudo service openntpd start

|

By default, the OpenNTPD service will not listen for time requests, and will use
the Tier-2 servers from `ntp.org`_ for keeping accurate time. If you want to use
a different time server for synchronization, or use OpenNTPD as a time server,
please see */usr/local/etc/ntpd.org*.

.. _ntp.org: http://www.ntp.org

Adding a jail
==============

There are multiple ways to manage your jails, but ezjail_ is one of the more
popular ones, probably beacuse it is just so EZ. You can install it from a
binary package:

.. _ezjail: http://erdgeist.org/arts/software/ezjail/

|

.. code-block:: bash

    sudo pkg install ezjail

|

Ezjail works by creating a base jail, and then using that base as the model for
all subsequent jails. Set up the base jail:

|

.. code-block:: bash

    sudo ezjail-admin install -p

|

The -p flag should cause ezjail to include the FreeBSD ports tee in the base jail.

Setting up the network
------------------------

Before the jail can be started, you'll need to do some network configuration.

Virtual Interface
++++++++++++++++++++

Add the following to */etc/rc.conf*:

|

.. code-block:: text

    # Setup the interface that all jails will use
    cloned_interfaces="lo1"
    ifconfig_lo1="inet 172.16.1.1 netmask 255.255.255.0"

    # Future jails can use the following as a template.
    # Be sure to use 255.255.255.255 as the netmask for all interface aliases
    # ifconfig_lo1_alias0="inet 172.16.1.2 netmask 255.255.255.255"

    # Enable port forwarding and packet filtering
    pf_enable="YES"

    # Enable EZJail at startup
    ezjail_enable="YES"

|

To get the interface set up without a reboot, you can use the following commands:

|

.. code-block:: bash

    sudo ifconfig lo1 create
    sudo ifconfig lo1 inet 172.16.1.1 netmask 255.255.255.0

|

An *ifconfig* should now show a new interface:

|

.. code-block:: text

    lo1: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384
        options=600003<RXCSUM,TXCSUM,RXCSUM_IPV6,TXCSUM_IPV6>
        inet 172.16.1.1 netmask 0xffffff00
        nd6 options=29<PERFORMNUD,IFDISABLED,AUTO_LINKLOCAL>

|

NAT for packet forwarding
+++++++++++++++++++++++++++

Now that you have an interface to use with your jails, you'll need to get some
packet forwarding set up. Edit /etc/pf.conf (which will be empty by default)
according to the following

|

.. code-block:: text

    #Define the interfaces
    ext_if = "vtnet0"
    int_if = "lo1"
    jail_net = $int_if:network

    #Define the NAT for the jails
    nat on $ext_if from $jail_net to any -> ($ext_if)

|

The first 3 lines define a couple of useful variables. The *nat* line instructs
PF to mask outbound traffic from the jails (all of them) behind the IP address
of the external interface. In short, all of your outbound jail traffic will come
from the IP address of your droplet.

With that in place, you can start PF:

|

.. code-block:: bash

    sudo service pf start

|

Before you load the firewall ruleset, test the config file to ensure that all is
well:

|

.. code-block:: text

    freebsd@bsdsrv01:~ % sudo pfctl -nvf /etc/pf.conf
    ext_if = "vtnet0"
    int_if = "lo1"
    jail_net = "lo1:network"
    nat on vtnet0 inet from 172.16.1.0/24 to any -> (vtnet0) round-robin

|

Your output should look very similar to what is above. If not, the *pf* should tell
you what line has the error. Once you are getting output that inidicates no errors
you can turn on the NAT:

|

.. code-block:: bash

    sudo pfctl -f /etc/pf.conf

|

Creating the first jail
=========================

It's time to create & start a jail:

|

.. code-block:: bash

    sudo ezjail-admin create WEBSERVER 172.16.1.1
    sudo ezjail-admin start WEBSERVER

|

Those commands will have a lot of output, and may end with a warning. You can
safely ignore the warnings. The jail needs to be told how to do DNS lookups. The
simple way to solve this is to copy the hosts */etc/resolv.conf* into the jail:

|

.. code-block:: bash

    sudo cp /etc/resolv.conf /usr/jails/WEBSERVER/etc/

|

Go ahead and jump into the console of our jail:

|

.. code-block:: bash

    sudo ezjail-admin console WEBSERVER

|

There will be a lot of stuff on the console -- very similar to what you should
have seen when you first connected to your Droplet.

|

.. code-block:: text

    freebsd@bsdsrv01:~ % sudo ezjail-admin console WEBSERVER
    FreeBSD 10.1-RELEASE (GENERIC) #0 r274401: Tue Nov 11 21:02:49 UTC 2014

    Welcome to FreeBSD!

    Release Notes, Errata: https://www.FreeBSD.org/releases/
    Security Advisories:   https://www.FreeBSD.org/security/
    FreeBSD Handbook:      https://www.FreeBSD.org/handbook/
    FreeBSD FAQ:           https://www.FreeBSD.org/faq/
    Questions List: https://lists.FreeBSD.org/mailman/listinfo/freebsd-questions/
    FreeBSD Forums:        https://forums.FreeBSD.org/

    Documents installed with the system are in the /usr/local/share/doc/freebsd/
    directory, or can be installed later with:  pkg install en-freebsd-doc
    For other languages, replace "en" with a language code like de or fr.

    Show the version of FreeBSD installed:  freebsd-version ; uname -a
    Please include that output and any error messages when posting questions.
    Introduction to manual pages:  man man
    FreeBSD directory layout:      man hier

    Edit /etc/motd to change this login announcement.
    root@WEBSERVER:~ #

|

Notice that your prompt has changed. Congratulations, you are inside your jail!
It's probably a good idea to test your connectivity to the outside world, but
by default, and for security reasons, FreeBSD jails are not allowed to ping. To
test connectivity, you can use telnet:

|

.. code-block:: text

    root@WEBSERVER:~ # telnet www.digitalocean.com 80
    Trying 104.16.25.4...
    Connected to www.digitalocean.com.
    Escape character is '^]'.

|

What that command did was to open up a very basic connection to a webserver at
Digital Ocean. Pressing Control-] closes the connection, and *quit* exits telnet.

Installing a webserver
-------------------------

With a jail up and connected to the internet, you can go ahead and install a
webserver. You should be inside of your jail for this (remember that you can use
*sudo ezjail-admin console WEBSERVER* to get into your jail):

|

.. code-block:: bash

    pkg install nginx

|

Since *pkg* has not yet been run in your jail, you'll be prompted to install it
and let it configure itself. The you will be prompted about installing the webserver:

|

.. code-block:: text

    root@WEBSERVER:~ # pkg install nginx
    The package management tool is not yet installed on your system.
    Do you want to fetch and install it now? [y/N]: y
    Bootstrapping pkg from pkg+http://pkg.FreeBSD.org/freebsd:10:x86:64/latest, please wait...
    Verifying signature with trusted certificate pkg.freebsd.org.2013102301... done
    [WEBSERVER] Installing pkg-1.4.12...
    [WEBSERVER] Extracting pkg-1.4.12: 100%
    Message for pkg-1.4.12:
     If you are upgrading from the old package format, first run:

      # pkg2ng
    Updating FreeBSD repository catalogue...
    [WEBSERVER] Fetching meta.txz: 100%    944 B   0.9kB/s    00:01
    [WEBSERVER] Fetching packagesite.txz: 100%    5 MiB   1.8MB/s    00:03
    Processing entries: 100%
    FreeBSD repository update completed. 23992 packages processed
    Updating database digests format: 100%
    The following 2 packages will be affected (of 0 checked):

    New packages to be INSTALLED:
        nginx: 1.6.2_1,2
        pcre: 8.35_2

    The process will require 6 MiB more space.
    1 MiB to be downloaded.

    Proceed with this action? [y/N]:

|

When you say "Yes", pkg will finish the installation of nginx. Next set nginx to
start when the jail starts, and start it immediately:

|

.. code-block:: bash

    echo 'nginx_enable="YES"' > /etc/rc.conf.d/nginx
    service nginx start

|

Redirecting the web traffic to the webserver
----------------------------------------------

Your web server should now be running, but you can't access it quite yet. Issue an
*exit* command inside your jail to get back to your host system. Make a couple
of edits to /etc/pf.conf to make it look like this:

|

.. code-block:: text

    # Define the interfaces
    ext_if = "vtnet0"
    int_if = "lo1"
    jail_net = $int_if:network

    # Define the IP address of jails
    # as well as ports to be allowed redirected
    WEBSERVER = "172.16.1.1"
    WEBSERVER_TCP_PORTS = "{ 80, 443 }"

    # Define the NAT for the jails
    nat on $ext_if from $jail_net to any -> ($ext_if)

    # Redirect traffic on ports 80 and 443 to the webserver jail
    rdr pass on $ext_if inet proto tcp to port $WEBSERVER_TCP_PORTS -> $WEBSERVER

|

A quick *sudo pfctl -nf /etc/pf.conf* should return nothing, indicating that
there are no syntax errors. You can flush the current rules and reload them:

|

.. code-block:: text

    sudo pfctl -F all -f /etc/pf.conf

|

To be perfectly clear, that command will flush all of the existing tables and
load up the new rules.

At this point, you should be able to browse to the IP of your Droplet, and get
the default Nginx page:

|

.. image:: /images/FreeBSD_nginx_default.png

|

Finishing touches
===================

With a fully functioning jail, there are just 2 things left to do.

Locking down the firewall
----------------------------

The way things stand right now, your jail is working, but the host system is pretty
wide-open. If you edit your */etc/pf.conf* once more, we can restrict all IB
traffic that is not destined for a jail except for SSH.

|

.. code-block:: text

    # Define the interfaces
    ext_if = "vtnet0"
    int_if = "lo1"
    jail_net = $int_if:network

    # Define the IP address of jails
    # as well as ports to be allowed redirected
    WEBSERVER = "172.16.1.1"
    WEBSERVER_TCP_PORTS = "{ 80, 443 }"

    # Define the NAT for the jails
    nat on $ext_if from $jail_net to any -> ($ext_if)

    # Redirect traffic on ports 80 and 443 to the webserver jail
    rdr pass on $ext_if inet proto tcp to port $WEBSERVER_TCP_PORTS -> $WEBSERVER

    # Set the default: block everything
    block all

    # Allow the jail traffic to be translated
    pass from { lo0, $jail_net } to any keep state

    # Allow SSH in to the host
    pass in inet proto tcp to $ext_if port ssh

    # Allow OB traffic
    pass out all keep state

|

Tweaking the jail
-------------------

If you run the *date* command in your jail, you'll notice that the TimeZone
might be different from the host's timezone. You can fix that by running:

|

.. code-block:: bash

    tzsetup
|

from within the jail. It is the same process as you already went through earlier
when you set up the timesone for the host.

While you are in the jail, you should probably add the following lines to
*/etc/rc.conf* as well:

|

.. code-block:: text

    rpcbind_enable="NO"             # Disable the RPC daemon
    cron_flags="$cron_flags -J 15"  # Prevent lots of jails running cron jobs at the same time
    syslogd_flags="-ss"             # Disable syslogd listening for incoming connections
    sendmail_enable="NONE"          # Completely disable sendmail
    clear_tmp_enable="YES"          # Clear /tmp at startup

|

As you can see, they are basic commands for keeping your jail in order.

Next Steps
============

With the first jail out of the way, you can continue to add more and more.  The
high level steps would be along these lines:

#. Create a new lo1 alias with a unique IP address and netmask of 255.255.255.255
#. Define the jail in */etc/pf.conf*, including the IP, ports to be redirected, and the redirect rules.
#. Create the jail
